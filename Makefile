# This Makefile is to run the frameworks
# Author: Benjamin P. Trachtenberg
# Version: 2021.5.16.001
#

.PHONY: all clean deploy_framework check_framework_running check_framework_replicas remove_framework \
        remove_volumes build_genie_parser check_stats

all: deploy_framework

deploy_framework:
	docker stack deploy -c ./docker/stack/full-framework.yml automation-framework

check_framework_running:
	docker stack ps automation-framework

check_framework_replicas:
	docker stack services automation-framework

check_stats:
	docker stats

remove_framework:
	docker stack rm automation-framework

remove_volumes:
	docker volume rm automation-framework_vault-file
	docker volume rm automation-framework_vault-logs
	docker volume rm automation-framework_nautobot-redis
	docker volume rm automation-framework_nautobot-postgres

build_genie_parser:
	docker-compose -f docker/compose/docker-compose-rh-parser.yml build

clean: remove_framework
