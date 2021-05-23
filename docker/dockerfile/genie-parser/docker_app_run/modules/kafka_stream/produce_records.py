"""
Producer Utilities
"""
import json
import hashlib


class ProduceRecords:
    """Class to produce records to Kafka

    :type producer: confluent_kafka.Producer Object
    :param producer: The producers to send to
    :type topic: String
    :param topic: The topic to send to

    :rtype: None
    :returns: None
    """

    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic

    def produce_rerecords(self, records):
        """Method to produce records to Kafka

        :type records: Dict or List of Dicts
        :param records: The records to send

        :rtype: None
        :returns: None
        """
        self._send_records(records=records)

        # Wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        self.producer.flush()

    @staticmethod
    def delivery_report(err, msg):
        """Method to check if a message is delivered or failed, used as a callback
        when sending records. Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush().
        """
        if err is not None:
            print(f'Message delivery failed: {err}')

        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def _send_single_record(self, data):
        """Method used to send a single record"

        :type data: Dict
        :param data: The record data

        :rtype: None
        :returns: None

        """
        # Trigger any available delivery report callbacks from previous produce() calls
        self.producer.poll(0)

        json_data = json.dumps(data)

        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.
        self.producer.produce(topic=self.topic, key='{}'.format(hashlib.sha224(json_data.encode('utf-8')).hexdigest()),
                              value=json_data.encode('utf-8'), callback=self.delivery_report)

    def _send_list_of_records(self, data_list):
        """Method to send a list of records

        :type data_list: List of Dicts
        :param data_list: The record data

        :rtype: None
        :returns: None

        :raises TypeError: If the data in each list entry is not a dictionary
        """
        for data in data_list:
            if not isinstance(data, dict):
                raise TypeError(f'data must be a dict, but received a {type(data)}!!')

            self._send_single_record(data)

    def _send_records(self, records=None):
        """Method to send records

        :type records: Dict or List of Dicts
        :param records: The record data

        :rtype: None
        :returns: None

        :raises TypeError: If records is not a list or a dictionary
        """
        if isinstance(records, list):
            self._send_list_of_records(records)

        elif isinstance(records, dict):
            self._send_single_record(records)

        else:
            raise TypeError(f'records must be a list or a dict, but received a {type(records)}!!')
