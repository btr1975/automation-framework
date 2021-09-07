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
from diagrams.onprem.database import Influxdb
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.ci import TC


def main():
    graph_attr = {
        "fontsize": "45",
        'overlap_scaling': '100',
        'size': '24!',
        'ratio': 'expand'
    }

    with Diagram(name='Automation Framework Kubernetes', direction='LR', graph_attr=graph_attr):
        with Cluster('Docker Cluster'):
            docker = Docker('Docker')

            with Cluster('container1'):
                python_container = Python('APIs\nOther Microservices')

            with Cluster('Docker Registry'):
                docker_registry_container = Docker('Docker Registry\ntcp:5000')

            with Cluster('Docker Registry Browser'):
                docker_registry_browser_container = Python('Docker Registry Browser\ntcp:8088')

            with Cluster('BatFish'):
                batfish_container = Custom('BatFish\ntcp:8888\ntcp:9997\ntcp:9996', 'custom_icons/BatFish.png')

        with Cluster('Secrets Managers'):
            vault = Vault('HashiCorp Vault\ntcp:8200')
            secrets_managers = [
                vault,
            ]

        with Cluster('Logging and Search'):
            with Cluster('ELK Stack'):
                elastic_search = Elasticsearch('Elastic Search\ntcp:9200')
                kibana = Kibana('Kibana\ntcp:5601')
                logstash = Logstash('Logstash\ntcp:5044')
                search_log = [
                    elastic_search,
                    kibana,
                    logstash
                ]

            with Cluster('Influxdb'):
                infulxdb = Influxdb('Influxdb\ntcp:8086')

            with Cluster('Grafana'):
                grafana = Grafana('Grafana\ntcp:3000')

        with Cluster('Database'):
            with Cluster('Mongo dB'):
                mongodb = Mongodb('MongoDb\ntcp:27017')
                mongodb_express = Mongodb('MongoDb Express\ntcp:8181')
                mongo_group = [
                    mongodb,
                    mongodb_express
                ]

        with Cluster('CI/CD'):
            team_city = TC('TeamCity')


        python_container - vault

        python_container - logstash

        python_container - infulxdb

        python_container - mongodb


if __name__ == '__main__':
    main()
