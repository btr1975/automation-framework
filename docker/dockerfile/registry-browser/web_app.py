"""
Repository Browser Web Server
"""
import flask
from flask import Flask
from flask import render_template
from registry_browser import DockerRegistryApi


app = Flask(__name__, template_folder='./templates')


@app.route('/', methods=['GET'])
def home():
    if flask.request.method == 'GET':
        registry = DockerRegistryApi('http://10.0.0.101')
        return render_template(
            'home.html',
            title='Docker Registry Browser Home',
            description='Docker Registry Browser Home',
            registry_results_data=registry.get_catalog().get('repositories')
        )

    else:
        raise Exception()


@app.route('/repository/<repository>', methods=['GET'])
def repository(repository):
    if flask.request.method == 'GET':
        registry = DockerRegistryApi('http://10.0.0.101')
        return render_template(
            'repository-info.html',
            title='Docker Registry Browser Home',
            description='Docker Registry Browser Home',
            repository=repository,
            repository_results_data=registry.get_repository_tags(repository).get('tags')
        )

    else:
        raise Exception()

def run_local_server(ip_addr, port, debug=True):
    app.run(port=int(port), host=ip_addr, debug=debug)


if __name__ == '__main__':
    run_local_server('0.0.0.0', 8080)
