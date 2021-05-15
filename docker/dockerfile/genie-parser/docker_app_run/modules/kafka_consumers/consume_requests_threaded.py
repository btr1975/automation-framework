import json
import hashlib
import platform
import os
import sys
import queue
import threading
from confluent_kafka import Consumer
from modules.kafka_producers import produce_results
from modules.command_parse import command_parse
from modules.vault_lib import VaultConnection


def consume_requests_threaded():
    # Create consumer object with optional values
    c = Consumer({
        'bootstrap.servers': 'broker-1:9092,broker-2:9093,broker-3:9094',
        'group.id': 'genie.runners',
        'auto.offset.reset': 'beginning',
        'client.id': platform.node(),
    })

    # Subscribe to topics to listen to
    c.subscribe(['genie.runners.requests'])

    # Create a FIFO queue for threading
    fifo_queue = queue.Queue()

    # Create a thread lock object so only 1 secondary thread runs at a time
    thread_lock = threading.Lock()

    try:
        # Begin infinite loop to check for new messages
        while True:
            # Poll every second
            msg = c.poll(1.0)

            # If the message is empty move to next iteration
            if msg is None:
                continue

            # If their is a message error print it, and move to next iteration
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            # Receive message if there is one, and if there is no error
            python_data = json.loads(msg.value().decode('utf-8'))

            # Check to see if key destination-host = genie-runners
            if python_data.get('destination-host') == 'genie.runners':
                print("Hey I'm a genie.runner")
                print('Key = {}'.format(msg.key().decode("utf-8")))
                print('Hash of value is: {}'.format(hashlib.sha224(msg.value()).hexdigest()))
                if msg.key().decode("utf-8") == hashlib.sha224(msg.value()).hexdigest():
                    print('MATCHED HASH')

                # Lookup login credentials from HashiCopr Vault
                print('----- Looking up credentials in HashiCorp Vault -----')
                vault_obj = VaultConnection(protocol=os.getenv('VAULT_PROTOCOL'), host=os.getenv('VAULT_HOST'),
                                            token=os.getenv('VAULT_TOKEN'), port=int(os.getenv('VAULT_PORT')),
                                            ssl_verify=bool(os.getenv('VAULT_SSL_VERIFY')))

                vault_response = vault_obj.get_kv_v1_value(os.getenv('VAULT_KV_PATH'))

                print('----- Lookup complete -----')

                # Add username and password to request
                python_data['username'] = vault_response.get('data').get('username')
                python_data['password'] = vault_response.get('data').get('password')

                print('----- Start new thread for command get -----')
                threading.Thread(target=command_parse, args=(python_data, fifo_queue, thread_lock)).start()

            else:
                print('This is not for genie.runners, nothing to do.')

            # Check if there is something in the queue to send
            if fifo_queue.qsize() > 0:
                print('----- Queue Size is {} -----'.format(fifo_queue.qsize()))
                command_result_dict = 0
                command_result_raw = 1

                # Get 1 item from the queue
                queue_data = fifo_queue.get()

                # Create the results dict
                send_dict = {'result': queue_data[command_result_dict],
                             'result_raw': queue_data[command_result_raw],
                             'original_hash': '{}'.format(msg.key().decode("utf-8"))}

                # Update the results dict with the original python_data
                send_dict.update(python_data)

                print('----- Producing results -----')
                produce_results(send_dict)

    except KeyboardInterrupt as e:
        c.close()
        sys.exit(e)
