"""
This is used to connect to HashiCorp Vault

"""
import json
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import socket
from .util.exceptions import ProtocolError


class VaultConnectionBase:
    """
    Class for base needs for HashiCorp Vault

    :type protocol: String
    :param protocol: The protocol to use options are {'http', 'https'}
    :type host: String
    :param host: The Vault server name or ip address
    :type token: String
    :param token: The vault token
    :type port: Integer
    :param port: The port number to use default: 8200
    :type ssl_verify: Boolean
    :param ssl_verify: Verify SSL Certificates default: True

    :rtype: None
    :return: None

    :raises ProtocolError: If protocol is not one of these {'http', 'https'}
    :raises TypeError: If host is not a string
    :raises TypeError: If token is not a string
    :raises TypeError: If port is not a integer
    :raises TypeError: If ssl_verify is not a boolean

    """

    def __init__(self, protocol, host, token, port=8200, ssl_verify=True):
        if protocol not in {'http', 'https'}:
            raise ProtocolError("'protocol' must be one of the following {'http', 'https'}")

        if not isinstance(host, str):
            raise TypeError("'host' must be of type string but received a {}".format(type(host)))

        if not isinstance(token, str):
            raise TypeError("'token' must be of type string but received a {}".format(type(token)))

        if not isinstance(port, int):
            raise TypeError("'port' must be of type integer but received a {}".format(type(port)))

        if not isinstance(ssl_verify, bool):
            raise TypeError("'ssl_verify' must be of type boolean but received a {}".format(type(ssl_verify)))

        if not ssl_verify:
            urllib3.disable_warnings(category=InsecureRequestWarning)

        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'X-Vault-Token': '{token}'.format(token=token)}

        self.protocol = protocol
        self.ssl_verify = ssl_verify

        self.base_vault_url = '{protocol}://{host}:{port}/'.format(protocol=protocol, host=host, port=port)

    @staticmethod
    def print_pretty_json(json_data):
        """Method to print response JSON real pretty like

        :type json_data: Dict
        :param json_data: JSON Data

        :rtype: None
        :return: None it prints pretty JSON

        """
        print(json.dumps(json_data, sort_keys=True, indent=4))

    def _post(self, url, json_data=None, params=None):
        """Protected method to send a post request

        :type url: String
        :param url: The URL to sent the request to
        :type json_data: Dict or None
        :param json_data: A dictionary of JSON data, default is None
        :type params: Dict or None
        :param params: A dictionary of params, default is None

        :rtype: <class 'requests.models.Response'>
        :return: requests Response Object

        :raises TypeError: If json_data is not a dictionary if json_data is given
        :raises TypeError: If params is not a dictionary if params is given

        """
        response = None

        if json_data:
            self.__verify_json_data(json_data)

        if params:
            self.__verify_params(params)

        if self.protocol == 'http':
            response = requests.post(url, headers=self.headers, json=json_data, params=params)

        elif self.protocol == 'https':
            response = requests.post(url, headers=self.headers, json=json_data, params=params, verify=self.ssl_verify)

        return response

    def _get(self, url, json_data=None, params=None):
        """Protected method to send a get request

        :type url: String
        :param url: The URL to sent the request to
        :type json_data: Dict or None
        :param json_data: A dictionary of JSON data, default is None
        :type params: Dict or None
        :param params: A dictionary of params, default is None

        :rtype: <class 'requests.models.Response'>
        :return: requests Response Object

        :raises TypeError: If json_data is not a dictionary if json_data is given
        :raises TypeError: If params is not a dictionary if params is given

        """
        response = None

        if json_data:
            self.__verify_json_data(json_data)

        if params:
            self.__verify_params(params)

        if self.protocol == 'http':
            response = requests.get(url, headers=self.headers, json=json_data, params=params)

        elif self.protocol == 'https':
            response = requests.get(url, headers=self.headers, json=json_data, params=params, verify=self.ssl_verify)

        return response

    def __verify_json_data(self, json_data):
        """Private method to verify json_data is a dictionary

        :type json_data: Dict
        :param json_data: Dict of data

        :rtype: None
        :return: None it verifies if the data is of type dictionary

        :raises TypeError: If json_data is not a dictionary

        """
        if not isinstance(json_data, dict):
            raise TypeError('json_data must be a dictionary but received a {}'.format(type(json_data)))

    def __verify_params(self, params):
        """Private method to verify params is a dictionary

        :type params: Dict
        :param params: Dict of data

        :rtype: None
        :return: None it verifies if the data is of type dictionary

        :raises TypeError: If params is not a dictionary

        """
        if not isinstance(params, dict):
            raise TypeError('params must be a dictionary but received a {}'.format(type(params)))


class VaultConnection(VaultConnectionBase):

    def __init__(self, protocol, host, token, port=8200, ssl_verify=True):
        super().__init__(protocol, host, token, port, ssl_verify)

    def get_kv_v1_value(self, path):
        """Method to get KeyValue v1 store

        :type path: String
        :param path: The KeyValue store path

        :rtype: Dict
        :return: A Dictionary of response JSON Data

        """
        url = '{base_url}v1/{path}'.format(base_url=self.base_vault_url, path=path)
        return self._get(url).json()
