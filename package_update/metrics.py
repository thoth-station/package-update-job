
#!/usr/bin/env python3
# thoth-investigator
# Copyright(C) 2020 Christoph Görn
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


"""This is Thoth investigator consumer metrics."""


from package_update import __version__ as __package_update_version__

from prometheus_client import Gauge, Counter


# add the application version info metric
investigator_info = Gauge("package_update_consumer_info", "Package Update Version Info", labelnames=["version"])
investigator_info.labels(version=__package_update_version__).inc()

# Metrics for Kafka
mismatch_in_progress = Gauge(
    "hash_mismatch_in_progress",
    "Total number of hashmismatch messages currently being processed. This will be 1 or 0 unless an async version is implemented",
)
mismatch_exceptions = Counter(
    "hash_mismatch_exceptions",
    "Number of hash mismatch messages which failed to be processed.",
)
mismatch_success = Counter(
    "hash_mismatch_processed",
    "Number of hash mismatch messages which were successfully processed.",
)

missing_version_in_progress = Gauge(
    "missing_version_in_progress",
    "Total number of missing version messages currently being processed.",
)
missing_version_exceptions = Counter(
    "missing_version_exceptions",
    "Number of missing version messages which failed to be processed.",
)
missing_version_success = Counter(
    "missing_version_processed",
    "Number of missing version messages which were successfully processed.",
)

missing_package_in_progress = Gauge(
    "missing_package_in_progress",
    "Total number of missing package messages currently being processed.",
)
missing_package_exceptions = Counter(
    "missing_package_exceptions",
    "Number of missing package messages which failed to be processed.",
)
missing_package_success = Counter(
    "missing_package_processed",
    "Number of missing package messages which were successfully processed.",
)
