#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 09:49:01 2021

@author: anthimevalin
"""
import csv
from uk_covid19 import Cov19API
import sched
import time


    


def parse_csv_data(csv_filename):
    try:
        file = open(csv_filename)
        csvreader = csv.reader(file)
    except:
        print('csv_filename not found')
    covid_csv_data = []
    for row in csvreader:
        covid_csv_data.append(row)
    return(covid_csv_data)


def process_covid_csv_data(covid_csv_data):
    current_hospital_cases = int(float(covid_csv_data[1][-2]))
    
    last7days_cases = 0
    for i in range(3, 10):
        last7days_cases += int(float(covid_csv_data[i][-1]))
        
    entry = False
    j = 1 
    while not entry:
        if covid_csv_data[j][-3] == '':
            j = j + 1
        else: 
            entry = True
    total_deaths = int(float(covid_csv_data[j][-3]))
    return last7days_cases, current_hospital_cases, total_deaths




###############################################################################


def covid_API_request(location = 'Exeter', location_type = 'Ltla') -> dict:

    location_filter = [f'areaType={location_type}', f'areaName={location}']


    req_structure = {
        "date": "date",
        #"areaName": "areaName",
        #"areaType": "areaType",
        "newCasesByPublishDate": "newCasesByPublishDate",
        #"cumCasesByPublishDate": "cumCasesByPublishDate",
        #"newDeathsByPublishDate": "newDeathsByPublishDate",
        #"cumDeathsByPublishDate": "cumDeathsByPublishDate",
        #"cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate",
        "cumDeaths60DaysByPublishDate": "cumDeaths60DaysByPublishDate",
        #"newDeaths28DaysByDeathDateAgeDemographics": "newDeaths28DaysByDeathDateAgeDemographics",
        "hospitalCases": "hospitalCases",
        #"cumVaccinationBoosterDoseUptakeByPublishDatePercentage": "cumVaccinationBoosterDoseUptakeByPublishDatePercentage",
        #"cumVaccinationCompleteCoverageByPublishDatePercentage": "cumVaccinationCompleteCoverageByPublishDatePercentage",
        #"cumVaccinationFirstDoseUptakeByPublishDatePercentage": "cumVaccinationFirstDoseUptakeByPublishDatePercentage",
        #"cumVirusTestsByPublishDate": "cumVirusTestsByPublishDate"
        
        }
    try:
        api = Cov19API(filters=location_filter, structure=req_structure)

        data = api.get_json()
    except:
        print('Cant access Cov19API')

    return(data)






def infection_rate_exeter():
    i = 0
    days_7 = []
    while i < 6:
        days_7.append((covid_API_request()['data'][i])['newCasesByPublishDate'])
        i = i + 1
    return (sum(days_7)/7)


def infection_rate_england():
    i = 0
    days_7 = []
    while i < 6:
        days_7.append((covid_API_request('England', 'nation')['data'][i])['newCasesByPublishDate'])
        i = i + 1
    return (sum(days_7)/7)




scheduler = sched.scheduler(time.time, time.sleep)

def schedule_covid_updates(update_interval, update_name):
    covid_API_request()
    scheduler.enter(update_interval, 1, schedule_covid_updates, (update_interval, update_name))




