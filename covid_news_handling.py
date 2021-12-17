#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 18:18:51 2021

@author: anthimevalin
"""

from newsapi import NewsApiClient
import requests
import sched, time
import json 

try:
    with open('config_confidential.json', 'r') as f:
        config_confidential = json.load(f)
except:
    print('Could not config_confidential.json')



api = NewsApiClient(api_key=config_confidential['api_key'])
api_key = config_confidential['api_key']


def news_API_request(covid_terms = ['Covid', 'COVID-19', 'coronavirus']) -> dict:
    keywords = covid_terms
    term = 0
    url = ('http://newsapi.org/v2/top-headlines?q=' + (keywords[term]) + '&language=en' + '&apiKey=' + api_key)
    for terms in keywords:
        url = ('http://newsapi.org/v2/top-headlines?q=' + (keywords[term]) + '&language=en' + '&apiKey=' + api_key)
        url_x = requests.get(url)
        term = term + 1

    url_x_info = url_x.json()

    return(url_x_info)




scheduler_news = sched.scheduler(time.time, time.sleep)
    

def update_news(update_interval, update_name):
    news_API_request()
    scheduler_news.enter(update_interval, 1, update_news, (update_interval, update_name))



    
   

