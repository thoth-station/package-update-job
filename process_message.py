from thoth.common import init_logging, OpenShift
from thoth.storages import GraphDatabase
from thoth.python import AIOSource
from thoth.python import Source
from thoth.sourcemanagement.sourcemanagement import SourceManagement
from thoth.sourcemanagement.enums import ServiceType


from prometheus_client import start_http_server, Counter, Gauge

import asyncio
import logging
import faust
import os
import ssl
from urllib.parse import urlparse
from time import time

from messages.missing_package import MissingPackageMessage
from messages.missing_version import MissingVersionMessage
from messages.hash_mismatch import HashMismatchMessage

init_logging()

_LOGGER = logging.getLogger("thoth.package_update")

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

_OPENSHIFT = OpenShift()
graph = GraphDatabase()
graph.connect()

missing_package_process_runtime = Gauge(
    "thoth_package_update_missing_package_runtime",
    "Time to process missing package message.",
    ["thoth", "package_update"],
)
hash_mismatch_process_runtime = Gauge(
    "thoth_package_update_hashmismatch_runtime",
    "Time to process hash mismatch message.",
    ["thoth", "package_update"],
)
missing_version_process_runtime = Gauge(
    "thoth_package_update_missing_version_runtime",
    "Time to process missing version message.",
    ["thoth", "package_update"],
)

"""Process message for update_consumer."""


def gauge_function_time(gauge: Gauge):
    """Wrapper which uses a defined Gauge to post a metric about function execution time."""
    def measure_function_time(func):
        def inner_func1():
            start = time.time()
            func(*args, *kwargs)
            end = time.time()
            gauge.set(end - start)

        return inner_func1
    return measure_function_time


# NOTE: This could be moved to thoth-sourcemanagement
def git_source_from_url(url: str) -> SourceManagement:
    """Parse URL to get SourceManagement object."""
    res = urlparse(url)
    path = res.path.split('/')
    service_url = res.netloc
    service_name = service_url.split('.')[-2]     # all urls should look something like x.x.github.com
    s_type = ServiceType.by_name(service_name)
    if s_type == ServiceType.GITHUB:
        token = GITHUB_PRIVATE_TOKEN
    elif s_type == ServiceType.GITLAB:
        token = GITLAB_PRIVATE_TOKEN
    else:
        raise NotImplementedError("There is no token for this service type")
    return SourceManagement(service_type, res.scheme + "://" + res.netloc, token, res.path)


@gauge_function_time(hash_mismatch_process_runtime)
def process_mismatch(mismatch):
    """Process a hash mismatch message from package-update producer."""
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
    def issue_body(): return "Automated message from package change detected by thoth.package-update"

    for repo in repositories:
        gitservice_repo = git_source_from_url(repo)
        gitservice_repo.open_issue_if_not_exist(issue_title, issue_body)


@gauge_function_time(missing_package_process_runtime)
def process_missing_package(package):
    """Process a missing package message from package-update producer."""
    repostiories = graph.get_all_repositories_using_package(
        index_url=package.index_url,
        package_name=package.package_name
    )

    issue_title = f"Missing package {package.package_name} on {package.index_url}"
    def issue_body(): return "Automated message from package change detected by thoth.package-update"

    for repo in repositories:
        gitservice_repo = git_source_from_url(repo)
        gitservice_repo.open_issue_if_not_exist(issue_title, issue_body)


@gauge_function_time(missing_version_process_runtime)
def process_missing_version(version):
    """Process a missing version message from package-update producer."""
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
