#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:25:47 2019

@author: sebas12
"""


### Neccessary import statements
import numpy as np
import os
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

### Define Neccessary Function(s)
def team_stats_downloader(driver_object, current_year , *args , **kwargs):
    """
    Purpose: Downloads the excel spreadsheet for the specified year which contains team statistics PER 100
             POSSESSIONS for all 30 teams in the NBA. After this, the file is moved to the correct folder 
             location for easy use and access later on.
    
    Details: See the README file in the folder where these files are stored for information about each column
             header.
    
    Arguments:
        driver_object - Selenium driver class/object which is instantiated before the class is called via a 
                        line of code such as: driver = webdriver.Chrome('/{path to driver}/'). This is what 
                        will be used to navigate to the neccessary webpages where the data to be scraped 
                        lives.
        current_year - str object that is of the form i.e., '2018-19' which describes the year that you wish 
                       the function to get data from.
        *args - any positional arguments that may be needed in future implementations of this function. 
                Current version does NOT support the use of them.
        **kwargs - any additional keyword arguments that may be needed in future implementations of this 
                   function. Current version does NOT support the use of them.
        
    
    Useful Resources:
        1. https://www.basketball-reference.com/
        2. Selenium Documentation.
    """
    
    ### Get the data
    # navigate to page of data.
    initial_link = 'https://www.basketball-reference.com/leagues/NBA_20{}.html'.format(current_year[5::])
    driver.get(initial_link)
    hundo = driver.find_element_by_link_text('Team Per 100 Poss Stats')
    driver.execute_script("arguments[0].click();", hundo)
    
    # download the spreadsheet
    driver.implicitly_wait(7)
    buttons = driver.find_elements_by_class_name('tooltip')
    driver.execute_script("arguments[0].click();", buttons[53])
    
    
    ### Redirect file
    # wait for file to completely download
    sleep(10)
    
    # get the file.
    computer_user_name = os.getlogin()
    for file in os.listdir('/Users/{}/Downloads'.format(computer_user_name)):
        if file.endswith('.xls'):
            xls_file = file
    
    # rename and move it.
    data_path = '/Users/{}/Documents/Python/sports_betting/data/external/basketball_reference/Team_data'.format(computer_user_name)
    os.rename('/Users/{}/Downloads/{}'.format(computer_user_name , xls_file) ,
              '{}/team_data_{}.xls'.format(data_path , current_year)  )
    
    return 'Process complete for {} NBA season.'.format(current_year)

### Execution
# instantiate the webdriver
driver = webdriver.Chrome('/Users/sebas12/Downloads/chromedriver')

# download the spreadsheets iteratively
years_list = ['20{}-{}'.format(i , i+1) for i in range(18 , 9 , -1)] + ['2009-10'] + ['200{}-0{}'.format(i , i+1) for i in range(8 , 3 , -1)]
for year in years_list:
    team_stats_downloader(driver , year)
    