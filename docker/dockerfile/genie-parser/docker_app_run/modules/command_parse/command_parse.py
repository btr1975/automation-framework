"""
This holds functionality to get commands, and parse commands

"""
from quick_netmiko import QuickNetmiko
from pyats_genie_command_parse import GenieCommandParse


def command_parse(python_dict, fifo_queue, thread_lock):  # pylint: disable=inconsistent-return-statements
    """Function to get and parse commands from devices

    :type python_dict: Dict
    :param python_dict: A dictionary of connection data
    :type fifo_queue: queue.Queue Object
    :param fifo_queue: The FIFO queue
    :type thread_lock: threading.Lock Object
    :param thread_lock: The thread lock

    :rtype: None
    :returns: None, but it does put a item in the fifo_queue

    """
    with thread_lock:
        allowed_device_types = {'ios', 'iosxe', 'iosxr', 'nxos'}

        if python_dict.get('device_type') not in allowed_device_types:
            return None

        command = python_dict.get('command')

        netmiko_obj = QuickNetmiko(python_dict.get('device_ip_name'), python_dict.get('device_type'),
                                   python_dict.get('username'), python_dict.get('password'))

        command_result = netmiko_obj.send_commands(command)

        genie_parse_obj = GenieCommandParse(python_dict.get('device_type'))

        parse_result = genie_parse_obj.parse_string(command, command_result)

        fifo_queue.put((parse_result, command_result))
