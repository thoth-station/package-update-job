#!/usr/bin/env python3
# thoth-storages
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
from thoth.python import AIOSource
from thoth.python import Source
from thoth.common import init_logging

import asyncio
import logging
import faust
import os
import ssl

from messages.missing_package import MissingPackageMessage
from messages.missing_version import MissingVersionMessage
from messages.hash_mismatch import HashMismatchMessage
from messages.message_base import MessageBase

init_logging()

_LOGGER = logging.getLogger("thoth.package_update")

app = MessageBase.app

namespace = os.getenv("THOTH_NAMESPACE")


@app.command()
async def main():
    """Run package-update."""
    graph = GraphDatabase()
    graph.connect()

    removed_pkgs = set()

    hash_mismatch = HashMismatchMessage()
    missing_package = MissingPackageMessage()
    missing_version = MissingVersionMessage()

    indexes = {x["url"] for x in graph.get_python_package_index_all()}
    sources = dict()
    for i in indexes:
        sources[i] = dict()
        sources[i]["source"] = AIOSource(i)
        sources[i]["packages"] = await sources[i]["source"].get_packages()
        sources[i]["packages"] = sources[i]["packages"].packages

    all_pkgs = graph.get_python_packages_all(count=None, distinct=True)
    _LOGGER.info("Checking availability of %r package(s)", len(all_pkgs))
    for pkg in all_pkgs:
        src = sources[pkg[1]]
        if not pkg[0] in src["packages"]:
            removed_pkgs.add((pkg[1], pkg[0]))
            try:
                await missing_package.publish_to_topic(missing_package.MessageContents(
                    index_url=pkg[1],
                    package_name=pkg[0],
                ))
                _LOGGER.info("%r no longer provides %r", pkg[1], pkg[0])
            except Exception as e:
                _LOGGER.exception("Failed to publish with the following error message: %r", e)

    all_pkg_vers = graph.get_python_package_versions_all(count=None, distinct=True)
    _LOGGER.info("Checking integrity of %r package(s)", len(all_pkg_vers))
    for pkg_ver in all_pkg_vers:

        # Skip because we have already marked the entire package as missing
        if (pkg_ver[2], pkg_ver[0]) in removed_pkgs:
            continue

        src = sources[pkg_ver[2]]["source"]
        package_versions = await src.get_package_versions(pkg_ver[0])
        if not pkg_ver[1] in package_versions.versions:

            try:
                await missing_version.publish_to_topic(
                    missing_version.MessageContents(
                        index_url=pkg_ver[2], package_name=pkg_ver[0], package_version=pkg_ver[1]
                    )
                )
                _LOGGER.info("%r no longer provides %r-%r", pkg_ver[2], pkg_ver[0], pkg_ver[1])
            except Exception as identifier:
                _LOGGER.exception("Failed to publish with the following error message: %r", identifier.msg)

            continue

        source_hashes = {i["sha256"] for i in await src.get_package_hashes(pkg_ver[0], pkg_ver[1])}
        stored_hashes = set(graph.get_python_package_hashes_sha256(pkg_ver[0], pkg_ver[1], pkg_ver[2]))
        if not source_hashes == stored_hashes:
            try:
                await hash_mismatch.publish_to_topic(
                    hash_mismatch.MessageContents(
                        index_url=pkg_ver[2],
                        package_name=pkg_ver[0],
                        package_version=pkg_ver[1],
                        missing_from_source=list(stored_hashes-source_hashes),
                        missing_from_database=list(source_hashes-stored_hashes),
                    )
                )
                _LOGGER.debug("Source hashes:\n%r\nStored hashes:\n%r\nDo not match!", source_hashes, stored_hashes)
            except Exception as identifier:
                _LOGGER.exception("Failed to publish with the following error message: %r", identifier.msg)


if __name__ == "__main__":
    app.main()
