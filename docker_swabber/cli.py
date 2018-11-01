"""Automate management of Docker hub image tags."""

import os
import configparser
import requests

import click

from . import __version__


USER_SECTION_KEY = 'user'


TOKEN_OPTION_KEY = 'token'


def get_token():
    """Read stored auth token."""
    cfg = os.path.join(click.get_app_dir('swabber'), 'config.ini')
    parser = configparser.RawConfigParser()
    parser.read([cfg])
    token = parser[USER_SECTION_KEY][TOKEN_OPTION_KEY]
    return token


def set_token(new_token):
    """Store auth token."""
    cfg = os.path.join(click.get_app_dir('swabber'), 'config.ini')
    parser = configparser.RawConfigParser()
    parser.read([cfg])

    try:
        parser[USER_SECTION_KEY][TOKEN_OPTION_KEY] = new_token
    except KeyError:
        parser[USER_SECTION_KEY] = {TOKEN_OPTION_KEY: new_token}

    if not os.path.exists(click.get_app_dir('swabber')):
        os.makedirs(click.get_app_dir('swabber'))
    with open(cfg, 'w') as configfile:
        parser.write(configfile)


@click.group()
@click.version_option(__version__)
def main():
    """Small CLI to automate management of Docker hub image tags."""
    pass


@main.command()
@click.option('--username', '-u', help='Docker Hub username.')
@click.option('--password', '-p', help='Docker Hub password.')
def login(username, password):
    """Login to Docker Hub and store auth token."""
    request = requests.post('https://hub.docker.com/v2/users/login/',
                            json={'username': username, 'password': password})
    token = request.json()['token']
    set_token(token)
