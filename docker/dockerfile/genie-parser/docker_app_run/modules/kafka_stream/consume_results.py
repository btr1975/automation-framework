import json
import hashlib
import sys
import platform
from confluent_kafka import Consumer


def consume_results():
    c = Consumer({
        'bootstrap.servers': 'broker-1:9092,broker-2:9093,broker-3:9094',
        'group.id': 'genie.runner.users',
        'auto.offset.reset': 'beginning',
        'client.id': platform.node(),
    })

    c.subscribe(['genie.runners.requests.results'])

    message_count = 1

    try:
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            # Retrieve message
            python_data = json.loads(msg.value().decode('utf-8'))

            if python_data.get('destination-host') == 'genie.runners':
                print('-------------------------- Message {} --------------------------'.format(message_count))
                print("Hey I'm a genie.runner.users")
                print('Key = {}'.format(msg.key().decode("utf-8")))
                print('Hash of value is: {}'.format(hashlib.sha224(msg.value()).hexdigest()))
                if msg.key().decode("utf-8") == hashlib.sha224(msg.value()).hexdigest():
                    print('MATCHED HASH')

                message_count += 1

            else:
                print('-------------------------- Message {} --------------------------'.format(message_count))
                print('This is not for genie.runners.users, nothing to do.')
                message_count += 1

            print(python_data)

    except KeyboardInterrupt as e:
        c.close()
        sys.exit(e)
