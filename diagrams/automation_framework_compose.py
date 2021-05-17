from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.security import Vault
from diagrams.onprem.network import Zookeeper
from diagrams.onprem.queue import Kafka
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.elastic.elasticsearch import Kibana
from diagrams.elastic.elasticsearch import Logstash
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.onprem.database import Mongodb


def main():
    graph_attr = {
        "fontsize": "45",
        'overlap_scaling': '100',
        'size': '24!',
        'ratio': 'expand'
    }

    with Diagram(name='Automation Framework Compose', direction='LR', graph_attr=graph_attr):
        with Cluster('Docker Cluster'):
            docker = Docker('Docker')

            with Cluster('container1'):
                python_container = Python('APIs\nOther Microservices')

            with Cluster('BatFish'):
                batfish_container = Custom('BatFish\ntcp:8888\ntcp:9997\ntcp:9996', 'custom_icons/BatFish.png')

        with Cluster('Kafka Cluster'):
            with Cluster('Zookeeper'):
                Zookeeper('Zookeeper\ntcp:2181')

            with Cluster('REST Proxy'):
                rest_proxy = Custom('REST Proxy\ntcp:8082', 'custom_icons/REST-API.png')

            with Cluster('Control Center'):
                control_center = Kafka('Control Center\ntcp:9021')

            with Cluster('Schema Registry'):
                schema_registry = Storage('Schema Registry\ntcp:8081')

            with Cluster('Brokers'):
                broker_1 = Kafka('Broker 1\ntcp:9092')
                kafka_brokers = [
                    broker_1,
                    Kafka('Broker 2\ntcp:9093'),
                    Kafka('Broker 3\ntcp:9094')
                ]

        with Cluster('Secrets Managers'):
            vault = Vault('HashiCorp Vault\ntcp:8200')
            secrets_managers = [
                vault,
            ]

        with Cluster('Logging and Search'):
            with Cluster('Search and Logging'):
                elastic_search = Elasticsearch('Elastic Search\ntcp:9200')
                kibana = Kibana('Kibana\ntcp:5601')
                logstash = Logstash('Logstash\ntcp:5044')
                search_log = [
                    elastic_search,
                    kibana,
                    logstash
                ]

        with Cluster('Inventory and Connectivity'):
            with Cluster('Inventory'):
                nautobot = Custom('Nautobot\ntcp:8000', 'custom_icons/Nautobot.jpeg')

        with Cluster('Database'):
            with Cluster('Mongo dB'):
                mongodb = Mongodb('MongoDb\ntcp:27017')
                mongodb_express = Mongodb('MongoDb Express\ntcp:8081')
                mongo_group = [
                    mongodb,
                    mongodb_express
                ]

        kafka_brokers - python_container

        python_container - vault

        python_container - nautobot

        nautobot - logstash
        python_container - logstash

        python_container - mongodb


if __name__ == '__main__':
    main()
