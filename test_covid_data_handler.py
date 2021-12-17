#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 16:56:33 2021

@author: anthimevalin
"""


from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import infection_rate_exeter
import unittest
"""
Test for function called parse csv data that takes an argument called csv 
filename and returns a list of strings for the rows in the file
"""
class TestCovidDataHandler(unittest.TestCase):
    def test_parse_csv_data (self):
        data = parse_csv_data('nation_2021-10-28.csv') 
        self.assertEqual(len(data), 639)
    
          
    
    def test_process_covid_csv_data(self):
        last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
        self.assertEqual(last7days_cases, 240_299)
        self.assertEqual(current_hospital_cases, 7_019)
        self.assertEqual(total_deaths, 141_544)

    
    
    def test_covid_API_request(self):
        self.assertEqual((covid_API_request()['data'][-1])['date'], '2020-04-22')
        
    def test_infection_rate_exeter(self):
        test_exeter_rate = infection_rate_exeter
    
       

if __name__ == '__main__':
    unittest.main()
    
  