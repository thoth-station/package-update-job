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

from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway

from thoth.common import init_logging
from thoth.storages import GraphDatabase
from thoth.python import Source

import logging
import os

from messages.missing_package import MissingPackageMessage
from messages.missing_version import MissingVersionMessage
from messages.hash_mismatch import HashMismatchMessage

init_logging()

_LOGGER = logging.getLogger("thoth.package_update")

prometheus_registry = CollectorRegistry()

_METRIC_MISSING_PACKAGE = Gauge(
    "package_update_missing_package",
    "Number of packages missing off of indexes.",
    ["namespace"],
    registry=prometheus_registry,
)

_METRIC_MISSING_VERSION = Gauge(
    "package_update_missing_version",
    "Number of individual versions messing off indexes.",
    ["namespace"],
    registry=prometheus_registry,
)

_METRIC_HASH_MISMATCH = Gauge(
    "package_update_hash_mismatch",
    "Number of package hash mismatches.",
    ["namespace"],
    registry=prometheus_registry,
)

namespace = os.getenv("THOTH_NAMESPACE")


def main():
    """Run package-update."""
    graph = GraphDatabase()
    graph.connect()

    removed_pkgs = set()

    hash_mismatch = HashMismatchMessage()
    missing_package = MissingPackageMessage()
    missing_version = MissingVersionMessage()

    all_pkgs = graph.get_python_packages_all(count=None, distinct=True)
    _LOGGER.info("Checking availability of %r package(s)", len(all_pkgs))
    for pkg in all_pkgs:
        src = Source(pkg[1])
        if not src.provides_package(pkg[0]):
            removed_pkgs.add((pkg[1], pkg[0]))
            missing_package.publish_to_topic(missing_package.MessageContents(index_url=pkg[1], package_name=pkg[0]))
            _METRIC_MISSING_PACKAGE.labels(namespace=namespace).inc()
            _LOGGER.debug("%r no longer provides %r", pkg[1], pkg[0])

    all_pkg_vers = graph.get_python_package_versions_all(count=None, distinct=True)
    _LOGGER.info("Checking integrity of %r package(s)", len(all_pkg_vers))
    for pkg_ver in all_pkg_vers:

        # Skip because we have already marked the entire package as missing
        if (pkg_ver[2], pkg_ver[0]) in removed_pkgs:
            continue

        src = Source(pkg_ver[2])
        if not src.provides_package_version(pkg_ver[0], pkg_ver[1]):
            missing_version.publish_to_topic(
                missing_version.MessageContents(
                    index_url=pkg_ver[2], package_name=pkg_ver[0], package_version=pkg_ver[1]
                )
            )
            _METRIC_MISSING_VERSION.labels(namespace=namespace).inc()
            _LOGGER.debug("%r no longer provides %r-%r", pkg_ver[2], pkg_ver[0], pkg_ver[1])
            continue

        source_hashes = sorted([i["sha256"] for i in src.get_package_hashes(pkg_ver[0], pkg_ver[1])])
        stored_hashes = sorted(graph.get_python_package_hashes_sha256(pkg_ver[0], pkg_ver[1], pkg_ver[2]))
        if not source_hashes == stored_hashes:
            hash_mismatch.publish_to_topic(
                hash_mismatch.MessageContents(index_url=pkg_ver[2], package_name=pkg_ver[0], package_version=pkg_ver[1])
            )
            _METRIC_HASH_MISMATCH.labels(namespace=namespace).inc()
            _LOGGER.debug("Source hashes:\n%r\nStored hashes:\n%r\nDo not match!", source_hashes, stored_hashes)


if __name__ == "__main__":
    main()
