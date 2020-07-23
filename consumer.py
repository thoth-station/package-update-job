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
from package_update import __service_version__

from prometheus_client import generate_latest

import asyncio
import logging
import faust
import os
import ssl
from urllib.parse import urlparse
from aiohttp import web

init_logging()

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Thoth Package Update consumer v%s", __service_version__)

app = MessageBase().app

hash_mismatch_topic = HashMismatchMessage().topic
missing_package_topic = MissingPackageMessage().topic
missing_version_topic = MissingVersionMessage().topic

@app.page("/metrics")
async def get_metrics(self, request):
    """Serve the metrics from the consumer registry."""
    return web.Response(text=generate_latest().decode("utf-8"))


@app.page("/_health")
async def get_health(self, request):
    """Serve a readiness/liveness probe endpoint."""
    data = {"status": "ready", "version": __service_version__}
    return web.json_response(data)


# NOTE: if we can change the PROCESS functions to be async we can set `concurrency` of @app.agent to something > 1
@app.agent(hash_mismatch_topic)
async def consume_hash_mismatch(hash_mismatches):
    """Loop when a hash mismatch message is received."""
    async for mismatch in hash_mismatches:
        process_mismatch(mismatch)


@app.agent(missing_package_topic)
async def consume_missing_package(missing_packages):
    """Loop when a missing package message is received."""
    async for package in missing_packages:
        process_missing_package(package)


@app.agent(missing_version_topic)
async def consume_missing_version(missing_versions):
    """Loop when a missing version message is received."""
    async for version in missing_versions:
        missing_package_version_counter.inc()
        process_missing_version(version)

if __name__ == "__main__":
    app.main()
