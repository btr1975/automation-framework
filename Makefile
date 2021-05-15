# This Makefile is to run the frameworks
# Author: Benjamin P. Trachtenberg
# Version: 2021.5.14.001
#

.PHONY: all clean deploy_framework check_framework_running check_framework_replicas remove_framework \
        remove_volumes build_genie_parser

all: deploy_framework

deploy_framework:
	docker stack deploy -c ./docker/stack/full-framework.yml e-trade-framework

check_framework_running:
	docker stack ps e-trade-framework

check_framework_replicas:
	docker stack services e-trade-framework

remove_framework:
	docker stack rm e-trade-framework

remove_volumes:
	docker volume rm e-trade-framework_vault-file
	docker volume rm e-trade-framework_vault-logs

build_genie_parser:
	docker-compose -f docker/compose/docker-compose-rh-parser.yml build

clean: remove_framework
