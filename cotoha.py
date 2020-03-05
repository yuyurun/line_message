#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import requests
import json

import csv

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
DEVELOPER_API_BASE_URL = os.environ["DEVELOPER_API_BASE_URL"]
ACCESS_TOKEN_PUBLISH_URL = os.environ["ACCESS_TOKEN_PUBLISH_URL"]


def auth():
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    data = {
        "grantType": "client_credentials",
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET
    }
    r = requests.post(ACCESS_TOKEN_PUBLISH_URL,
                      headers=headers,
                      data=json.dumps(data))
    return r.json()["access_token"]


def parse(text, access_token):
    base_url = DEVELOPER_API_BASE_URL
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8",
        "Authorization": "Bearer {}".format(access_token)
    }
    data = {
        "sentence": text,
        "type": "default"
    }
    r = requests.post(base_url + "v1/parse",
                      headers=headers,
                      data=json.dumps(data))

    data = {
        "sentence": text,
        "type": "default"
    }
    r_type = requests.post(base_url + "v1/sentence_type",
                           headers=headers,
                           data=json.dumps(data))
    return r.json(), r_type.json()


def judge_directive(res):
    directive = False
    if res["result"]['dialog_act'] == ['directive']:
        directive = True
    return directive

def convert(r_parse,r_type):
    response = 'んんん？'
    if judge_directive(r_type):
        for word in r_parse["result"]:
            for token in word["tokens"]:
                nai = make_gokan_dic(token['features'])
                if token['pos'] == '動詞語幹' and nai != False:
                        response = token['form'] + nai + 'たくな〜〜い！'

    return response

def make_gokan_dic(gokan):
    if len(gokan) == 0:
        return False
    gokan_dic = {}
    with open('../data/gokan.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            gokan_dic[row[0]] = row[1]
    for k,v in gokan_dic.items():
        if gokan[0] == k:
            return v
        else:
            return False



def trans(text):
    access_token = auth()
    r_parse, r_type = parse(text, access_token)
    return convert(r_parse, r_type)
