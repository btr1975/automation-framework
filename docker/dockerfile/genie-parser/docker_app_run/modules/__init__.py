"""
init for the modules module
"""
from .kafka_consumers import consume_requests, consume_results, consume_requests_threaded
from .kafka_producers import produce_results, produce_requests
from .vault_lib import VaultConnection
