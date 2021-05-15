"""
This is for vault_lib custom exceptions

"""


class ProtocolError(Exception):
    """Exception for protocol Exceptions

    :type value: String
    :param value: The message you want to emit

    """
    def __init__(self, value):  # pylint: disable=super-init-not-called
        self.value = '{}'.format(value)

    def __str__(self):
        return repr(self.value)
