#!/usr/bin/env python3
# thoth-package-update
# Copyright(C) 2020 Kevin Postlethwait
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This is run periodically to ensure integrity of Python Packages stored in the database."""

from thoth.storages import GraphDatabase
from thoth.python import AIOSource, AsyncIterableVersions
from thoth.python import Source
from thoth.common import init_logging
from thoth.messaging import missing_package_message, missing_version_message, hash_mismatch_message
from thoth.messaging.missing_package import MessageContents as MissingPackageContents
from thoth.messaging.missing_version import MessageContents as MissingVersionContents
from thoth.messaging.hash_mismatch import MessageContents as HashMismatchContents
import thoth.messaging.producer as producer

import asyncio
import logging
import os
import ssl
from functools import wraps
from aiohttp.client_exceptions import ClientResponseError
from typing import Dict, Any, Tuple, Callable

from package_update import __service_version__ as __package_update_version__

init_logging()

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Thoth package update producer v%s", __package_update_version__)

SEMAPHORE_LIMIT = int(os.getenv("THOTH_PACKAGE_UPDATE_SEMAPHORE_LIMIT", 1000))
async_sem = asyncio.Semaphore(SEMAPHORE_LIMIT)
COMPONENT_NAME = "package-update-job"

p = producer.create_producer()


def redirect_exception_message(func):
    """Redirect a messages exception to be logged instead of halting execution."""

    async def inner_function(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except Exception(e):
            _LOGGER.warning(e)

    return inner_function


def with_semaphore(async_sem) -> Callable:
    """Only have N async functions running at the same time."""

    def somedec_outer(fn):
        @wraps(fn)
        async def somedec_inner(*args, **kwargs):
            async with async_sem:
                response = await fn(*args, **kwargs)
            return response

        return somedec_inner

    return somedec_outer


@with_semaphore(async_sem)
async def _gather_index_info(index: str, aggregator: Dict[str, Any]) -> None:
    aggregator[index] = dict()
    aggregator[index]["source"] = AIOSource(index)
    result = await aggregator[index]["source"].get_packages()
    aggregator[index]["packages"] = result
    aggregator[index]["packages"] = aggregator[index]["packages"].packages


def _check_package_availability(package: Tuple[str, str, str], sources: Dict[str, Any], removed_packages: set) -> bool:
    src = sources[package[1]]
    if not package[0] in src.get("packages", []):
        removed_packages.add((package[1], package[0]))
        try:
            producer.publish_to_topic(
                p,
                missing_package_message,
                MissingPackageContents(
                    index_url=package[1],
                    package_name=package[0],
                    component_name=COMPONENT_NAME,
                    service_version=__package_update_version__,
                ),
            )
            _LOGGER.info("%r no longer provides %r", package[1], package[0])
            return False
        except Exception as e:
            _LOGGER.exception("Failed to publish with the following error message: %r", e)
    return True


@with_semaphore(async_sem)
async def _check_hashes(
    package_version: Tuple[str, str, str], package_versions, source, removed_packages: set, graph: GraphDatabase,
) -> bool:
    if not package_version[1] in package_versions.versions:
        try:
            producer.publish_to_topic(
                p,
                missing_version_message,
                MissingVersionContents(
                    index_url=package_version[2],
                    package_name=package_version[0],
                    package_version=package_version[1],
                    component_name=COMPONENT_NAME,
                    service_version=__package_update_version__,
                ),
            )
            _LOGGER.info("%r no longer provides %r-%r", package_version[2], package_version[0], package_version[1])
            return False
        except Exception as identifier:
            _LOGGER.exception("Failed to publish with the following error message: %r", str(identifier))

    try:
        source_hashes = {i["sha256"] for i in await source.get_package_hashes(package_version[0], package_version[1])}
    except ClientResponseError:
        _LOGGER.warning(
            "404 error retrieving hashes for: %r==%r on %r", package_version[0], package_version[1], package_version[2],
        )
        return False  # webpage might be down

    stored_hashes = set(
        graph.get_python_package_hashes_sha256(package_version[0], package_version[1], package_version[2]),
    )
    if not source_hashes == stored_hashes:
        try:
            producer.publish_to_topic(
                p,
                hash_mismatch_message,
                HashMismatchContents(
                    index_url=package_version[2],
                    package_name=package_version[0],
                    package_version=package_version[1],
                    missing_from_source=list(stored_hashes - source_hashes),
                    missing_from_database=list(source_hashes - stored_hashes),
                    component_name=COMPONENT_NAME,
                    service_version=__package_update_version__,
                ),
            )
            _LOGGER.debug("Source hashes:\n%r\nStored hashes:\n%r\nDo not match!", source_hashes, stored_hashes)
            return False
        except Exception as identifier:
            _LOGGER.exception("Failed to publish with the following error message: %r", str(identifier))

    return True


@with_semaphore(async_sem)
async def _get_all_versions(package_name: str, source: str, sources, accumulator: Dict[Tuple[Any, Any], Any]):
    src = sources[source]["source"]
    try:
        accumulator[(package_name, source)] = await src.get_package_versions(package_name)
    except ClientResponseError:
        _LOGGER.warning(
            "404 error retrieving versions for: %r on %r", package_name, source,
        )


async def main():
    """Run package-update."""
    graph = GraphDatabase()
    graph.connect()

    removed_pkgs = set()

    indexes = {x["url"] for x in graph.get_python_package_index_all(enabled=True)}
    sources = dict()

    async_tasks = []
    for i in indexes:
        async_tasks.append(_gather_index_info(i, sources))
    await asyncio.gather(*async_tasks, return_exceptions=True)
    async_tasks.clear()

    all_pkgs = graph.get_python_packages_all(count=None, distinct=True)
    _LOGGER.info("Checking availability of %r package(s)", len(all_pkgs))
    for pkg in all_pkgs:
        _check_package_availability(
            package=pkg, sources=sources, removed_packages=removed_pkgs,
        )

    all_pkg_vers = graph.get_python_package_versions_all(count=None, distinct=True)

    all_pkg_names = {(i[0], i[2]) for i in all_pkg_vers}

    versions = dict.fromkeys(all_pkg_names)

    for i in all_pkg_names:
        async_tasks.append(_get_all_versions(package_name=i[0], source=i[1], sources=sources, accumulator=versions))
    await asyncio.gather(*async_tasks, return_exceptions=True)
    async_tasks.clear()

    _LOGGER.info("Checking integrity of %r package(s)", len(all_pkg_vers))
    for pkg_ver in all_pkg_vers:
        # Skip because we have already marked the entire package as missing
        if (pkg_ver[2], pkg_ver[0]) in removed_pkgs or versions[(pkg_ver[0], pkg_ver[2])] is None:  # in case of 404
            continue
        src = sources[pkg_ver[2]]["source"]
        async_tasks.append(
            _check_hashes(
                package_version=pkg_ver,
                package_versions=versions[(pkg_ver[0], pkg_ver[2])],
                source=src,
                removed_packages=removed_pkgs,
                graph=graph,
            ),
        )

    await asyncio.gather(*async_tasks, return_exceptions=True)
    async_tasks.clear()
    p.flush()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
