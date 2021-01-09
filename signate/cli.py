#!/usr/bin/python
#
# Copyright 2018 - 2020 SIGNATE Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -*- coding: utf-8 -*-
from operator import itemgetter
from signate import info
from swagger_client.rest import ApiException
from tabulate import tabulate
from textwrap import dedent
import click
import json
import os
import swagger_client
import warnings
import wget

api_instance = None


def success(message):
    click.echo(click.style(message, fg='green'))
    exit(0)


def warn(message):
    click.echo(click.style(message, fg='yellow'))


def error(message):
    click.echo(click.style(message, fg='red'))


def die(message):
    error(message)
    exit(1)


def get_api_token():
    signate_dir = os.path.expanduser('~/.signate/')
    signate_json = os.path.expanduser(signate_dir + 'signate.json')
    if not os.path.isdir(signate_dir):
        os.makedirs(signate_dir)
    try:
        api_token = json.loads(open(signate_json).read())['api-token']
    except FileNotFoundError:
        message = dedent("""
        Could not find %s.
        Please get the API token from this page: %s
        """ % (signate_json, click.style('https://signate.jp/account_settings', fg='blue')))
        die(message)
    except KeyError:
        die('There was no "api-token" key in %s.' % (signate_json))
    return api_token


def set_api_token(token):
    signate_dir = os.path.expanduser('~/.signate/')
    signate_json = os.path.expanduser(signate_dir + 'signate.json')
    if not os.path.isdir(signate_dir):
        os.makedirs(signate_dir)
    try:
        tokenFile = open(signate_json, 'w')
        tokenFile.write(token)
        tokenFile.close()
    except IOError as e:
        warnings.warn("I/O error({0}): {1}".format(e.errno, e.strerror))


def set_api_instance_for_token():
    global api_instance
    configuration = swagger_client.Configuration()
    api_instance = swagger_client.DefaultApi(swagger_client.ApiClient(configuration))


def set_api_instance(api_token):
    global api_instance
    configuration = swagger_client.Configuration()
    configuration.api_key['Authorization'] = api_token
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    api_instance = swagger_client.DefaultApi(swagger_client.ApiClient(configuration))


def set_user_agent():
    global api_instance
    api_instance.api_client.user_agent = info.NAME + '/' + info.VERSION


@click.group()
@click.version_option(version=info.VERSION)
def cli():
    pass


@cli.command()
@click.option('-e', '--email', type=str, required=True, help='The email address to be registered')
@click.option('-p', '--password', type=str, required=True, help='The password to be registered')
def token(email, password):
    """Download the API Token"""
    set_api_instance_for_token()
    api_response = api_instance.get_access_token(email, password)
    set_api_token(api_response.to_str())
    success('The API Token has been downloaded successfully.')


@cli.command()
def list():
    """List competition"""
    prepare()
    api_response = api_instance.get_competitions()
    click.echo(tabulate(api_response['data'], headers='keys', tablefmt='simple', stralign='left'))


@cli.command()
@click.option('-c', '--competition-id', type=int, required=True, help='Specify the id of competitions')
def files(competition_id):
    """List file of competition"""
    prepare()
    api_response = api_instance.get_competition_files(competition_id)
    click.echo(tabulate(api_response['data'], headers='keys', tablefmt='simple', stralign='left'))


@cli.command()
@click.option('-c', '--competition-id', type=int, required=True, help='Specify the id of competitions')
@click.option('-f', '--file-id', type=int, help='Specify id of files')
@click.option('-p', '--path', type=click.Path(exists=True, file_okay=False), help='Specify the download destination')
def download(competition_id, file_id=None, path=None):
    """Download the file of competition"""
    prepare()
    if file_id:
        api_response = fileDownload(competition_id, file_id, path)
    else:
        api_response = api_instance.get_competition_files(competition_id)
        for file in sorted(api_response['data'], key=itemgetter('size')):
            fileDownload(competition_id, file['fileId'], path)
    for message in api_response.get('warnings', []):
        warn(message)
    success('\nDownload completed.')


@cli.command()
@click.option('-c', '--competition-id', type=int, required=True, help='Specify the id of competitions')
@click.option('-n', '--note', type=str, help='You can leave the comment')
@click.argument('result-file', type=click.Path(exists=True, dir_okay=False), required=True)
def submit(competition_id, result_file, note=None):
    """Submit a result file to the competition"""
    prepare()
    if note:
        api_response = api_instance.post_competition_submit(competition_id,
                                                            result_file,
                                                            submission_note=note)
    else:
        api_response = api_instance.post_competition_submit(competition_id,
                                                            result_file)
    success(api_response.message)


def accept(competition_id):
    prepare()
    api_response = api_instance.post_competition_agreement(competition_id)
    success(api_response.message)


def confirm(required_agreement):
    prepare()
    prompt_message = dedent("""
    %s
    Please read the terms of use before accepting: %s
    """ % (required_agreement['prompt'], click.style(required_agreement['termsUrl'], fg='blue')))
    if click.confirm(prompt_message):
        accept(required_agreement['competitionId'])
    else:
        pass


def fileDownload(competition_id, file_id, path):
    api_response = api_instance.post_competition_file(competition_id, file_id)
    if not api_response['data'][0]:
        return api_response
    click.echo(api_response['data'][0]['name'])
    if path:
        wget.download(api_response['data'][0]['url'], out=path)
    else:
        wget.download(api_response['data'][0]['url'])
    click.echo()
    return api_response


def main():
    warnings.filterwarnings(action='ignore')
    try:
        cli()
    except ApiException as ae:
        response = json.loads(ae.body)
        message = response['message']
        if 'requiredAgreement' in response:
            error(message)
            confirm(response['requiredAgreement'])
        elif 'validations' in response:
            for attr, value in response['validations'].items():
                error(attr + ':')
                for e in value:
                    error(e)
            die(message)
        elif message:
            die(message)
        else:
            die(str(ae.status) + ' ' + str(ae.reason))


def prepare():
    api_token = get_api_token()
    set_api_instance(api_token)
    set_user_agent()
