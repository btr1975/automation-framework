import json
import hashlib


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def send_single_record(producer, topic, data, callback):
    # Trigger any available delivery report callbacks from previous produce() calls
    producer.poll(0)

    json_data = json.dumps(data)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    producer.produce(topic=topic, key='{}'.format(hashlib.sha224(json_data.encode('utf-8')).hexdigest()),
                     value=json_data.encode('utf-8'), callback=callback)


def send_list_of_records(producer, topic, data_list, callback):
    for data in data_list:
        if not isinstance(data, dict):
            raise TypeError('data must be a dict, but received a {}!!'.format(type(data)))

        send_single_record(producer, topic, data, callback)


def send_records(producer=None, topic=None, records=None, callback=None):
    if isinstance(records, list):
        send_list_of_records(producer, topic, records, callback)

    elif isinstance(records, dict):
        send_single_record(producer, topic, records, callback)

    else:
        raise TypeError('records must be a list or a dict, but received a {}!!'.format(type(records)))
