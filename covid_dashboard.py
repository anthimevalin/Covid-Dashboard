#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 11:11:48 2021

@author: anthimevalin
"""

from flask import Flask
from flask import render_template 
from flask import request
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates
from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_data_handler import infection_rate_exeter
from covid_data_handler import infection_rate_england
import sched, time
import json
import logging


 



   
logging.basicConfig(filename = 'logging.log', filemode = 'w', format = '%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG) 
    



try:
    with open('config_confidential.json', 'r') as f:
        config_confidential = json.load(f)
        logging.info('config_confidential.json is being read')
except FileNotFoundError:
    logging.critical('Sorry, the file config_confidential does not exist.')

app = Flask(__name__, template_folder='template', static_url_path = config_confidential['static_path'])

def minutes_to_seconds( minutes: str ) -> int:
        return int(minutes)*60
    
def hours_to_minutes( hours: str ) -> int:
    return int(hours)*60


def hhmm_to_seconds( hhmm: str ) -> int:
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])

def hhmmss_to_seconds( hhmmss: str ) -> int:
    if len(hhmmss.split(':')) != 3:
        print('Incorrect format. Argument must be formatted as HH:MM:SS')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + \
        minutes_to_seconds(hhmmss.split(':')[1]) + int(hhmmss.split(':')[2])


def current_time_hhmm():
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min) 
scheduler_news = sched.scheduler(time.time, time.sleep)
scheduler = sched.scheduler(time.time, time.sleep)

try:
    with open('config_info.json', 'r') as f2:
            config_info = json.load(f2)
            logging.info('config_info.json is being read')
except FileNotFoundError:
    logging.critical('Sorry, the fileconfig_info.json does not exist.')
     
#event_dict is the dictionary that holds 'update' and 'scheduled_events'
try:    
    event_dict = config_info
except NameError:
    logging.critical('Sorry, config_info is not defined')
#event_dict = {'update': [], 'scheduled_events': []}

#A for loop to initiate the program
for i in range(len(event_dict['update'])):
    scheduler.run(blocking=False)
    scheduler_news.run(blocking=False)
    init_update_time = ((event_dict['update'])[i])['content']
    logging.debug(f'The init_update_time: {init_update_time}')
    init_update_time_sec = hhmm_to_seconds(init_update_time)
    logging.debug(f'The init_update_time in seconds: {init_update_time_sec}')
    init_current_time_sec = hhmm_to_seconds(current_time_hhmm())
    logging.debug(f'The init_current_time in seconds: {init_current_time_sec}')
    
    #An if/else function that deals with events that were repeated or not repeated
    if ((event_dict['update'])[i])['repeat'] == False:
        if init_update_time_sec > init_current_time_sec:
            init_delay = init_update_time_sec - init_current_time_sec    
            logging.debug(f'init_delay = {init_delay}')
        else:
            init_delay = (init_update_time_sec - init_current_time_sec) + 86400 
            logging.debug(f'init_delay = {init_delay}')
      
        #schedule to open covid_API_request when init_delay is reached
        scheduler.enter(init_delay, 1, covid_API_request())

    else:
        if init_update_time_sec > init_current_time_sec:
            init_delay = init_update_time_sec - init_current_time_sec   
            logging.debug(f'init_delay = {init_delay}')
        else:
            init_delay = (init_update_time_sec - init_current_time_sec) + 86400
            logging.debug(f'init_delay = {init_delay}')
        scheduler.enter(init_delay, 1, covid_API_request())
        init_update_interval = 86400
        update_name = ((event_dict['update'])[i])['title']
        logging.debug(f'update_name = {update_name}')
        #schedule to run schedule_covid_updates when init_delay is reached
        scheduler.enter(init_delay, 1, schedule_covid_updates, (init_update_interval, update_name))

   




@app.route('/index', methods=['GET', 'POST'])
def index():
    

    scheduler.run(blocking=False)
    scheduler_news.run(blocking=False)
    update_label = request.args.get('two')

    
    if update_label:
        update_time = request.args.get('update')
        logging.debug(f'The update_time: {update_time}')
        update_time_sec = hhmm_to_seconds(update_time)
        logging.debug(f'The update_time in seconds: {update_time_sec}')
        current_time_sec = hhmm_to_seconds(current_time_hhmm())
        logging.debug(f'The current_time in seconds: {current_time_sec}')
        
        
        covid_data_checkbox = request.args.get('covid-data')
        repeat_checkbox = request.args.get('repeat')
        if covid_data_checkbox:
                
            if update_time_sec > current_time_sec:
                delay = update_time_sec - current_time_sec
                logging.debug(f'delay = {delay}')
                update_list = {'title': f'data: {update_label}', 'content': update_time, 'repeat': False}
               
            else:
                delay = (update_time_sec - current_time_sec) + 86400
                logging.debug(f'delay = {delay}')
                update_list = {'title': f'data: {update_label}', 'content': update_time, 'repeat': False}
            
            
            update_event_without_repeat = scheduler.enter(delay, 1, covid_API_request())
            
           
            if repeat_checkbox:
                update_list = {'title': f'data daily: {update_label}', 'content': update_time, 'repeat': True}
                update_interval = 86400
                update_name = update_label
                logging.debug(f'update_name = {update_name}')
                scheduler.enter(delay, 1, schedule_covid_updates, (update_interval, update_name))
                
            event_list = {'update_event_without_repeat': update_event_without_repeat}
            logging.debug(f'event_list: {event_list}')
            event_dict['update'].append(update_list)
            event_dict['scheduled_events'].append(event_list)
                
        news_checkbox = request.args.get('news')   
        
        if news_checkbox:
          
          if update_time_sec > current_time_sec:
              delay = update_time_sec - current_time_sec
              logging.debug(f'delay = {delay}')
              update_list = {'title': f'news: {update_label}', 'content': update_time, 'repeat': False}
  
          else:
              delay = (update_time_sec - current_time_sec) + 86400
              logging.debug(f'delay = {delay}')
              update_list = {'title': f'news: {update_label}', 'content': update_time, 'repeat': False}
              
      
          update_event_without_repeat = scheduler_news.enter(delay, 1, news_API_request())
     
          if repeat_checkbox:
              update_list = {'title': f'daily news: {update_label}', 'content': update_time, 'repeat': True}
              update_interval = 86400
              update_name = update_label
              logging.debug(f'update_name = {update_name}')
              scheduler_news.enter(delay, 1, update_news, (update_interval, update_name))
              
          event_list = {'update_event_without_repeat': update_event_without_repeat}
          logging.debug(f'event_list: {event_list}')
          event_dict['update'].append(update_list)
          event_dict['scheduled_events'].append(event_list)
           
  
    update_item = request.args.get('update_item')
    if update_item:
         for i in range(len(event_dict['update'])):
             if (event_dict['update'])[i]['title'] == update_item:
                 try:
                     scheduler.cancel(((event_dict['scheduled_events'])[i])['update_event_without_repeat'])
                 except Exception as e:
                     logging.error(e)   
                 del (event_dict['update'])[i] 
                 del (event_dict['scheduled_events'])[i]
                 logging.info('update_item deleted')
                 break
             
   
    notif = request.args.get('notif')
    if notif:
        for i in range(len(news_API_request()['articles'])):
            if (news_API_request()['articles'])[i]['title'] == notif:
                del (news_API_request()['articles'])[i]
                break
        
    try:           
        with open('config_info.json', 'w') as f2:
                json.dump(event_dict, f2)
                logging.info('json dump of event_dict into f2 is successful')
    except FileNotFoundError:
        logging.critical('Sorry, the file config_info.json does not exist')
            
    
     
    return render_template('index.html', 
                           title ='Daily update',
                           location = 'Exeter', 
                           nation_location = 'England',
                           local_7day_infections = round(infection_rate_exeter()),
                           national_7day_infections = round(infection_rate_england()),
                           hospital_cases = f"Hospital cases: {((covid_API_request('England', 'nation')['data'][0])['hospitalCases'])}", 
                           deaths_total = f"Total deaths: {((covid_API_request('England', 'nation')['data'][0])['cumDeaths60DaysByPublishDate'])}",
                           news_articles = (news_API_request()['articles']),
                           updates = event_dict['update']
                          
                           )





if __name__ == '__main__':
    app.run(debug=True)
     
#ADD IN DOCUMENTATION need to do --info do change level
#User can change the default level (warning) by adding a command agrument 


