"""
Main running app for the container non-threaded
mostly for testing

"""
from quick_netmiko import QuickNetmiko
from pyats_genie_command_parse import GenieCommandParse
from modules import consume_requests, VaultDataKv2


def docker_app_run(python_dict):
    """Function to get and parse commands from devices

    :type python_dict: Dict
    :param python_dict: A dictionary of connection data

    :rtype: (Dict, String)
    :returns:A tuple of a Dict and a String

    """
    allowed_device_types = {'ios', 'iosxe', 'iosxr', 'nxos'}

    if python_dict.get('device_type') not in allowed_device_types:
        return None

    vault = VaultDataKv2()

    command = python_dict.get('command')

    netmiko_obj = QuickNetmiko(python_dict.get('device_ip_name'), python_dict.get('device_type'),
                               vault.get_latest_data().get('username'), vault.get_latest_data().get('password'))

    command_result = netmiko_obj.send_commands(command)

    genie_parse_obj = GenieCommandParse(python_dict.get('device_type'))

    parse_result = genie_parse_obj.parse_string(command, command_result)

    return parse_result


consume_requests(docker_app_run)
