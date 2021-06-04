import json
import re
import requests


class DockerRegistryApi:
    """Class to easily get Docker registry data

    :type host: String
    :param host: Registry to connect to
    :type port: Integer
    :param port: The port to connect to

    :rtype: None
    :returns: None

    :raises ValueError: If host does not match regex
    :raises TypeError: If port is not an integer
    """
    host_regex = re.compile(r'^(http|https)://\S+$')

    def __init__(self, host, port=5000):
        if not self.host_regex.match(host):
            raise ValueError('"host" must be in the following format "^(http|https)://\\S+$" ')

        if not isinstance(port, int):
            raise TypeError(f'"port" must be of type integer but received a {type(port)}')

        self.server_url = f'{host}:{port}/v2'
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get_catalog(self):
        """Method to get the registry catalog

        :rtype: Dict
        :returns: JSON Response

        :raises Exception: If errors happen
        """
        response = requests.get(f'{self.server_url}/_catalog', headers=self.headers)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def get_repository_tags(self, name):
        """Method to get the repository tags

        :type name: String
        :param name: The name of the repository

        :rtype: Dict
        :returns: JSON Response

        :raises Exception: If errors happen
        """
        response = requests.get(f'{self.server_url}/{name}/tags/list', headers=self.headers)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def get_all_repository_tags(self):
        """Method to get the repository tags

        :rtype: List
        :returns: List of JSON Responses

        :raises Exception: If errors happen
        """
        temp_list = list()
        if self.get_catalog().get('repositories'):
            for name in self.get_catalog().get('repositories'):
                temp_list.append(self.get_repository_tags(name))

        return temp_list

    def get_repository_manifest(self, name, tag):
        """Method to get the repository manifest

        :type name: String
        :param name: The name of the repository
        :type tag: String
        :param tag: The tag to use

        :rtype: Dict
        :returns: JSON Response

        :raises Exception: If errors happen
        """
        response = requests.get(f'{self.server_url}/{name}/manifests/{tag}', headers=self.headers)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    @staticmethod
    def print_pretty_json(json_data):  # pragma: no cover
        """Method to print response JSON real pretty like

        :type json_data: Dict
        :param json_data: JSON Data in a dictionary

        :rtype: None
        :return: prints pretty JSON
        """
        print(json.dumps(json_data, sort_keys=True, indent=4))

    @staticmethod
    def get_pretty_json(json_data):  # pragma: no cover
        """Method to get response JSON real pretty like

        :type json_data: Dict
        :param json_data: JSON Data in a dictionary

        :rtype: String
        :return: pretty JSON
        """
        return json.dumps(json_data, sort_keys=True, indent=4)


if __name__ == '__main__':
    obj_a = DockerRegistryApi('http://10.0.0.101')
    obj_a.print_pretty_json(obj_a.get_catalog())
    obj_a.print_pretty_json(obj_a.get_all_repository_tags())
    obj_a.print_pretty_json(obj_a.get_repository_manifest('nso-teamcity', 'latest'))
