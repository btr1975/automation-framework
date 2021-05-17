# automation-framework
Automation Framework

**This is not meant to be in production, this is a development environment**

## Assumptions

1. You know the basics of [Docker](https://www.docker.com/).
2. You know the basics of [Docker Compose](https://docs.docker.com/compose/).
3. You know the basics of [Docker Swarm](https://docs.docker.com/engine/swarm/).

## General Information

* The base Makefile is meant to be used with Docker Swarm

* The Makefile located in docker/compose is used for individual architecture pieces

* **Compose** does not have memory limits

### Possible Special Need for ELK

* You may need to run this command on the host system

```text
sysctl -w vm.max_map_count=262144
```

### Nautobot required after creating container

* You need to create a super user use the following command, and follow prompts.

```text
docker exec -it <container-name> nautobot-server createsuperuser
```

### Information URLs

* [vm.max_map_count](https://www.elastic.co/guide/en/elasticsearch/reference/5.0/vm-max-map-count.html#vm-max-map-count)
* [curl examples send data to ELK](https://mindmajix.com/elasticsearch/curl-syntax-with-examples)
* [nautobot-lab reference](https://github.com/nautobot/nautobot-lab)
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
* [Docker Swarm](https://docs.docker.com/engine/swarm/)
* [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
* [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

### What is Available in Swarm

| ARCHITECTURE | USED FOR |
|---|---|
| Kafka | As a message bus |
| ELK Elastic Search | Logging search, various other stuff |
| Hashicorp Vault | Secrets Storage |
| Nautobot | "Source of truth" |
| A Genie Parser | Something to parse show commands |

![Automation Framework Swarm](diagrams/automation_framework_swarm.png)

### What is Available in Compose

| ARCHITECTURE | USED FOR |
|---|---|
| Kafka | As a message bus |
| ELK Elastic Search | Logging search, various other stuff |
| Hashicorp Vault | Secrets Storage |
| Nautobot | "Source of truth" |
| A Genie Parser | Something to parse show commands |
| MongoDB | Document dB |
| Batfish | Modeling |
| Influxdb | Series dB |

![Automation Framework Compose](diagrams/automation_framework_compose.png)
