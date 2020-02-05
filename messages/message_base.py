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

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic


_LOGGER = logging.getLogger(__name__)


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_CAFILE = os.getenv("KAFKA_CAFILE", "ca.crt")
KAFKA_CLIENT_ID = os.getenv("KAFKA_CLIENT_ID", "thoth-messaging")
KAFKA_PROTOCOL = os.getenv("KAFKA_PROTOCOL", "SSL")

MESSAGE_BASE_TOPIC = "base-topic"

class MessageBase:
    """Class used for Package Release events on Kafka topic."""

    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        # client_id=KAFKA_CAFILE,
        # security_protocol=KAFKA_PROTOCOL,
        # ssl_cafile=KAFKA_CAFILE,
    )

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        acks=0,  # Wait for leader to write the record to its local log only.
        compression_type="gzip",
        # value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        # security_protocol=KAFKA_PROTOCOL,
        # ssl_cafile=KAFKA_CAFILE,
    )

    def __init__(self, topic_name: str = MESSAGE_BASE_TOPIC, num_partitions: int = 1, replication_factor: int = 1):
        self.topic = topic_name
        self.create_topic(num_partitions = num_partitions, replication_factor = replication_factor)

    def create_topic(self, num_partitions: int = 1, replication_factor: int = 1):
        """Create the topic on our Kafka broker."""
        topic_list = []

        try:
            new_topic = NewTopic(name=self.topic, num_partitions=num_partitions, replication_factor=replication_factor)
            topic_list.append(new_topic)

            self.admin_client.create_topics(new_topics=topic_list, validate_only=False)
        except kafka.errors.TopicAlreadyExistsError as excptn:
            _LOGGER.debug("Topic already exists")

    def publish_to_topic(self, payload: dict):
        """Publish the given dict to a Kafka topic."""
        try:
            future = self.producer.send(self.topic_name, payload)
            result = future.get(timeout=6)
            _LOGGER.debug(result)
        except AttributeError as excptn:
            _LOGGER.debug(excptn)
        except (kafka.errors.NotLeaderForPartitionError, kafka.errors.KafkaTimeoutError) as excptn:
            _LOGGER.exception(excptn)
