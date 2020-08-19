#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest.mock import MagicMock
import pickle


def convert_normal(cli):
    api_instance = cli.api_instance
    resp_get_token = {'api-token': "tmp"}
    api_instance.get_access_token = MagicMock(
        return_value=resp_get_token)

    resp_get_competition = {'data': [
        {'competitionId': 1, 'title': '銀行の顧客ターゲティング【練習問題】',
         'closing': '2100-01-01 00:00:00', 'prize': 'Knowledge', 'participants': 0},
        {'competitionId': 2, 'title': 'お弁当大作戦After【練習問題】',
         'closing': '2100-01-01 00:00:00', 'prize': 'Knowledge', 'participants': 0},
        {'competitionId': 3, 'title': 'レコメンドエンジン作成チャレンジコンペティション',
         'closing': '2100-01-01 00:00:00', 'prize': '60万円', 'participants': 0},
    ]}
    api_instance.get_competitions = MagicMock(
        return_value=resp_get_competition)

    resp_get_competition_files = {'data': [
        {'fileId': 1, 'name': 'train.csv', 'title': '学習用データ',
            'size': 2345067, 'updated_at': '2019-02-14 13:00:29'},
        {'fileId': 2, 'name': 'test.csv', 'title': '検証用データ',
            'size': 1523536, 'updated_at': '2019-02-14 13:00:29'},
        {'fileId': 3, 'name': 'submit_sample.csv', 'title': '応募用サンプル',
            'size': 205890, 'updated_at': '2019-02-14 13:00:29'}]}

    api_instance.get_competition_files = MagicMock(
        return_value=resp_get_competition_files)

    resp_post_competition_files = {'data': [
        {'fileId': 1, 'url': 'https://www.python.org/ftp/python/3.7.2/python-3.7.2-macosx10.6.pkg',
            'name': 'train.csv', 'size': 2345067, 'updated_at': '2019-02-14 13:00:29'},
        {'fileId': 2, 'url': 'https://www.python.org/ftp/python/3.7.1/python-3.7.1-macosx10.6.pkg',
            'name': 'test.csv', 'size': 1523536, 'updated_at': '2019-02-14 13:00:29'},
        {'fileId': 3, 'url': 'https://www.python.org/ftp/python/3.7.0/python-3.7.0-macosx10.6.pkg',
            'name': 'submit_sample.csv', 'size': 205890, 'updated_at': '2019-02-14 13:00:29'}]}

    api_instance.post_competition_files = MagicMock(
        return_value=resp_post_competition_files)

    resp_post_competition_file = {'data': [
        {'fileId': 1, 'url': 'https://www.python.org/ftp/python/3.7.2/python-3.7.2-macosx10.6.pkg',
            'name': 'train.csv', 'size': 2345067, 'updated_at': '2019-02-14 13:00:29'}]}

    api_instance.post_competition_file = MagicMock(
        return_value=resp_post_competition_file)

    resp_post_submit = {'message':
                        '''You have successfully submitted your predictions.
                            We will send you the submission result to your email address.'''}

    api_instance.post_competition_submit = MagicMock(
        return_value=resp_post_submit)


def convert_raise_error(cli):
    api_instance = cli.api_instance
    with open('ApiException.pickle', mode='rb') as f:
        apiException = pickle.load(f)
    api_instance.get_competitions = MagicMock(side_effect=apiException)
    api_instance.get_competition_files = MagicMock(side_effect=apiException)
    api_instance.post_competition_files = MagicMock(side_effect=apiException)
    api_instance.post_competition_file = MagicMock(side_effect=apiException)
    api_instance.post_competition_submit = MagicMock(side_effect=apiException)
    api_instance.get_access_token = MagicMock(side_effect=apiException)
