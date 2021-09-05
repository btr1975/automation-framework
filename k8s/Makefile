SHELL := /bin/bash
# This Makefile is to run k8s for the framework
# Author: Benjamin P. Trachtenberg
# Version: 2021.9.5.001
#

.PHONY: all clean \
        apply_vault-with-lb delete_vault-with-lb apply_vault-with-nodeport

all: deploy_all

apply_vault-with-lb:
	(cd vault-latest-lb && microk8s kubectl apply -f .)

delete_vault-with-lb:
	(cd vault-latest-lb && microk8s kubectl delete -f .)

apply_vault-with-nodeport:
	(cd vault-latest-nodeport && microk8s kubectl apply -f .)

delete_vault-with-nodeport:
	(cd vault-latest-nodeport && microk8s kubectl delete -f .)
