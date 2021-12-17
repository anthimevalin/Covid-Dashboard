#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 16:06:25 2021

@author: anthimevalin
"""

import json
from covid_dashboard import event_dict



config_info = {'update': (event_dict['update']),'scheduled_events': (event_dict['scheduled_events'])}



with open('config_info.json', 'w') as f2:
    json.dump(event_dict, f2)

#do you add try in config???