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
from thoth.python import Source

import logging
import concurrent.futures

from messages.missing_package import MissingPackageMessage
from messages.missing_version import MissingVersionMessage
from messages.hash_mismatch import HashMismatchMessage

_LOGGER = logging.getLogger(__name__)

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

hash_mismatch = HashMismatchMessage()
missing_package = MissingPackageMessage()
missing_version = MissingVersionMessage()

removed_pkgs = set()

def check_package_availability(pkg: tuple):
    src = Source(pkg[1])
    provides = src.provides_package(pkg[0])
    if not provides:
        removed_pkgs.add(f"{pkg[1]}-{pkg[0]}")
        missing_package.publish_to_topic(missing_package.MessageContents(index_url=pkg[1], package_name=pkg[0]))
        _LOGGER.debug("%r no longer provides %r", pkg[1], pkg[0])


def check_python_package_version(pkg_ver: tuple, graph: GraphDatabase):
    # Skip because we have already marked the entire package as missing
    if f"{pkg_ver[2]}-{pkg_ver[0]}" in removed_pkgs:
        return

    src = Source(pkg_ver[2])
    if not src.provides_package_version(pkg_ver[0], pkg_ver[1]):
        missing_version.publish_to_topic(
            missing_version.MessageContents(
                index_url=pkg_ver[2], package_name=pkg_ver[0], package_version=pkg_ver[1]
            )
        )
        _LOGGER.debug("%r no longer provides %r-%r", pkg_ver[2], pkg_ver[0], pkg_ver[1])
        return

    source_hashes = sorted([i["sha256"] for i in src.get_package_hashes(pkg_ver[0], pkg_ver[1])])
    stored_hashes = sorted(graph.get_python_package_hashes_sha256(pkg_ver[0], pkg_ver[1], pkg_ver[2]))
    if not source_hashes == stored_hashes:
        hash_mismatch.publish_to_topic(
            hash_mismatch.MessageContents(index_url=pkg_ver[2], package_name=pkg_ver[0], package_version=pkg_ver[1])
        )
        _LOGGER.debug("Source hashes:\n%r\nStored hashes:\n%r\nDo not match!", source_hashes, stored_hashes)

def main():
    """Run package-update."""
    graph = GraphDatabase()
    graph.connect()

    all_pkgs = graph.get_python_packages_all(count=9999999999999, distinct=True)
    all_pkgs_len = len(all_pkgs)

    _LOGGER.info("Checking availability of %r package(s)", all_pkgs_len)

    threads = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for pkg in all_pkgs:
            executor.submit(check_package_availability, pkg)

    all_pkg_vers = graph.get_python_package_versions_all(count=99999999999, distinct=True)
    all_pkg_vers_len = len(all_pkg_vers)
    _LOGGER.info("Checking integrity of %r package(s)", len(all_pkg_vers))

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for pkg_ver in all_pkg_vers:
            executor.submit(check_python_package_version, pkg_ver, graph)

if __name__ == "__main__":
    main()
