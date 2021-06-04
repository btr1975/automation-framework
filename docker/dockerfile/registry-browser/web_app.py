"""
Repository Browser Web Server
"""
import os
import flask
from flask import Flask
from flask import render_template
from registry_browser import DockerRegistryApi


app = Flask(__name__, template_folder='./templates')
REGISTRY_SERVER = os.environ.get('REGISTRY_SERVER') or 'http://127.0.0.1'

print(f'USING REGISTRY_SERVER {REGISTRY_SERVER}')

@app.route('/', methods=['GET'])
def home():
    if flask.request.method == 'GET':
        registry = DockerRegistryApi(REGISTRY_SERVER)
        return render_template(
            'home.html',
            title='Docker Registry Browser Home',
            description='Docker Registry Browser Home',
            registry_results_data=registry.get_catalog().get('repositories')
        )

    else:
        raise Exception()


@app.route('/repository/<repository_name>', methods=['GET'])
def repository(repository_name):
    if flask.request.method == 'GET':
        registry = DockerRegistryApi(REGISTRY_SERVER)
        return render_template(
            'repository-info.html',
            title=f'Docker Registry Repository Tags {repository_name}',
            description=f'Docker Registry Repository Tags {repository_name}',
            repository_name=repository_name,
            repository_results_data=registry.get_repository_tags(repository_name).get('tags')
        )

    else:
        raise Exception()


@app.route('/manifest/<repository_name>/<tag>', methods=['GET'])
def repository_tag_manifest(repository_name, tag):
    if flask.request.method == 'GET':
        registry = DockerRegistryApi(REGISTRY_SERVER)
        manifest = registry.get_pretty_json(registry.get_repository_manifest(repository_name, tag))
        return render_template(
            'repository-tag-manifest-info.html',
            title='Docker Registry Browser Home',
            description='Docker Registry Browser Home',
            repository_name=repository_name,
            tag=tag,
            repository_tag_manifest_results_data=manifest
        )

    else:
        raise Exception()


def run_local_server(ip_addr, port, debug=True):
    app.run(port=int(port), host=ip_addr, debug=debug)


if __name__ == '__main__':
    run_local_server('0.0.0.0', 8080)
