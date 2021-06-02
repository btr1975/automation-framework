"""
Utilities
"""
import json
import hashlib


def msg_value_to_dict(msg):
    """Function to convert Kafka Message Value to a Dict

    :type msg: Kafka Message
    :param msg: The Kafka message

    :rtype: Dict
    :returns: The Kafka message value as a Dict

    """
    return json.loads(msg.value().decode('utf-8'))


def msg_key_to_string(msg):
    """Function to convert Kafka Message Key to a String

    :type msg: Kafka Message
    :param msg: The Kafka message

    :rtype: String
    :returns: The Kafka message key as a string

    """
    return json.loads(msg.key().decode('utf-8'))


def get_python_dict_hash_sha256(python_dict):
    """Function to get sha256 hash from a Dict

    :type python_dict: Dict
    :param python_dict: Any python Dict

    :rtype: String
    :returns: Hash Value

    """
    return hashlib.sha256(json.dumps(python_dict).encode('utf-8')).hexdigest()
