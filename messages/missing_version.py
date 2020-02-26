#!/usr/bin/env python3
# thoth-messaging
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


"""This is Thoth Messaging module."""


import os
import json
import logging

import kafka
import faust

from .message_base import MessageBase

_LOGGER = logging.getLogger("thoth.package_update.messages")


class MissingVersionMessage(MessageBase):
    """Class used for Package Release events on Kafka topic."""

    topic_name = "thoth.package-update.missing-package-version"

    class MessageContents(faust.Record, serializer="json"):
        """Class used to represent a contents of a missing-package message Kafka topic."""

        index_url: str
        package_name: str
        package_version: str

    def __init__(self, num_partitions: int = 1, replication_factor: int = 1):
        """Initialize missing-package-version topic."""
        super(MissingVersionMessage, self).__init__(
            self.topic_name,
            value_type=self.MessageContents,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )
