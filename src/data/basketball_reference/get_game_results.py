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

### Define the class
class game_results_downloader:
  def __init__(self , webdriver_path = '/Users/sebas12/Downloads/chromedriver', *args, **kwargs):
    """
    Purpose: 
      
    Details: 

    Arguments:
        self - Variable that contains the attributes of this class. This variable gets initilizied with the 
               attributes driver when initialized.
        webdriver_path - Location on the user's computer of the downloaded webdriver (see resource 2.) that will
                         be used to execute webdriver commands. The default value is the location of the 
                         webdriver on the author of this function's machine.
        args - Positional arguments that are included for potential use in future versions of this class
        kwargs - Keyword arguments that allow the user to specify which webrowser to use. In the current version
                 of this function, this is the ONLY thing that can be validally passed as keyword argument. 

                 The webrowers that the user can use are Firefox, Opera, Safari, and Chrome.

                 IF the webdriver is not specified, the default is Chrome.

    Useful Resources:
        1. https://stackoverflow.com/questions/625083/what-init-and-self-do-on-python
        2. https://www.seleniumhq.org/download/ (section Third Party Drivers, Bindings, and Plugins)
    """
    if kwargs:
      if kwargs.get('webdriver').lower() == 'firefox':
        self.driver = webdriver.Firefox(webdriver_path)
      if kwargs.get('webdriver').lower() == 'opera':
        self.driver = webdriver.Opera(webdriver_path)
      if kwargs.get('webdriver').lower() == 'safari':
        self.driver = webdriver.Safari(webdriver_path)
      if kwargs.get('webdriver').lower() == 'chrome':
        self.driver = webdriver.Chrome(webdriver_path)

    else:
      self.driver = webdriver.Chrome(webdriver_path)

    def __str__(self):
      """
      Purpose: 
        
      Details: 

      Arguments:
          self -  

      Useful Resources:
          1. 
      """
      return 'Class to download data from https://basketball-reference.com/ using Selenium.'

    def __repr__(self):
      """
      Purpose: 
        
      Details: 

      Arguments:
          self -  

      Useful Resources:
          1. 
      """
      return self.driver

  def get_data(self, season_year, all_months = True, *args, **kwargs):
      """
      **Purpose:**
      This function will download boxscore .xls spreadsheets from `Basketball-reference <Basketball-reference.com>` 
      of a given NBA season. After this, it will move each file to the desired directory. This is done by using
      the web automation provided by the Selenium Python package as well as the os Python package.
      
      **Details:**
      This function can only handle calls for one season.

      When the files are moved, they are moved into a new directory season_year and also renamed in the 
      following way: Month_season_year.xls.
      
      **Arguments:**
      :type season_year: str
          Describes the year that you wish the function to get data from. The format of this variable is 
          'Start year - end year', i.e., '2018-19'.

      :type all_months: Boolean, optional (default=True)
          Determines whether or not the function will download data for every month of the specified season.

      :type args: None
          Positional arguments that are included for potential use in future versions of this class.

      :type kwargs: str
          Positional arguments that allow the user to specify the months to get data for (if all_months is set 
          to False) and/or the final path for the spreadsheet. 

          For specifying months, the keyword arguments themselves (i.e., month_one) is not what matters thanks 
          to the way you iterate over dictionaries in Python, but what does matter is the values you set for 
          them; they have to be strings of the months themselves with the first letter capitalized and the 
          month(s) spelled out entirely and correctly.

          To specify the final location of the downloaded spreadsheets, the user must use the keyword 'final_path'.
          If this keyword is not given, the function will default to ~/data/external/basketball_reference/game_results/season_year/
          
      :returns: str telling the user that the downloading and relocation of files is complete.
      
      **Useful Resources:**
      1. `Basketball-reference Homepage <Basketball-reference.com>`
      2. `Selenium Documentation. <https://www.seleniumhq.org/>`
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
      
      if all_months:
          # instantiate a list of the months:
          months_list = ['October' , 'November' , 'December' , 'January' , 'February' , 'March' , 'April']
          inital_string = 'Will download data for ' + '{}, '*len(months_list)
          print(inital_string.format(*months_list))
          
          # download the spreadsheet for all of the months iteratively. 
          for month in months_list:
              # navigate to the month's webpage
              html_link = 'https://www.basketball-reference.com/leagues/NBA_20{}_games-{}.html'.format(season_year[5::] ,  month.lower())
              driver.get(html_link)
              
              if driver.title[0] == 'P':
                # navigations to a webpage that does NOT exist on this site lead to the driver having the title
                # 'Page Not Found (404 error) | Basketball-Reference.com'.
                print('Not downloading data for {}. Webpage not found.'.format(month))
              else:
                # download the month's spreadsheet
                element_to_hover_over = driver.find_elements_by_class_name('hasmore')
                ActionChains(driver).move_to_element(element_to_hover_over[-1]).perform()
                buttons = driver.find_elements_by_class_name('tooltip')
                try:
                    buttons[2].click()
                except:
                    driver.implicitly_wait(10) # seconds
                    buttons[2].click()
                print('   Downloaded data for {}.'.format(month))
      
      else:
          # instantiate a list of the months based on what the user passed in to kwargs:
          months_list = list(kwargs.values())

          # sort the months just in case the user didn't do so.
          all_months = ['January' , 'February' , 'March' , 'April' , 'May' , 'June' , 'July' , 'August' , 'September' , 'October' , 'November' , 'December']
          months_list = sorted(months_list , key = lambda x: all_months.index(x))

          inital_string = 'Will download data for ' + '{}, '*len(months_list)
          print('{}'.format(inital_string , *months_list))
          
          # get data
          for month in months_list:
              # navigate to the month's webpage
              html_link = 'https://www.basketball-reference.com/leagues/NBA_20{}_games-{}.html'.format(season_year[5::] ,  month.lower())
              driver.get(html_link)
              
              if driver.title[0] == 'P':
                # navigations to a webpage that does NOT exist on this site lead to the driver having the title
                # 'Page Not Found (404 error) | Basketball-Reference.com'.
                print('Not downloading data for {}. Webpage not found.'.format(month))
              else:
                # download the month's spreadsheet
                element_to_hover_over = driver.find_elements_by_class_name('hasmore')
                ActionChains(driver).move_to_element(element_to_hover_over[-1]).perform()
                buttons = driver.find_elements_by_class_name('tooltip')
                try:
                    buttons[2].click()
                except:
                    driver.implicitly_wait(10) # seconds
                    buttons[2].click()
                print('Downloading data for {}.'.format(month))
      
      
      ### Second, we rename and move the files for easier use in the future.
      computer_user_name = os.getlogin()
      data_path = kwargs.get('final_path' , 
                             '/Users/{}/Documents/Python/sports_betting/data/external/basketball_reference/Game_results/{}'.format(computer_user_name , season_year))
      # make script wait for a few seconds while all of the downloaded files load in.
      print('Now moving files to {}'.format(data_path))
      sleep(10) # the script will wait for 10 seconds before doing anything.
      
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
      os.mkdir(data_path)
        # put all of the files in a directory whose name is given by the year the user is downloading files for.
      for file , month in zip(xls_files , months_list):
          os.rename('/Users/{}/Downloads/{}'.format(computer_user_name , file) , 
                    '{}/{}_{}.xls'.format(data_path , month , season_year))

      driver.quit()
          
      return 'Process complete for {} NBA season.'.format(season_year)


### Execution
if __name__ == '__main__': # if we're running the script directly.
  years_list = ['20{}-{}'.format(i , i+1) for i in range(18 , 9 , -1)] + ['2009-10'] + ['200{}-0{}'.format(i , i+1) for i in range(8 , 3 , -1)]

  downloader = game_results_downloader()
  for year in years_list:
    if year == '2011-12':
      # for some reason, there is NO november data on the website for this year EVEN THOUGH games were definetly
      # played on this month in this season!
      downloader.get_data( driver , 
                           year , 
                           all_months = False , 
                           month_one = 'december' ,
                           month_two = 'january' , 
                           month_three = 'february' , 
                           month_four = 'march' , 
                           month_five = 'april' )
    else:
      downloader.get_data(driver , years_list)
