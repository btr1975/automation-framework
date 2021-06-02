"""
Class to get data from HashiCorp Vault
"""
import hvac


HVAC_URL = 'http://10.0.0.101:8200'
HVAC_TOKEN = 's.VeIER2pQZ6oHPdFNauVAYSUc'
HVAC_PATH = 'test'


class VaultDataKv2:

    def __init__(self, url=HVAC_URL, token=HVAC_TOKEN, path=HVAC_PATH):
        self.client = hvac.Client(url=url, token=token)
        self.path = path

    def __read_secret_version(self, version=None):
        if version:
            return self.client.secrets.kv.v2.read_secret_version(path=self.path, version=version)

        else:
            return self.client.secrets.kv.v2.read_secret_version(path=self.path)

    def get_latest_keys(self):
        return self.__read_secret_version()['data']['data'].keys()

    def get_latest_data(self):
        return self.__read_secret_version()['data']['data']

    def get_latest_created(self):
        return self.__read_secret_version()['data']['metadata']['created_time']

    def get_latest_version(self):
        return self.__read_secret_version()['data']['metadata']['version']

    def get_version_keys(self, version):
        return self.__read_secret_version(version)['data']['data'].keys()

    def get_version_data(self, version):
        return self.__read_secret_version(version)['data']['data']

    def get_version_created(self, version):
        return self.__read_secret_version(version)['data']['metadata']['created_time']
