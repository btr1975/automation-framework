import platform
import os
import sys
import queue
import threading
from confluent_kafka import Consumer
from confluent_kafka import Producer
from .produce_records import ProduceRecords
from .util import msg_value_to_dict, get_python_dict_hash_sha256, msg_key_to_string
from modules.command_parse import command_parse
from modules.vault_lib import VaultDataKv2


def consume_requests_threaded():
    producer = Producer({
        'bootstrap.servers': 'broker-1:9092,broker-2:9093,broker-3:9094'
    })
    # Create consumer object with optional values
    c = Consumer({
        'bootstrap.servers': 'broker-1:9092,broker-2:9093,broker-3:9094',
        'group.id': 'genie.runners',
        'auto.offset.reset': 'beginning',
        'client.id': platform.node(),
    })

    # Subscribe to topics to listen to
    c.subscribe(['genie.runners.requests'])

    # Set up producer
    produce_results = ProduceRecords(producer, topic='genie.runners.requests.results')

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
            python_data = msg_value_to_dict(msg)

            # Check to see if key destination-host = genie-runners
            if python_data.get('destination-host') == 'genie.runners':
                print("Hey I'm a genie.runner")
                print(f'Key = {msg_key_to_string(msg)}')
                print(f'Hash of value is: {get_python_dict_hash_sha256(python_data)}')
                if msg_key_to_string(msg) == get_python_dict_hash_sha256(python_data):
                    print('MATCHED HASH')

                # Lookup login credentials from HashiCopr Vault
                print('----- Looking up credentials in HashiCorp Vault -----')
                vault_obj = VaultDataKv2()

                print('----- Lookup complete -----')

                # Add username and password to request
                python_data['username'] = vault_obj.get_latest_data().get('username')
                python_data['password'] = vault_obj.get_latest_data().get('password')

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
                produce_results.produce_rerecords(send_dict)

    except KeyboardInterrupt as e:
        c.close()
        sys.exit(e)
