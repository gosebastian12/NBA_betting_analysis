#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:25:47 2019

@author: {sebas12}
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
# instantiate the webdriver
driver = webdriver.Chrome('/Users/sebas12/Downloads/chromedriver') # path of the Chrome webdriver we are using.

class game_results_downloader:
  def __init__(self , webdriver_path = '/Users/sebas12/Downloads/chromedriver', *args, **kwargs):
    """

    """
    self.driver = webdriver.Chrome(webdriver_path)

  def get_data(self, current_year, all_months = True, *args, **kwargs):
      """
      Purpose: This function will download all of the spreadsheets associated with each month (either all or 
               certain ones specified by the user) of a given NBA season. After this, it will move each file to
               the correct folder location allowing for clear organization that will help when data is used in 
               the future.
      
      Details: This function can only handle calls for a given season.
              
               The final destination of the downloaded files is /Users/{sebas12}/Documents/Python/Sports_betting/
               Data/Game_results/current_year.
               
               Note also that this function does not return anything for future use. It just prints out a 
               statement saying that it is done doing what it is set up to do.
      
      Arguments:
          driver_object - Selenium driver class/object which is instantiated before the class is called via a 
                          line of code such as: driver = webdriver.Chrome('/{path to driver}/'). This is what 
                          will be used to navigate to the neccessary webpages where the data to be scraped lives.
          current_year - str object that is of the form i.e., '2018-19' which describes the year that you wish 
                         the function to get data from. 
          all_months - boolean object whose default value is set to True. When set to true, the function will 
                       download ALL of the spreadsheets for each month of the season. If not, it turn to the 
                       keyword arguments that you pass into the function and only download the spreadsheet
                       specified by the months given in the keyword argument.
          *args - any positional arguments that may be needed in future implementations of this function. 
                  Current version does NOT support the use of them.
          **kwargs - arguments passed in to the function only when all_months is set to False. The function is
                     set up so that the only form that it will accept is something like: month_one = 'October',
                     month_two = 'November', month_three = 'March'. The keyword arguments themselves (i.e., 
                     month_one) is not what matters thanks to the way you iterate over dictionaries in Python, 
                     but what does is the values you set for them; they have to be strings of the months 
                     themselves with the first letter capitalized and the month(s) spelled out entirely and 
                     correctly.
      
      Useful Resources:
          1. https://www.basketball-reference.com/
          2. Selenium Documentation.
      """
      def sorted_nicely(l):
        """ Sorts the given iterable in the way that is expected. This function will be used below.
     
        Required arguments:
        l -- The iterable to be sorted.
        """

        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key = alphanum_key)
        
      ### First, download the spreadsheets
      # get driver
      driver = self.driver

      # navigate to webpage.
      initial_html_link = 'https://www.basketball-reference.com/leagues/NBA_20{}_games.html'.format(
                                                          current_year[5::]   )
      driver.get(initial_html_link)
      
      if all_months:
          # instantiate a list of the months:
          months_list = ['October' , 'November' , 'December' , 'January' , 'February' , 'March' , 'April']
          
          # download the October spreadsheet
          element_to_hover_over = driver.find_elements_by_class_name('hasmore')
          ActionChains(driver).move_to_element(element_to_hover_over[-1]).perform()
          buttons = driver.find_elements_by_class_name('tooltip')
          try:
              buttons[2].click()
          except:
              driver.implicitly_wait(10) # seconds
              buttons[2].click()
          
          # do the same for the rest of the months iteratively. 
          for month in months_list[1::]:
              # navigate to the month's webpage
              driver.find_element_by_link_text('{}'.format(month)).click()
              
              # download the month's spreadsheet
              element_to_hover_over = driver.find_elements_by_class_name('hasmore')
              ActionChains(driver).move_to_element(element_to_hover_over[-1]).perform()
              buttons = driver.find_elements_by_class_name('tooltip')
              try:
                  buttons[2].click()
              except:
                  driver.implicitly_wait(10) # seconds
                  buttons[2].click()
      
      else:
          # instantiate a list of the months:
          months_list = list(kwargs.values())
          
          # get data
          for month in months_list:
              # navigate to the month's webpage
              html_link = 'https://www.basketball-reference.com/leagues/NBA_20{}_games-{}.html'.format(
                                                          current_year[5::] ,  months_list[0] )
              driver.get(html_link)
              
              # download the month's spreadsheet
              element_to_hover_over = driver.find_elements_by_class_name('hasmore')
              ActionChains(driver).move_to_element(element_to_hover_over[-1]).perform()
              buttons = driver.find_elements_by_class_name('tooltip')
              try:
                  buttons[2].click()
              except:
                  driver.implicitly_wait(10) # seconds
                  buttons[2].click()
      
      
      ### Second, we rename and move the files for easier use in the future.
      # make script wait for a few seconds while all of the downloaded files load in.
      sleep(10) # the script will wait for 10 seconds before doing anything.

      computer_user_name = os.getlogin()
      
      # for sorting purposes, rename the first download file.
      os.rename('/Users/{}/Downloads/sportsref_download.xls'.format(computer_user_name) , 
                '/Users/{}/Downloads/sportsref_download (0).xls'.format(computer_user_name))  
      
      # get a list of the file names that were downloaded
      xls_files = []
      for file in os.listdir('/Users/{}/Downloads'.format(computer_user_name)):
          if file.endswith('.xls'):
              xls_files.append(file)
      # order the files with the function defined in the previous cell.
      xls_files = sorted_nicely(xls_files)
      
      # rename and move the files.
      data_path = '/Users/{}/Documents/Python/sports_betting/data/external/basketball_reference/Game_results{}'.format(computer_user_name , current_year)
      os.mkdir(data_path)
        # put all of the files in a directory whose name is given by the year the user is downloading files.
      for file , month in zip(xls_files , months_list):
          os.rename('/Users/{}/Downloads/{}'.format(computer_user_name , file) , 
                    '{}/{}_{}.xls'.format(data_path , month , current_year))
          
      return 'Process complete for {} NBA season.'.format(current_year)


### Execution
if __name__ == '__main__': # if we're running the script directly.
  years_list = ['20{}-{}'.format(i , i+1) for i in range(18 , 9 , -1)] + ['2009-10'] + ['200{}-0{}'.format(i , i+1) for i in range(8 , 3 , -1)]
  for year in years_list:
    if year == '2011-12':
      # for some reason, there is NO november data on the website for this year EVEN THOUGH games were definetly
      # played on this month in this season!
      game_results_downloader( driver , 
                               year , 
                               all_months = False , 
                               month_one = 'december' ,
                               month_two = 'january' , 
                               month_three = 'february' , 
                               month_four = 'march' , 
                               month_five = 'april' )
    else:
      game_results_downloader(driver , years_list)