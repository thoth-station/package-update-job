
from thoth.storages import GraphDatabase
from thoth.python import AIOSource
from thoth.python import Source
from thoth.common import _OPENSHIFT, init_logging
from thoth.sourcemanagement.sourcemanagement import SourceManagement
from thoth.sourcemanagement.enums import ServiceType

from prometheus_client import start_http_server, Counter

import asyncio
import logging
import faust
import os
import ssl
from urllib.parse import urlparse

from messages.missing_package import MissingPackageMessage
from messages.missing_version import MissingVersionMessage
from messages.hash_mismatch import HashMismatchMessage

init_logging()

_LOGGER = logging.getLogger("thoth.package_update")


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

GITHUB_PRIVATE_TOKEN = os.getenv(
    "THOTH_GITHUB_PRIVATE_TOKEN", None
)
GITLAB_PRIVATE_TOKEN = os.getenv(
    "THOTH_GITLAB_PRIVATE_TOKEN", None
)

ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=_KAFKA_CAFILE)
app = faust.App("thoth-messaging", broker=_KAFKA_BOOTSTRAP_SERVERS, ssl_context=ssl_context, web_enabled=False)

graph = GraphDatabase()
graph.connect()

start_http_server(8000, addr="/metrics")
# TODO: query prometheus scraper and get or create values for all metrics for now we will set them all to 0
# NOTE: these counters are temp metrics as they are already exposed by Kafka
hash_mismatch_counter = Counter(
    "thoth_package-update_hashmismatch_total",
    "Total number of hashmismatches found.",
    ["thoth", "package-update"],
)
missing_package_counter = Counter(
    "thoth_package-update_missingpackage_total",
    "Total number of hashmismatches found.",
    ["thoth", "package-update"],
)
missing_package_version_counter = Counter(
    "thoth_package-update_missingversion_total",
    "Total number of hashmismatches found.",
    ["thoth", "package-update"],
)

# NOTE: This could be moved to thoth-sourcemanagement
def git_source_from_url(url: str) -> SourceManagement:
    res = urlparse(url)
    path = res.path.split('/')
    service_url = res.netloc
    service_name = service_url.split('.')[-2]     # all urls should look something like x.x.github.com
    s_type = ServiceType.by_name(service_name)
    if s_type = ServiceType.GITHUB:
        token = GITHUB_PRIVATE_TOKEN
    elif s_type = ServiceType.GITLAB:
        token = GITLAB_PRIVATE_TOKEN
    else:
        raise NotImplementedError("There is no token for this service type")
    return SourceManagement(service_type, res.scheme + "://" + res.netloc, token, res.path)

# TODO: for storages we need the following functions:
#       update_hash_mismatch(index_url, package_name, package_version, new_hash)


@app.agent(hash_mismatch_topic)
async def consume_hash_mismatch(hash_mismatches):
    """Dump the messages received."""
    async for mismatch in hash_mismatches:
        # TODO: update the hashes in the database? or is this done by solver
        hash_mismatch_counter.inc()

        # NOTE: This may work better as an argo work flow which looks something like:
        #   A B C
        #    ╲|╱
        #     D
        # Where A, B, C are all solvers and D is a container which warns all users of change
        try:
            analysis_id = _OPENSHIFT.schedule_all_solvers(
                packages=f"{mismatch.package_name}==={mismatch.package_version}",
                indexes=[mismatch.index_url],
                output=_SOLVER_OUTPUT,
                transitive=False,   # NOTE: not sure what option should be used here
            )
        except Exception:
            # If we get some errors from OpenShift master - do not retry. Rather schedule the remaining
            # ones and try to schedule the given package in the next run.
            _LOGGER.exception(
                f"Failed to schedule new solver to solve package {mismatch.package_name} in version"
                f" {mismatch.package_version}, the graph refresh job will not fail but will try to reschedule"
                " this in next run"
            )

        repositories = graph.get_all_repositories_using_package_version(
            index_url=mismatch.index_url,
            package_name=mismatch.package_name,
            package_version=mismatch.package_version,
        )

        issue_title = f"Hash mismatch for {mismatch.package_name}=={mismatch.package_version} on {mismatch.index_url}"
        issue_body = lambda: "Automated message from package change detected by thoth.package-update"

        for repo in repositories:
            gitservice_repo = git_source_from_url(repo)
            gitservice_repo.open_issue_if_not_exist(issue_title, issue_body)

@app.agent(missing_package_topic)
async def consume_missing_package(missing_packages):
    """Dump the messages received."""
    async for package in missing_packages:
        missing_package_counter.inc()
        # TODO: determine how to mark an entire package as missing in the database

        # TODO: open issue if package is a direct dependency of the user, otherwise rerun thamos-advise/kebechet
        repostiories = graph.get_all_repositories_using_package(
            index_url=package.index_url,
            package_name=package.package_name
        )

        issue_title = f"Missing package {package.package_name} on {package.index_url}"
        issue_body = lambda: "Automated message from package change detected by thoth.package-update"

        for repo in repositories:
            gitservice_repo = git_source_from_url(repo)
            gitservice_repo.open_issue_if_not_exist(issue_title, issue_body)

@app.agent(missing_version_topic)
async def consume_missing_version(missing_versions):
    """Dump the messages received."""
    async for version in missing_versions:
        missing_package_version_counter.inc()
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

        issue_title = f"Missing package version {version.package_name}=={version.package_version} on {version.index_url}"
        issue_body = lambda: "Automated message from package change detected by thoth.package-update"

        for repo in repositories:
            gitservice_repo = git_source_from_url(repo)
            gitservice_repo.open_issue_if_not_exist(issue_title, issue_body)

if __name__ == "__main__":
    app.main()