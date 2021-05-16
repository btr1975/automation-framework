# This Makefile is to run compose for the framework
# Author: Benjamin P. Trachtenberg
# Version: 2021.5.16.001
#

.PHONY: all clean \
        deploy_nautobot start_nautobot stop_nautobot rm_nautobot remove_nautobot_volumes \
        deploy_elk start_elk stop_elk  rm_elk \
        deploy_vault start_vault stop_vault rm_vault remove_vault_volumes \
        deploy_kafka start_kafka stop_kafka  rm_kafka \
        deploy_rh_parser start_rh_parser stop_rh_parser rm_rh_parser \
        deploy_mogodb start_mogodb stop_mogodb rm_mogodb remove_mogodb_volumes \
        check_volumes \
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

deploy_mogodb:
	docker-compose -f docker-compose-mongo-latest.yml up -d

start_mogodb:
	docker-compose -f docker-compose-mongo-latest.yml start

stop_mogodb:
	docker-compose -f docker-compose-mongo-latest.yml stop

rm_mogodb:
	docker-compose -f docker-compose-mongo-latest.yml rm

remove_mogodb_volumes:
	docker volume rm compose_mongo-data-db-compose
	docker volume rm compose_mongo-data-configdb-compose

check_stats:
	docker stats

check_volumes:
	docker volume ls

clean: stop_all rm_all
