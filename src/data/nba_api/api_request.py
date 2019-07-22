#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Wed Jul 17 11:25:47 2019
# @author: sebas12


### Neccessary import statements
import numpy as np
from seleniumrequests import Chrome, Firefox, Opera, PhantomJS, Safari
	# we are using the Selenium Requests package instead of requests one because the requests one requires us to
	# pass in the request headers from the url that we are passing into it. There's no easy and straightforward
	# way to do that automatically (see https://stackoverflow.com/questions/39882645/how-to-grab-headers-in-python-selenium-webdriver).
	# So instead we use seleniumrequests which allows us to easily do a get request using the functionality in
	# requests while at the same time getting the headers we need so we don't have to look for them myself. In 
	# the end, this package is much more reliable than requests with the NBA stats API.
import pandas as pd

### Define Class
class nba_stats_API:
	"""
	:Purpose: 

	:Details:

	:type web_browser:
	:param web_browser:

	:type args:
	:param args:

	:type kwargs:
	:param kwargs:

	:returns: 

	:Useful Resources: 1. `Selenium Requests Homepage <https://github.com/cryzed/Selenium-Requests>`_
					   2. ` <>`_
	"""
	def __init__(self, web_browser = 'Chrome', webdriver_path = '/Users/sebas12/Downloads/chromedriver', *args, **kwargs):
		# instantiate the web browser that will be used in this function.
		if web_browser.lower() == 'chrome':
			self.driver = Chrome(webdriver_path)
		elif web_browser.lower() == 'firefox':
			self.driver = FireFox(webdriver_path)
		elif web_browser.lower() == 'opera':
			self.driver == Opera(webdriver_path)
		elif web_browser.lower() == 'phantomjs':
			self.driver = PhantomJS(webdriver_path)
		elif web_browser.lower() == 'safari':
			self.driver = Safari(webdriver_path)

		self.base_url = kwargs.get('base_url' , 'https://stats.nba.com/stats/')
			# for future convinence.
		self.last_url_called = None
			# for future inspection
		self.API_params = None
		

	def player_API_call(self, endpoint, return_format = 'DataFrame', sort_by_playerID = True, prune_player_data = True, *args, **kwargs):
		"""
		:Purpose: This function uses the SeleniumRequests Python package (see resource 1.) to perform an API GET
				  request to the stats.nba.com API. After making the request, the function then performs some
				  processing of the JSON output resulting in its output: the obtained data stored in a the
				  data structure of the user's choice.

		:Details: This function can only handle the following endpoints of the stats.nba.com API (the hyperlinks
				  take you to the documentation of that endpoint):
				  	1. `boxscoreadvancedv2 <https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/boxscoreadvancedv2.md>`_
				  	2. `boxscorefourfactorsv2 <https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/boxscorefourfactorsv2.md>`_
				  	3. `boxscoremiscv2 <https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/boxscoremiscv2.md>`_
				  	4. `boxscorescoringv2 <https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/boxscorescoringv2.md>`_
				  	5. `boxscoretraditionalv2 <https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/boxscoretraditionalv2.md>`_
				  	6. `boxscoreusagev2 <https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/boxscoreusagev2.md>`_
				  Trying to use this function for another endpoint will result in the function not making any calls.

				  All of the endpoint parameters are specified by using the **kwargs functionality of this 
				  function. For most, the only required parameter is :code: GameID. Not passing in the other 
				  parameters will result in them being set to their default values.

		:type endpoint: str
		:param endpoint: Specifies which endpoint of the stats.nba.com API to make GET request to. See the 
						 details section for valid values. 

						 The values of this parameter are not case-sensitive.

		:type return_format: str (Default 'DataFrame')
		:param return_format: Specifies which data structure the function will organize the obtained data in. 
							  Valid values for this variable are 'DataFrame' (returns the data in Pandas 
							  DataFrames), 'Array' (returns the data in NumPy arrays), and 'List' (returns the
							  data in Python lists).

							  The values of this parameter are not case-sensitive.

		:type sort_by_playerID: Boolean (Default True)
		:param sort_by_playerID: Determines whether or not the data structures giving the player statistics will
								 be sorted by the playerIDs.

		:type prune_player_data: Boolean (Default True)
		:param prune_player_data: Determines whether or not the obtained data will be trimmed down to throw away
								  information not relevent to this project.

		:type args: None
		:param args: Positional arguments that are included for potential use in future versions of this function.

		:type kwargs: str
		:param kwargs: Keyword arguments that allow the user to specify the parameters of the Endpoint that they
					   are trying to obtain data. See the documentation for each endpoint (see Details section) 
					   for the neccessary parameters.

					   The values of the keywords ARE case sensitive.

		:returns: tuple object containing organized data structures of the data obtained from the API. The  
				  contents of that tuple will be one of the three possibilities:
				  	1. `Two pandas DataFrames <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
				  		* 2D DataFrame representing the statistics of the players on the away team; rows 
				  		  represent an individual player and columns represent a given statistic (given by the 
				  		  column header).
				  		* 2D DataFrame representing the statistics of the players on the home team; rows 
				  		  represent an individual player and columns represent a given statistic (given by the 
				  		  column header).
				  	2. `Three NumPy arrays <https://docs.scipy.org/doc/numpy/reference/generated/numpy.array.html>`_
				  		* 1D numpy array of the statistics column headers.
				  		* 2D numpy array representing the statistics of the players on the away team; rows 
				  		  represent an individual player and columns represent a given statistic.
				  		* 2D numpy array representing the statistics of the players on the home team; rows 
				  		  represent an individual player and columns represent a given statistic.
				  	3. `Three Python lists <https://docs.python.org/3/tutorial/datastructures.html>`_
				  		* 1D Python list of the statistics column headers.
				  		* 2D Python list representing the statistics of the players on the away team; rows 
				  		  represent an individual player and columns represent a given statistic.
				  		* 2D Python list representing the statistics of the players on the home team; rows 
				  		  represent an individual player and columns represent a given statistic.

		:Useful Resources: 1. `Selenium Requests Homepage <https://github.com/cryzed/Selenium-Requests>`_
						   2. ` <>`_
		"""
		### make endpoint case-insensitive 
		endpoint = endpoint.lower()

		headers_to_keep_dict = {'boxscoreadvancedv2' : [ "TEAM_ID" ,	
												         "PLAYER_ID" ,
													     "MIN" , 
												         "E_OFF_RATING" , 
												         "OFF_RATING" , 
												         "E_DEF_RATING" , 
												         "DEF_RATING" ,
												         "E_NET_RATING" ,
												    	 "NET_RATING" ,
													     "AST_PCT" ,
													     "AST_TOV" ,
													     "AST_RATIO" ,
													     "OREB_PCT" ,
													     "DREB_PCT" ,
													     "REB_PCT" ,
													     "TM_TOV_PCT" ,
													     "EFG_PCT" ,
													     "TS_PCT" ,
													     "USG_PCT" ,
													     "E_USG_PCT" ,
													     "E_PACE" ,
													     "PACE" ,
													     "PIE" ] ,
								'boxscorefourfactorsv2' : ["TEAM_ID" , 
														   "PLAYER_ID" ,
														   "FTA_RATE",
														   "OPP_EFG_PCT",
														   "OPP_FTA_RATE",
														   "OPP_TOV_PCT",
														   "OPP_OREB_PCT"] , 
								'boxscoremiscv2' : [ "TEAM_ID" ,
												    "PLAYER_ID" ,
												    "PTS_OFF_TOV" ,
												    "PTS_2ND_CHANCE" ,
												    "PTS_FB" ,
												    "PTS_PAINT" ,
												    "OPP_PTS_OFF_TOV" ,
												    "OPP_PTS_2ND_CHANCE" ,
												    "OPP_PTS_FB" ,
												    "OPP_PTS_PAINT" ,
												    "BLK" ,
												    "BLKA" ,
												    "PF" , 
												    "PFD" ] ,
								'boxscorescoringv2' : [ "TEAM_ID" , 
														"PLAYER_ID" ,
														"PCT_FGA_2PT" ,
														"PCT_FGA_3PT" ,
														"PCT_PTS_2PT" ,
														"PCT_PTS_2PT_MR" ,
														"PCT_PTS_3PT" ,
														"PCT_PTS_FB" ,
														"PCT_PTS_FT" ,
														"PCT_PTS_OFF_TOV" ,
														"PCT_PTS_PAINT" ,
														"PCT_AST_2PM" ,
														"PCT_UAST_2PM" ,
														"PCT_AST_3PM" ,
														"PCT_UAST_3PM" ,
														"PCT_AST_FGM" ,
														"PCT_UAST_FGM" ] , 
								'boxscoretraditionalv2' : [ "TEAM_ID" , 
													        "PLAYER_ID" ,
													        "FGM" , 
													        "FGA" ,
													        "FG_PCT" ,
													        "FG3M" ,
													        "FG3A" ,
													        "FG3_PCT" ,
													        "FTM" ,
													        "FTA" ,
													        "FT_PCT" ,
													        "OREB" ,
													        "DREB" ,
													        "REB" ,
													        "AST" ,
													        "STL" ,
													        "TO" ,
													        "PF" ,
													        "PTS" ,
													        "PLUS_MINUS" ] ,
								'boxscoreusagev2' : []}
		try:
			headers_to_keep_dict[endpoint]
		except KeyError:
			return "Invalid endpoint given. See the details section of this method's docstring for valid endpoints."

		self.API_params = kwargs
		# set the neccessary parameters
		try: 
			kwargs['GameID']
		except KeyError:
			print('Incorrect usage of kwargs; No valid value for GameID is given. \n This is the one required keyword argument. \n Check to see if the right letters are capitalized.')

		if len(kwargs) == 1: 
			# that is, user only passed in a value for GameID (the one required keyword argument).
			self.API_params['EndPeriod'] = 0
			self.API_params['EndRange'] = 0
			self.API_params['RangeType'] = 0
			self.API_params['StartPeriod'] = 0
			self.API_params['StartRange'] = 0
		elif 1 < len(kwargs) < 6:
			# this is, user passed in more keywords than just GameID, but NOT all
			all_params = ['GameID', 'EndPeriod', 'EndRange', 'RangeType', 'StartPeriod', 'StartRange']
			for param in list(kwargs.keys()):
				all_params.remove(param)
			for param in all_params:
				self.API_params[param] = 0
		elif len(kwargs) == 6:
			# that is, user passed in a value for all of the endpoints parameters
			pass
		else:
			# that is, user passed in too many keyword arguments.
			return 'Too many values were passed into **kwargs. \n The function is setup so that kwargs can only be used to pass in endpoint parameters. \n {} does not have that many parameters. \n {} parameters were given when {} only takes 6.'.format(endpoint , len(kwargs) , endpoint)

		# define the URL and make the request
		kwargs_list = []
		_ = [ kwargs_list.extend( [i[0] , i[1]] ) for i in list(self.API_params.items()) ]
		param_string = len(self.API_params)*'{}={}&'

		api_url = self.base_url + '{}?'.format(endpoint) + param_string.format(*kwargs_list)
		requests_obj = self.driver.request('GET' , api_url)
		self.last_url_called = api_url

		# if successful, format and return the data.
		if requests_obj.status_code == 200:
			print('Request to {} was successful.'.format(self.last_url_called))

			data_dict = requests_obj.json()['resultSets'][0]
				# the format of the json object that we get from our GET request is a dictionary with keys
				# 'resource', 'parameters', and 'resultSets'. The location of the data we want is in the
				# 'resultSets' key and the other information is irrelevent to us so we get rid of it. The
				# data in 'resultSets' is in two lists. The first one contains a dictionary that has the
				# player statistics we want while the other contains a dictionary with the team data we are
				# currently not interested in so we also throw that away. 
			stat_headers = data_dict['headers']
			player_stats = data_dict['rowSet']

			if prune_player_data:
				# define what we will keep
				headers_to_keep = headers_to_keep_dict[endpoint] # this was determined beforehand.
				indices_to_keep = []
				for kept_header in headers_to_keep:
					indices_to_keep.append(stat_headers.index(kept_header))
				for list_index, player_list in enumerate(player_stats):
					player_stats[list_index] = [player_list[i] for i in indices_to_keep]
				stat_headers = headers_to_keep
				team_ID_index = 0
				player_ID_index = 1 
			else:
				team_ID_index = 1
				player_ID_index = 4

			# seperate away (listed first) and home players (listed_last)
			away_teamID = player_stats[0][team_ID_index]
			home_teamID = player_stats[-1][team_ID_index]

			away_player_stats = [player for player in player_stats if player[team_ID_index] == away_teamID]
			home_player_stats = [player for player in player_stats if player[team_ID_index] == home_teamID]

			# order each list by player ids for convience later on (if the user desires).
			if sort_by_playerID:
				away_player_stats = sorted(away_player_stats , key = lambda x: x[player_ID_index])
				home_player_stats = sorted(home_player_stats , key = lambda x: x[player_ID_index])
			
			# determine how to output the obtained data
			if return_format.lower() == "dataframe":
				return pd.DataFrame(away_player_stats, columns = stat_headers) , pd.DataFrame(home_player_stats, columns = stat_headers)
			if return_format.lower() == "array":
				return np.array(stat_headers), np.array(away_player_stats), np.array(home_player_stats) 
			if return_format.lower() == "list":
				return stat_headers , away_player_stats , home_player_stats
			else:
				return "Invaid data format requested. Valid values are dataframe, array, and list."

		else:
			return 'Request to {} was not successful. \n Status code is: {}.'.format( self.last_url_called , 
																					  requests_obj.status_code )


	def team_API_call(self, endpoint , *args, **kwargs):
		"""
		:Purpose: 

		:Details:

		:type endpoint:
		:param endpoint:

		:type args:
		:param args:

		:type kwargs:
		:param kwargs:

		:returns: 

		:Useful Resources: 1.
						   2.
		"""
		pass

	def close_driver(self, *args, **kwargs):
		"""
		:Purpose: 

		:Details:

		:returns: 

		:Useful Resources: 1.
						   2.
		"""
		pass

### Execute
if __name__ == '__main__':
	print("Running script directly.")
