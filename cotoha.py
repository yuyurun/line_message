#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json

import csv
import random


def auth(CLIENT_ID, CLIENT_SECRET):
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    data = {
        "grantType": "client_credentials",
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET
    }
    r = requests.post('https://api.ce-cotoha.com/v1/oauth/accesstokens',
                      headers=headers,
                      data=json.dumps(data))
    print(r.json())
    return r.json()["access_token"]


def parse(text, access_token):
    base_url = 'https://api.ce-cotoha.com/api/dev/nlp/'
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
    print(r.json(), r_type.json())
    return r.json(), r_type.json()


def convert(r_parse, r_type):
    response = ''
    res_list = ['たくなーい！','たくないよ(｀ε´*)','たくない！','たくないもん']
    if r_type["result"]['dialog_act'] == ['directive']:
        for word in r_parse["result"]:
            for token in word["tokens"]:
                nai = make_gokan_dic(token['features'])
                if token['pos'] == '動詞語幹' and nai != False:
                    response = token['form'] + nai + random.choice(res_list)
    elif r_type["result"]['dialog_act'] == ['information-providing']:
        f = ''
        for word in r_parse["result"]:
            for token in word["tokens"]:
                if token['pos'] == '動詞語幹':
                    f = token['lemma']
                    print(f)
                elif token['form'] == 'う' and token['pos'] == '動詞接尾辞' and len(f) > 0:
                    response = f + '!!'
    return response


def make_gokan_dic(gokan):
    if len(gokan) == 0:
        return False
    gokan_dic = {}
    with open('data/gokan.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            gokan_dic[row[0]] = row[1]
    for k, v in gokan_dic.items():
        if gokan[0] == k:
            return v
    return False


def trans(text, C_ID, C_TOKEN):
    access_token = auth(C_ID, C_TOKEN)
    res_list = ['んんん？','わかんない…','うーんと','( ；ᵕ； )']

    if len(text) > 15:
        response = random.choice(res_list)
    else:
        r_parse, r_type = parse(text, access_token)
        response = convert(r_parse, r_type)
        if response == '':
            response = random.choice(res_list)
    return response
