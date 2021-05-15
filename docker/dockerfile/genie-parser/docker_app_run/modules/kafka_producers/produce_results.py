from confluent_kafka import Producer
from .produce_util import delivery_report, send_records


def produce_results(records):
    producer = Producer({'bootstrap.servers': 'broker-1:9092,broker-2:9093,broker-3:9094'})

    send_records(producer=producer, topic='genie.runners.requests.results', records=records, callback=delivery_report)

    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
    producer.flush()
