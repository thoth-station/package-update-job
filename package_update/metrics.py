
#!/usr/bin/env python3
# thoth-package_update
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


"""This is Thoth package update consumer metrics."""


from package_update import __service_version__

from prometheus_client import Gauge, Counter


# add the application version info metric
package_update_info = Gauge("package_update_consumer_info", "Package Update Version Info", labelnames=["version"])
package_update_info.labels(version=__service_version__).inc()

# Metrics for Kafka
in_progress = Gauge(
    "messages_in_progress",
    "Total number of messages currently being processed. This will be 1 or 0 unless an async version is implemented",
    ["message_name"],
)
exceptions = Counter(
    "message_exceptions",
    "Number of messages which failed to be processed.",
    ["message_name"],
)
success = Counter(
    "messages_processed",
    "Number of hash mismatch messages which were successfully processed.",
    ["message_name"],
)

hash_mismatch_in_progress = in_progress.labels(message_name="hash_mismatch")
hash_mismatch_exceptions = exceptions.labels(message_name="hash_mismatch")
hash_mismatch_success = success.labels(message_name="hash_mismatch")

missing_version_in_progress = in_progress.labels(message_name="missing_version")
missing_version_exceptions = exceptions.labels(message_name="missing_version")
missing_version_success = success.labels(message_name="missing_version")

missing_package_in_progress = in_progress.labels(message_name="missing_package")
missing_package_exceptions = exceptions.labels(message_name="missing_package")
missing_package_success = success.labels(message_name="missing_package")
