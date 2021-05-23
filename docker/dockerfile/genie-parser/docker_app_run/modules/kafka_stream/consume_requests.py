import json
import hashlib
import platform
import datetime
import sys
from confluent_kafka import Consumer
from confluent_kafka import Producer
from .produce_records import ProduceRecords


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
            print('Received message: {}'.format(msg.value().decode('utf-8')))
            python_data = json.loads(msg.value().decode('utf-8'))

            if python_data.get('destination-host') == 'genie.runners':
                print("Hey I'm a genie.runner")
                print('Key = {}'.format(msg.key().decode('utf-8')))
                print('Hash of value is: {}'.format(hashlib.sha256(msg.value()).hexdigest()))
                if msg.key().decode("utf-8") == hashlib.sha256(msg.value()).hexdigest():
                    print('MATCHED HASH')
                if callback:
                    command_result__dict = callback(python_data)
                    send_dict = {'result': command_result__dict,
                                 'original_hash': '{}'.format(msg.key().decode("utf-8")),
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
