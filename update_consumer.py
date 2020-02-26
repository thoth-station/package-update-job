
from thoth.storages import GraphDatabase
from thoth.python import AIOSource
from thoth.python import Source
from thoth.common import _OPENSHIFT

import asyncio
import logging
import faust
import os
import ssl

from messages.missing_package import MissingPackageMessage
from messages.missing_version import MissingVersionMessage
from messages.hash_mismatch import HashMismatchMessage

_LOGGER = logging.getLogger(__name__)


_KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
_KAFKA_CAFILE = os.getenv("KAFKA_CAFILE", "ca.crt")
KAFKA_CLIENT_ID = os.getenv("KAFKA_CLIENT_ID", "thoth-messaging")
KAFKA_PROTOCOL = os.getenv("KAFKA_PROTOCOL", "SSL")
KAFKA_TOPIC_RETENTION_TIME_SECONDS = 60 * 60 * 24 * 45

_SOLVER_OUTPUT = os.getenv(
    "THOTH_SOLVER_OUTPUT", "http://result-api/api/v1/solver-result"
)
_PACKAGE_ANALYZER_OUTPUT = os.getenv(
    "THOTH_PACKAGE_ANALYZER_OUTPUT", "http://result-api/api/v1/package-analysis-result"
)
_SUBGRAPH_CHECK_API = os.getenv(
    "THOTH_SUBGRAPH_CHECK_API", "http://result-api/api/v1/subgraph-check"
)

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=_KAFKA_CAFILE)
app = faust.App("thoth-messaging", broker=_KAFKA_BOOTSTRAP_SERVERS, ssl_context=ssl_context, web_enabled=False)

graph = GraphDatabase()
graph.connect()

# TODO: for storages we need the following functions:
#       flag_missing_package_version(index_url, package_name, package_version)
#       get_repositories_which_use_package(index_url, package_name)
#       get_repositories_which_use_package_version(index_url, package_name, package_version)
#       update_hash_mismatch(index_url, package_name, package_version, new_hash)

# TODO: kebechet source management needs to be moved to its own package so it can be used by this — as well as other 
#       repositories

@app.agent(hash_mismatch_topic)
async def consume_hash_mismatch(hash_mismatches):
    """Dump the messages received."""
    async for mismatch in hash_mismatches:
        # TODO: update the hashes in the database


        # NOTE: This would work better as an argo work flow which looks something like:
        #   A B C
        #    ╲|╱
        #     D
        # Where A, B, C are all solvers and D is a container which warns all users of change
        # TODO: rerun solver
        try:
            analysis_id = _OPENSHIFT.schedule_all_solvers(
                packages=f"{package_name}==={package_version}",
                indexes=[index_url],
                output=_SOLVER_OUTPUT,
                transitive=False,   # NOTE: not sure what option should be used here
            )
        except Exception:
            # If we get some errors from OpenShift master - do not retry. Rather schedule the remaining
            # ones and try to schedule the given package in the next run.
            _LOGGER.exception(
                f"Failed to schedule new solver to solve package {package_name} in version {package_version}, "
                "the graph refresh job will not fail but will try to reschedule this in next run"
            )

        # TODO: warn users if the hash of the package they were using changes
        graph.get_all_repositories_using_package_version(
            index_url=mismatch.index_url,
            package_name=mismatch.package_name,
            package_version=mismatch.package_version,
        )
        app.log.info(f"{release}")

@app.agent(missing_package_topic)
async def consume_missing_package(missing_packages):
    """Dump the messages received."""
    async for package in missing_packages:
        # TODO: determine how to mark an entire package as missing in the database

        # TODO: open issue if package is a direct dependency of the user, otherwise rerun thamos-advise/kebechet
        graph.get_all_repositories_using_package(index_url=package.index_url, package_name=package.package_name)
        app.log.info(f"{release}")

@app.agent(missing_version_topic)
async def consume_missing_version(missing_versions):
    """Dump the messages received."""
    async for version in missing_versions:
        graph.update_missing_flag_package_version(
            index_url=version.index_url,
            package_name=version.package_name,
            package_version=version.package_version,
            value=True,
        )

        # TODO: rerun thamos-advise/kebechet on any source using this package.
        #       this might be best done as an argo workflow?
        graph.get_all_repositories_using_package_version(
            index_url=version.index_url,
            package_name=version.package_name,
            package_version=version.package_version,
        )

        app.log.info(f"{release}")

if __name__ == "__main__":
    app.main()