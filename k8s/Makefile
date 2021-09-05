SHELL := /bin/bash
# This Makefile is to run k8s for the framework
# Author: Benjamin P. Trachtenberg
# Version: 2021.9.5.001
#

.PHONY: all clean \
        apply_vault-with-lb delete_vault-with-lb apply_vault-with-nodeport \
        apply_batfish-with-lb delete_batfish-with-lb apply_batfish-with-nodeport delete_batfish-with-nodeport \
        apply_elk-with-lb delete_elk-with-lb apply_elk-with-nodeport delete_elk-with-nodeport \
        apply_grafana-with-lb delete_grafana-with-lb apply_grafana-with-nodeport delete_grafana-with-nodeport

all: deploy_all

apply_vault-with-lb:
	(cd vault-latest-lb && microk8s kubectl apply -f .)

delete_vault-with-lb:
	(cd vault-latest-lb && microk8s kubectl delete -f .)

apply_vault-with-nodeport:
	(cd vault-latest-nodeport && microk8s kubectl apply -f .)

delete_vault-with-nodeport:
	(cd vault-latest-nodeport && microk8s kubectl delete -f .)

apply_batfish-with-lb:
	(cd batfish-latest-lb && microk8s kubectl apply -f .)

delete_batfish-with-lb:
	(cd batfish-latest-lb && microk8s kubectl delete -f .)

apply_batfish-with-nodeport:
	(cd batfish-latest-nodeport && microk8s kubectl apply -f .)

delete_batfish-with-nodeport:
	(cd batfish-latest-nodeport && microk8s kubectl delete -f .)

apply_elk-with-lb:
	(cd elk-stack-latest-lb && microk8s kubectl apply -f .)

delete_elk-with-lb:
	(cd elk-stack-latest-lb && microk8s kubectl delete -f .)

apply_elk-with-nodeport:
	(cd elk-stack-latest-nodeport && microk8s kubectl apply -f .)

delete_elk-with-nodeport:
	(cd elk-stack-latest-nodeport && microk8s kubectl delete -f .)

apply_grafana-with-lb:
	(cd grafana-latest-lb && microk8s kubectl apply -f .)

delete_grafana-with-lb:
	(cd grafana-latest-lb && microk8s kubectl delete -f .)

apply_grafana-with-nodeport:
	(cd grafana-latest-nodeport && microk8s kubectl apply -f .)

delete_grafana-with-nodeport:
	(cd grafana-latest-nodeport && microk8s kubectl delete -f .)
