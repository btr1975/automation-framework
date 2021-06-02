import platform
import datetime
import sys
from confluent_kafka import Consumer
from confluent_kafka import Producer
from .produce_records import ProduceRecords
from .util import msg_value_to_dict, get_python_dict_hash_sha256, msg_key_to_string


def consume_requests(callback=None):
    producer = Producer({
        'bootstrap.servers': 'broker-1:9092,broker-2:9093,broker-3:9094'
    })
    producer_logs = Producer({
        'bootstrap.servers': 'broker-1:9092,broker-2:9093,broker-3:9094'
    })

    c = Consumer({
        'bootstrap.servers': 'broker-1:9092,broker-2:9093,broker-3:9094',
        'group.id': 'genie.runners',
        'auto.offset.reset': 'beginning',
        'client.id': platform.node(),
    })

    c.subscribe(['genie.runners.requests'])

    produce_results = ProduceRecords(producer, topic='genie.runners.requests.results')
    produce_logs = ProduceRecords(producer_logs, topic='automation.logs')

    try:
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print(' LOG '.center(75, '-'))
            print('')
            print(f'Received message: {msg_value_to_dict(msg)}')
            python_data = msg_value_to_dict(msg)

            if python_data.get('destination-host') == 'genie.runners':
                print("Hey I'm a genie.runner")
                print(f'Key = {msg_key_to_string(msg)}')
                print(f'Hash of value is: {get_python_dict_hash_sha256(python_data)}')
                if msg_key_to_string(msg) == get_python_dict_hash_sha256(python_data):
                    print('MATCHED HASH')
                if callback:
                    command_result__dict = callback(python_data)
                    send_dict = {'result': command_result__dict,
                                 'original_hash': f'{msg_key_to_string(msg)}',
                                 'timestamp': str(datetime.datetime.now(datetime.timezone.utc)),
                                 'replier': 'some_name',
                                 'original_request': python_data,
                                 'other_receivers': ['interface-checks', 'forwarding-checks'],
                                 }

                    produce_results.produce_rerecords(send_dict)
                    logs_record = {
                        'key': 'special_key',
                               'value': {'timestamp': str(datetime.datetime.now(datetime.timezone.utc)),
                                         'container': 'genie-parser',
                                         'actions': 'Did some stuff'}
                    }

                    produce_logs.produce_rerecords(logs_record)

            else:
                logs_record = {
                    'key': 'special_key',
                    'value': {'timestamp': str(datetime.datetime.now(datetime.timezone.utc)),
                              'container': 'genie-parser',
                              'actions': 'This is not for genie.runners, nothing to do.'}
                }
                produce_logs.produce_rerecords(logs_record)
                print('This is not for genie.runners, nothing to do.')

    except KeyboardInterrupt as e:
        c.close()
        sys.exit(e)
