#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 14:20:27 2021

@author: anthimevalin
"""


import json


config_confidential = {'api_key': 'f1c4a6d877f246c089fc9ee261632bbd', 'static_path': '/static'}


with open('config_confidential.json', 'w') as f:
    json.dump(config_confidential, f)

