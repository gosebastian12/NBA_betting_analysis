#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Wed Jul 17 11:25:47 2019
# @author: sebas12


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
class team_stats_downloader:
    def __init__(self, driver_url):
        self.driver = webdriver.Chrome('/Users/sebas12/Downloads/chromedriver')

    def get_data(self, season_year , *args , **kwargs):
        """
        :Purpose: This function will download the .xls spreadsheet from from `Basketball-reference 
                  <Basketball-reference.com>`_ for the specified year which contains team statistics PER 100 
                  POSSESSIONS for all 30 teams in the NBA.  After this, the file is moved to the desired location 
                  for future use.
        
        :Details: See the Basketball-refence website for information about the headers of these spreadsheets.
        
        :type season_year: str
        :param season_year: Describes the year that you wish the function to get data from. The format of this 
                            variable is 'Start year - end year', i.e., '2018-19'.

        :type args: None
        :param args: Positional arguments that are included for potential use in future versions of this class.

        :type kwargs: None
        :param kwargs: Keyword arguments that allow the user to specify the path of the location that the function 
                       will move the downloaded .xls spreadsheet to. If not specified, the function defaults to: 
                       ~/data/external/basketball_reference/Team_data/
        
        :Useful Resources:
        1. `Basketball-reference Homepage <Basketball-reference.com>`_
        2. `Selenium Documentation. <https://www.seleniumhq.org/>`_
        """
        
        ### Get the data
        # navigate to page of data.
        initial_link = 'https://www.basketball-reference.com/leagues/NBA_20{}.html'.format(season_year[5::])
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
        data_path = kwargs.get('final_path' , 
                               '/Users/{}/Documents/Python/sports_betting/data/external/basketball_reference/Game_results/{}'.format(computer_user_name , season_year))
        os.rename('/Users/{}/Downloads/{}'.format(computer_user_name , xls_file) ,
                  '{}/team_data_{}.xls'.format(data_path , season_year)  )
        
        return 'Process complete for {} NBA season.'.format(season_year)

### Execution
# instantiate the webdriver
if __name__ == '__main__': # only run if we're running the script directly.
    # download the spreadsheets iteratively
    years_list = ['20{}-{}'.format(i , i+1) for i in range(18 , 9 , -1)] + ['2009-10'] + ['200{}-0{}'.format(i , i+1) for i in range(8 , 3 , -1)]
    for year in years_list:
        team_stats_downloader(driver , year)
    