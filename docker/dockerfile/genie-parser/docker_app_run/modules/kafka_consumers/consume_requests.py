import json
import hashlib
import platform
import sys
from confluent_kafka import Consumer
from modules.kafka_producers import produce_results


def consume_requests(callback=None):
    c = Consumer({
        'bootstrap.servers': 'broker-1:9092,broker-2:9093,broker-3:9094',
        'group.id': 'genie.runners',
        'auto.offset.reset': 'beginning',
        'client.id': platform.node(),
    })

    c.subscribe(['genie.runners.requests'])

    try:
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print('Received message: {}'.format(msg.value().decode('utf-8')))
            python_data = json.loads(msg.value().decode('utf-8'))

            if python_data.get('destination-host') == 'genie.runners':
                print("Hey I'm a genie.runner")
                print('Key = {}'.format(msg.key().decode("utf-8")))
                print('Hash of value is: {}'.format(hashlib.sha224(msg.value()).hexdigest()))
                if msg.key().decode("utf-8") == hashlib.sha224(msg.value()).hexdigest():
                    print('MATCHED HASH')
                if callback:
                    command_result__dict, command_result_raw = callback(python_data)
                    send_dict = {'result': command_result__dict,
                                 'result_raw': command_result_raw,
                                 'original_hash': '{}'.format(msg.key().decode("utf-8"))}
                    send_dict.update(python_data)

                    produce_results(send_dict)

            else:
                print('This is not for genie.runners, nothing to do.')

    except KeyboardInterrupt as e:
        c.close()
        sys.exit(e)
