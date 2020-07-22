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

"""Consume messages produced by package-update.py faust app."""

from thoth.python import AIOSource
from thoth.python import Source
from thoth.common import init_logging
from thoth.messaging import MissingPackageMessage, MissingVersionMessage, HashMismatchMessage, MessageBase
from package_update.process_message import process_mismatch, process_missing_package, process_missing_version

from prometheus_client import start_http_server, Counter

import asyncio
import logging
import faust
import os
import ssl
from urllib.parse import urlparse

init_logging()

_LOGGER = logging.getLogger("thoth.package_update")

app = MessageBase.app

start_http_server(8000)
# TODO: query prometheus scraper and get or create values for all metrics for now we will set them all to 0
# NOTE: these counters are temp metrics as they are already exposed by Kafka
hash_mismatch_counter = Counter(
    "thoth_package_update_hashmismatch_total",
    "Total number of hashmismatches found.",
)
missing_package_counter = Counter(
    "thoth_package_update_missingpackage_total",
    "Total number of hashmismatches found.",
)

missing_package_version_counter = Counter(
    "thoth_package_update_missingversion_total",
    "Total number of hashmismatches found.",
)

hash_mismatch_topic = HashMismatchMessage().topic
missing_package_topic = MissingPackageMessage().topic
missing_version_topic = MissingVersionMessage().topic


@app.agent(hash_mismatch_topic)
async def consume_hash_mismatch(hash_mismatches):
    """Loop when a hash mismatch message is received."""
    async for mismatch in hash_mismatches:
        # TODO: update the hashes in the database? or is this done by solver
        hash_mismatch_counter.inc()

        # NOTE: This may work better as an argo work flow which looks something like:
        #   A B C
        #    ╲|╱
        #     D
        # Where A, B, C are all solvers and D is a container which warns all users of change
        process_mismatch(mismatch)


@app.agent(missing_package_topic)
async def consume_missing_package(missing_packages):
    """Loop when a missing package message is received."""
    async for package in missing_packages:
        missing_package_counter.inc()
        # TODO: determine how to mark an entire package as missing in the database

        # TODO: open issue if package is a direct dependency of the user, otherwise rerun thamos-advise/kebechet
        process_missing_package(package)


@app.agent(missing_version_topic)
async def consume_missing_version(missing_versions):
    """Loop when a missing version message is received."""
    async for version in missing_versions:
        missing_package_version_counter.inc()
        process_missing_version(version)

if __name__ == "__main__":
    start_http_server(8000)
    app.main()
