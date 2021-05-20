# This Makefile is to run compose for the framework
# Author: Benjamin P. Trachtenberg
# Version: 2021.5.20.001
#

.PHONY: all clean \
        deploy_nautobot start_nautobot stop_nautobot rm_nautobot remove_nautobot_volumes \
        deploy_elk start_elk stop_elk  rm_elk \
        deploy_vault start_vault stop_vault rm_vault remove_vault_volumes \
        deploy_kafka start_kafka stop_kafka  rm_kafka \
        deploy_rh_parser start_rh_parser stop_rh_parser rm_rh_parser \
        deploy_mongodb start_mongodb stop_mongodb rm_mongodb remove_mongodb_volumes \
        deploy_batfish start_batfish stop_batfish rm_batfish remove_batfish_volumes \
        deploy_influxdb start_influxdb stop_influxdb rm_influxdb remove_influxdb_volumes \
        deploy_grafana start_grafana stop_grafana rm_grafana \
        check_volumes check_running \
        deploy_all start_all stop_all rm_all

all: deploy_all

deploy_all: deploy_nautobot deploy_elk deploy_rh_parser deploy_kafka deploy_vault

start_all: start_nautobot start_elk start_kafka start_rh_parser start_vault

stop_all: stop_nautobot stop_elk stop_kafka stop_rh_parser stop_vault

rm_all: rm_nautobot rm_elk rm_kafka rm_rh_parser rm_vault

remove_all_volumes: remove_nautobot_volumes remove_vault_volumes

deploy_nautobot:
	docker-compose -f docker-compose-nautobot-latest.yml up -d

start_nautobot:
	docker-compose -f docker-compose-nautobot-latest.yml start

stop_nautobot:
	docker-compose -f docker-compose-nautobot-latest.yml stop

rm_nautobot:
	docker-compose -f docker-compose-nautobot-latest.yml rm

remove_nautobot_volumes:
	docker volume rm compose_nautobot-postgres-compose
	docker volume rm compose_nautobot-redis-compose

deploy_elk:
	docker-compose -f docker-compose-elk-stack-latest.yml up -d

start_elk:
	docker-compose -f docker-compose-elk-stack-latest.yml start

stop_elk:
	docker-compose -f docker-compose-elk-stack-latest.yml stop

rm_elk:
	docker-compose -f docker-compose-elk-stack-latest.yml rm

deploy_vault:
	docker-compose -f docker-compose-vault-latest.yml up -d

start_vault:
	docker-compose -f docker-compose-vault-latest.yml start

stop_vault:
	docker-compose -f docker-compose-vault-latest.yml stop

rm_vault:
	docker-compose -f docker-compose-vault-latest.yml rm

remove_vault_volumes:
	docker volume rm compose_vault-file-compose
	docker volume rm compose_vault-logs-compose

deploy_kafka:
	docker-compose -f docker-compose-kafka-latest.yml up -d

start_kafka:
	docker-compose -f docker-compose-kafka-latest.yml start

stop_kafka:
	docker-compose -f docker-compose-kafka-latest.yml stop

rm_kafka:
	docker-compose -f docker-compose-kafka-latest.yml rm

deploy_rh_parser:
	docker-compose -f docker-compose-rh-parser.yml up -d

start_rh_parser:
	docker-compose -f docker-compose-rh-parser.yml start

stop_rh_parser:
	docker-compose -f docker-compose-rh-parser.yml stop

rm_rh_parser:
	docker-compose -f docker-compose-rh-parser.yml rm

deploy_mongodb:
	docker-compose -f docker-compose-mongo-latest.yml up -d

start_mongodb:
	docker-compose -f docker-compose-mongo-latest.yml start

stop_mongodb:
	docker-compose -f docker-compose-mongo-latest.yml stop

rm_mongodb:
	docker-compose -f docker-compose-mongo-latest.yml rm

remove_mongodb_volumes:
	docker volume rm compose_mongo-data-db-compose
	docker volume rm compose_mongo-data-configdb-compose

deploy_batfish:
	docker-compose -f docker-compose-batfish-latest.yml up -d

start_batfish:
	docker-compose -f docker-compose-batfish-latest.yml start

stop_batfish:
	docker-compose -f docker-compose-batfish-latest.yml stop

rm_batfish:
	docker-compose -f docker-compose-batfish-latest.yml rm

remove_batfish_volumes:
	docker volume rm compose_batfish-data-compose

deploy_influxdb:
	docker-compose -f docker-compose-influxdb-2.0.4.yml up -d

start_influxdb:
	docker-compose -f docker-compose-influxdb-2.0.4.yml start

stop_influxdb:
	docker-compose -f docker-compose-influxdb-2.0.4.yml stop

rm_influxdb:
	docker-compose -f docker-compose-influxdb-2.0.4.yml rm

remove_influxdb_volumes:
	docker volume rm compose_influxdb-var-lib-influxdb2-compose
	docker volume rm compose_influxdb-etc-influxdb2-compose

deploy_grafana:
	docker-compose -f docker-compose-grafana-latest.yml up -d

start_grafana:
	docker-compose -f docker-compose-grafana-latest.yml start

stop_grafana:
	docker-compose -f docker-compose-grafana-latest.yml stop

rm_grafana:
	docker-compose -f docker-compose-grafana-latest.yml rm

check_stats:
	docker stats

check_running:
	docker ps

check_volumes:
	docker volume ls

clean: stop_all rm_all
