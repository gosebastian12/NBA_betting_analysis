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
from time import sleep

### Define Class
class nba_stats_API:
	"""
	Module that allows for easy access to the statistics stored in the NBA Stats API without sacrificing 
	flexibility.


	Attributes
	--------

	1. driver
	2. base_url
	3. supported_endpoints
	4. last_url_called
	5. API_params
	6. headers_to_keep_dict
	7. teamIDS_dict
	

	Parameters
	--------

		web_browser - *str* (default = 'Chrome')
			Indicates to the class which webdriver to use when making its various GET requests. The available options
			are (notice that the options are not case-sensitive):
			  - 'chrome'
			  - 'firefox'
			  - 'opera'
			  - 'phantomjs'
			  - 'safari'

		webdriver_path - *str* (default = '/Users/sebas12/Downloads/chromedriver')
			Indicates to the function the location of the executable for the the webdriver on the user's machine.


	See Also
	--------
	
	1. `Selenium Requests Homepage <https://github.com/cryzed/Selenium-Requests>`_
	2. `Saving Pandas DataFrames <https://stackoverflow.com/questions/37010212/what-is-the-fastest-way-to-upload-a-big-csv-file-in-notebook-to-work-with-python>`_
	"""
	def __init__(self, web_browser = 'Chrome', webdriver_path = '/Users/sebas12/Downloads/chromedriver', *args, **kwargs):
		# instantiate the web browser that will be used in this function.
		if web_browser.lower() == 'chrome':
			self.driver = Chrome(webdriver_path)
		elif web_browser.lower() == 'firefox':
			self.driver = Firefox(webdriver_path)
		elif web_browser.lower() == 'opera':
			self.driver == Opera(webdriver_path)
		elif web_browser.lower() == 'phantomjs':
			self.driver = PhantomJS(webdriver_path)
		elif web_browser.lower() == 'safari':
			self.driver = Safari(webdriver_path)

		self.driver.set_script_timeout(15)
		self.base_url = kwargs.get('base_url' , 'https://stats.nba.com/stats/')
			# for future convinence.
		self.last_url_called = None
			# for future inspection
		self.API_params = None
		self.teamIDS_dict = { 'ATL' : '1610612737' ,
							  'BOS' : '1610612738' ,
							  'BKN' : '1610612751' ,
							  'CHA' : '1610612766' ,
							  'CHI' : '1610612741' ,
							  'CLE' : '1610612739' ,
							  'DAL' : '1610612742' , 
							  'DEN' : '1610612743' , 
							  'DET' : '1610612765' , 
							  'GSW' : '1610612744' , 
							  'HOU' : '1610612745' , 
							  'IND' : '1610612754' , 
							  'LAC' : '1610612746' , 
							  'LAL' : '1610612747' , 
							  'MEM' : '1610612763' , 
							  'MIA' : '1610612748' , 
							  'MIL' : '1610612749' , 
							  'MIN' : '1610612750' , 
							  'NOP' : '1610612740' , 
							  'NYK' : '1610612752' , 
							  'OKC' : '1610612760' ,
							  'ORL' : '1610612753' , 
							  'PHL' : '1610612755' , 
							  'PHX' : '1610612756' , 
							  'POR' : '1610612757' , 
							  'SAC' : '1610612758' ,
							  'SAS' : '1610612759' , 
							  'TOR' : '1610612761' , 
							  'UTA' : '1610612762' , 
							  'WAS' : '1610612764' }
		self.supported_endpoints = [ 'boxscoreadvancedv2' , 
									 'boxscorefourfactorsv2' , 
									 'boxscoremiscv2' , 
									 'boxscorescoringv2' , 
									 'boxscoretraditionalv2' , 
									 'boxscoreusagev2' ]
		self.headers_to_keep_dict = {'boxscoreadvancedv2' : [ "TEAM_ID" ,	
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
														        "PTS" ,
														        "PLUS_MINUS" ] ,
									'boxscoreusagev2' : ["TEAM_ID" , 
														 "PLAYER_ID" ,
														 "PCT_FGM" ,
														 "PCT_FGA" ,
														 "PCT_FG3M" ,
														 "PCT_FG3A" ,
														 "PCT_FTM" ,
														 "PCT_FTA" ,
														 "PCT_OREB" ,
														 "PCT_DREB" ,
														 "PCT_REB" ,
														 "PCT_AST" ,
														 "PCT_TOV" ,
														 "PCT_STL" ,
														 "PCT_BLK" ,
														 "PCT_BLKA" ,
														 "PCT_PF" ,
														 "PCT_PFD" , 
														 "PCT_PTS" ]
														     }
		pass
		

	def player_API_call(self, endpoint, return_format = 'DataFrame', sort_by_playerID = True, prune_data = True, keepIDs = True, print_url = True, *args, **kwargs):
		"""
		This function uses the SeleniumRequests Python package (see resource 1.) to perform an API GET request 
		to the stats.nba.com API. After making the request, the function then performs some processing of the 
		JSON output resulting in its output: the obtained data stored in a the data structure of the user's 
		choice.


		Parameters
		--------

			endpoint - *str*
				Specifies which endpoint of the stats.nba.com API to make GET request to. See the details section for 
				valid values. 

				The values of this parameter are not case-sensitive.

			return_format - *str* (optional, default = 'DataFrame')
				Specifies which data structure the function will organize the obtained data in. Valid values for this 
				variable are 'DataFrame' (returns the data in Pandas DataFrames), 'Array' (returns the data in NumPy 
				arrays), and 'List' (returns thedata in Python lists).

				The values of this parameter are not case-sensitive.

			sort_by_playerID - *bool* (optional, default = True)
				Determines whether or not the data structures giving the player statistics will be sorted by the 
				playerIDs which may be useful in future use of the obtained data.

			prune_data - *bool* (optional, default = True)
				Determines whether or not the obtained data will be trimmed down to throw away information not relevent 
				to this project.

			keepIDs - *bool* (optional, default = True)
				Determines whether or not the playerIDs and teamIDS will remain in the final data structures that
				this function outputs.

			print_url - *bool* (optional, default = True)
				D

			kwargs - *str*
				Keyword arguments that allow the user to specify the parameters of the Endpoint that they are trying to 
				obtain data. See the documentation for each endpoint (see Details section) for the neccessary parameters.

				The values of the keywords ARE case sensitive.


		Returns
		-------

			first_team_data - *DataFrame, Array, List*
			second_team_data - *DataFrame, Array, List*
			headers - *Array, List* (unless return_format = 'DataFrame')
				The formats of these objects can one of the following three possibilities:
			  	1. `Two pandas DataFrames <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
			  		* 2D DataFrame representing the statistics of the players on the first team; rows 
			  		  represent an individual player and columns represent a given statistic (given by the 
			  		  column header).
			  		* 2D DataFrame representing the statistics of the players on the second team; rows 
			  		  represent an individual player and columns represent a given statistic (given by the 
			  		  column header).
			  	2. `Three NumPy arrays <https://docs.scipy.org/doc/numpy/reference/generated/numpy.array.html>`_
			  		* 1D numpy array of the statistics column headers.
			  		* 2D numpy array representing the statistics of the players on the first team; rows 
			  		  represent an individual player and columns represent a given statistic.
			  		* 2D numpy array representing the statistics of the players on the second team; rows 
			  		  represent an individual player and columns represent a given statistic.
			  	3. `Three Python lists <https://docs.python.org/3/tutorial/datastructures.html>`_
			  		* 1D Python list of the statistics column headers.
			  		* 2D Python list representing the statistics of the players on the first team; rows 
			  		  represent an individual player and columns represent a given statistic.
			  		* 2D Python list representing the statistics of the players on the second team; rows 
			  		  represent an individual player and columns represent a given statistic.


		Notes
		--------

			This function can only handle the following endpoints of the stats.nba.com API (the hyperlinks
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

		See Also:
		--------

			1. `Selenium Requests Homepage <https://github.com/cryzed/Selenium-Requests>`_
		"""
		### make endpoint case-insensitive 
		endpoint = endpoint.lower()

		try:
			self.headers_to_keep_dict[endpoint]
		except KeyError:
			return "Invalid endpoint given. See the details section of this method's docstring or the supported_methods attribute for valid endpoints."

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
		dummy_var = [ kwargs_list.extend( [i[0] , i[1]] ) for i in list(self.API_params.items()) ]
		param_string = len(self.API_params)*'{}={}&'

		api_url = self.base_url + '{}?'.format(endpoint) + param_string.format(*kwargs_list)
		requests_obj = self.driver.request('GET' , api_url)
		self.last_url_called = api_url

		# if successful, format and return the data.
		if requests_obj.ok:
			if print_url:
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

			if prune_data:
				headers_to_keep = self.headers_to_keep_dict[endpoint] # this was determined beforehand.
				# define what we will keep
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

			# seperate the two teams
			first_teamID = player_stats[0][team_ID_index]
			second_teamID = player_stats[-1][team_ID_index]

			first_player_stats = [player for player in player_stats if player[team_ID_index] == first_teamID]
			second_player_stats = [player for player in player_stats if player[team_ID_index] == second_teamID]

			# order each list by player ids for convience later on (if the user desires).
			if sort_by_playerID:
				first_player_stats = sorted(first_player_stats , key = lambda x: x[player_ID_index])
				second_player_stats = sorted(second_player_stats , key = lambda x: x[player_ID_index])
			
			# determine how to output the obtained data
			if return_format.lower() == "dataframe":
				first_df = pd.DataFrame(first_player_stats, columns = stat_headers)
				second_df = pd.DataFrame(second_player_stats, columns = stat_headers)
				if not keepIDs:
					first_df = first_df.drop( ["TEAM_ID" , "PLAYER_ID"] , axis = 1 )
					second_df = second_df.drop( ["TEAM_ID" , "PLAYER_ID"] , axis = 1 )
				return first_df , second_df
			if return_format.lower() == "array":
				return np.array(stat_headers), np.array(first_player_stats), np.array(second_player_stats) 
			if return_format.lower() == "list":
				return stat_headers , first_player_stats , second_player_stats
			else:
				return "Invaid data format requested. Valid values are dataframe, array, and list."

		else:
			return 'Request to {} was not successful. \n Status code is: {}.'.format( self.last_url_called , 
																					  requests_obj.status_code )


	def team_API_call(self, endpoint, return_format = 'DataFrame', prune_data = True, keepIDs = True, print_url = True, pd_index = 0, *args, **kwargs):
		"""
		Hi


		Parameters
		--------
		
			endpoint - *str*
				Specifies which endpoint of the stats.nba.com API to make GET request to. See the details 
				section for valid values. 

				The values of this parameter are not case-sensitive.

			return_format - *str* (optional, default = 'DataFrame')
				Specifies which data structure the function will organize the obtained data in. Valid values for  
				this variable are 'DataFrame' (returns the data in Pandas DataFrames), 'Array' (returns the data 
				in NumPy arrays), and 'List' (returns thedata in Python lists).

				The values of this parameter are not case-sensitive.

			kwargs - *str*
				Keyword arguments that allow the user to specify the parameters of the Endpoint that they 
				are trying to obtain data. See the documentation for each endpoint (see Details section) 
				for the neccessary parameters.

				The values of the keywords ARE case sensitive.

			prune_data - *bool* (optional, default = True)
				Determines whether or not the obtained data will be trimmed down to throw away information not  
				relevent to this project.

			keepIDs - *bool* (optional, default = True)
				Determines whether or not the playerIDs and teamIDS will remain in the final data structures that
				this function outputs.

			print_url - *bool* (optional, default = True)
				D

			pd_index - *int* (default = 0)
				function


		Returns
		--------
			first_data - *DataFrame, Array, List*
				f
			second_data = *DataFrame, Array, List*
				f
		"""
		### make endpoint case-insensitive 
		endpoint = endpoint.lower()

		try:
			self.headers_to_keep_dict[endpoint]
		except KeyError:
			return "Invalid endpoint given. See the details section of this method's docstring or the supported_methods attribute for valid endpoints."

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
		finished = 0
		while finished == 0:
			try:
				requests_obj = self.driver.request('GET' , api_url)
				finished = 1
			except:

				sleep(5)
		self.last_url_called = api_url

		# if successful, format and return the data.
		if requests_obj.ok:
			if print_url:
				print('Request to {} was successful.'.format(self.last_url_called))

			data_dict = requests_obj.json()['resultSets'][1]
			stat_headers = data_dict['headers']
			team_stats = data_dict['rowSet']

			if prune_data:
				headers_to_keep = self.headers_to_keep_dict[endpoint]
				headers_to_keep = headers_to_keep[:1:] + ['GAME_ID'] + headers_to_keep[2::] # remove PLAYER_ID

				indices_to_keep = []
				for kept_header in headers_to_keep:
					indices_to_keep.append(stat_headers.index(kept_header))
				for list_index, team_list in enumerate(team_stats):
					team_stats[list_index] = [team_list[i] for i in indices_to_keep]

				stat_headers = headers_to_keep
				team_ID_index = 0

			else:
				team_ID_index = 1

			# seperate the two teams
			first_team_stats = team_stats[0]
			second_team_stats = team_stats[1]

			# determine how to output the obtained data
			if return_format.lower() == "dataframe":
				first_df = pd.DataFrame( np.array(first_team_stats).reshape(1 , -1) , 
										columns = stat_headers ,
										index = [pd_index] ) 
				second_df = pd.DataFrame( np.array(second_team_stats).reshape(1 , -1) , 
										columns = stat_headers , 
										index = [pd_index])
				if not keepIDs:
					first_df = first_df.drop("TEAM_ID" , axis = 1 )
					second_df = second_df.drop("TEAM_ID" , axis = 1 )
				return first_df , second_df
			if return_format.lower() == "array":
				return np.array(stat_headers), np.array(first_team_stats), np.array(second_team_stats) 
			if return_format.lower() == "list":
				return stat_headers , first_team_stats , second_team_stats
			else:
				return "Invaid data format requested. Valid values are dataframe, array, and list."


		else:
			return 'Request to {} was not successful. \n Status code is: {}.'.format( self.last_url_called , 
																					  requests_obj.status_code )

	def game_results_API_call(self, season_year, team_abbreviation, *args, **kwargs):
		"""
		Hi


		Parameters
		--------

			season_year - *str*
			team_abbreviation - *str*


		Returns 
		--------

			hi


		See Also
		--------

		1. `Numpy Flip function <https://docs.scipy.org/doc/numpy/reference/generated/numpy.flip.html>`_
		"""
		teamID = self.teamIDS_dict[team_abbreviation]

		api_url = self.base_url + 'teamgamelog?SeasonType=Regular+Season&Season={}&TeamID={}'.format(season_year , teamID)
		self.API_params = { 'Season' : season_year , 
							'SeasonType' : 'Regular+Season&Season' , 
							'TeamID' : teamID }

		response_obj = self.driver.request('GET' , api_url)
		self.last_url_called = api_url

		def WL_converter(arr):
			if arr[-1] == 'W':
				arr[-1] = 1
			elif arr[-1] == 'L':
				arr[-1] = 0

			return arr

		if response_obj.ok:
			# print('Request to {} was successful.'.format(self.last_url_called))

			season_data = response_obj.json()['resultSets'][0]['rowSet']
			game_results = np.flip(np.array(season_data)[:,[0 , 1 , 4]] , axis = 0)

			if season_year == '2012-13' and team_abbreviation == 'BOS':
				game_results = np.delete(game_results , -2 , axis = 0)
			if season_year == '2012-13' and team_abbreviation == 'IND':
				game_results = np.delete(game_results , -2 , axis = 0)

			game_results = np.apply_along_axis(WL_converter , axis = 1 , arr = game_results)
			game_results_df = pd.DataFrame(game_results , columns = ['TEAM_ID' , 'GAME_ID' , 'RESULT']).astype({'TEAM_ID' : str , 'GAME_ID' : str , 'RESULT' : int})

			return game_results_df

		else:
			return 'Request to the teamgamelog endpoint failed with status code: {}. \n Attemped URL was: {}'.format(response_obj.status_code , self.last_url_called)


	def game_data_compiler(self, GameID, player_data = True, pd_index = 0, print_url = True, *args, **kwargs):
		"""
		Make several calls to the NBA API and concatenate the resulting outputs in order to have a single data 
		structure that contains all of the information we need to train our neual networks.
		

		Parameters
		--------

			GameID - *str*
				The GameID parameter of the game that we wish to obtain boxscore data for from the NBA Stats API.

			player_data - *bool* (default = True)
				Determines whether or not we will compile all of the player or team data from a specified game. Team
				data will be compiled when player_data = False and player data otherwise.

			pd_index - *int* (default = 0)
				f

			print_url - *bool* (optional, default = True)
				D

			kwargs - *list of strings*
				Keyword arguments that allow the user 
		

		Returns 
		--------
			final_first_df - *DataFrame*
			final_second_df - *DataFrame*
		"""
		first_dfs_list = []
		second_dfs_list = []
		if kwargs:
			endpoints = list(kwargs.values())
		else:
			endpoints = [ 'boxscoreadvancedv2' , 
						  'boxscorefourfactorsv2' , 
						  'boxscoremiscv2' , 
						  'boxscorescoringv2' , 
						  'boxscoretraditionalv2' , 
						  'boxscoreusagev2' ]

		if player_data: # compiling player data for the specified game
			for box_index , boxscore in enumerate(endpoints):
				if box_index == 0:
					first_df , second_df = self.player_API_call(endpoint = boxscore, GameID = GameID, keepIDs = True, print_url = print_url)
				else:
					first_df , second_df = self.player_API_call(endpoint = boxscore, GameID = GameID, keepIDs = False, print_url = print_url)
				first_dfs_list.append(first_df)
				second_dfs_list.append(second_df)

			final_first_df = pd.concat(first_dfs_list , axis = 1)
			final_second_df = pd.concat(second_dfs_list , axis = 1)

		else: # compiling team data for the specified game
			for box_index , boxscore in enumerate(endpoints):
				if box_index == 0:
					first_df , second_df = self.team_API_call(endpoint = boxscore, GameID = GameID, keepIDs = True, pd_index = pd_index, print_url = print_url)
				else:
					first_df , second_df = self.team_API_call(endpoint = boxscore, GameID = GameID, keepIDs = False, pd_index = pd_index, print_url = print_url)
					first_df = first_df.drop("GAME_ID" , axis = 1)
					second_df = second_df.drop("GAME_ID" , axis = 1)
				first_dfs_list.append(first_df)
				second_dfs_list.append(second_df)

			final_first_df = pd.concat(first_dfs_list , axis = 1)
			final_second_df = pd.concat(second_dfs_list , axis = 1)

		return final_first_df , final_second_df

	def season_data_compiler(self, season_year, team_abbreviation, give_player_data = True, *args, **kwargs):
		"""
		Compiles all of the data for a specified NBA team for a specified season year.
		

		Parameters
		--------
			season_year - *str*
				A string object that specifies which season the user would like to obtain data frome. The format
				of this string is the usual NBA season format: 'YYYY-YY' such as '2018-19'.

			team_abbreviation - *str*
				A string object which tells the function which team to get data for. 

				All team abbreviations are the usual NBA ones (as seen in game telecasts). If the user is unsure 
				of the offical abbreviation for a given team, they can check the keys of the teamIDS_dict 
				attribute of this class. In fact, that class is used to obtain the team ID of the specified team.

			give_player_data - *bool* (default = True)
				A boolean object that determines whether the function will return player statistics or team 
				statistics. If true, then player statistics for each game are given and if false, then team 
				statistics are given instead.


		Returns 
		--------
			season_df - *DataFrame*
				A Pandas DataFrame that contains all of the statistics for the team from the specified season.

				If the user is obtaining team stats from this season, then the DataFrame will be a typical 2D
				one where each row specifies a game (whose index is given by the game number - 1 since the 
				indexing starts at 0) and each column represents a given statistic.

				If the user is obtaining player stats from this season, then the returned DataFrame will be 
				three-dimensional where a game index (again, game number - 1) specifies a 2D DataFrame that 
				contains all of the player statistics for that game; each row in the 2D DataFrame represents a
				player and each column represents a statistic.


		See Also
		--------
		1. `Pandas Concat Function Documentation <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html>`_
		2. `Concatenation of 2D Pandas DataFrames <https://jakevdp.github.io/PythonDataScienceHandbook/03.06-concat-and-append.html>`_
		3. `Dealing with hierarchical Pandas DataFrames <https://jakevdp.github.io/PythonDataScienceHandbook/03.05-hierarchical-indexing.html>`_
		"""
		### Make API request to teamgamelog endpoint to get gameIDs for specified team's season to easily get
		### all of the season data.
		teamID = self.teamIDS_dict[team_abbreviation]

		api_url = self.base_url + 'teamgamelog?SeasonType=Regular+Season&Season={}&TeamID={}'.format(season_year , teamID)
		self.API_params = { 'Season' : season_year , 
							'SeasonType' : 'Regular+Season&Season' , 
							'TeamID' : teamID }

		response_obj = self.driver.request('GET' , api_url)
		self.last_url_called = api_url

		if response_obj.ok:
			# print('Request to {} was successful.'.format(self.last_url_called))

			season_data = response_obj.json()['resultSets'][0]['rowSet']
			gameIDs = np.flip(np.array(season_data)[:,1]).tolist()

			if season_year == '2012-13' and team_abbreviation == 'BOS' or season_year == '2012-13' and team_abbreviation == 'IND':
				gameIDs.remove('0021201214')

			num_games = len(gameIDs)

		else:
			return 'Request to the teamgamelog endpoint failed with status code: {}. \n Attemped URL was: {}'.format(response_obj.status_code , self.last_url_called)

		### Now use gameIDs list to iterate over all of the games in the specified season to get the desired data.
		if give_player_data:
			player_dfs_list = []
			for game_index , gameID in enumerate(gameIDs):  
				# the NBA organizes the games in the teamgamelog endpoint in REVERSE ORDER which is NOT what we
				# want.
				dfs_tuple = self.game_data_compiler( GameID = gameID , 
													 player_data = True,  
													 print_url = False )
				for df in dfs_tuple:
					if str( int(df.iloc[0]['TEAM_ID']) ) == teamID:
						player_dfs_list.append(df)
				print('\tCompiled data from {}/{} games'.format(game_index+1 , num_games))

			season_df = pd.concat(player_dfs_list , keys = list( range(len(player_dfs_list)) ))

			return season_df

		else:
			team_dfs_list = []
			for game_index , gameID in enumerate(gameIDs):
				# make the API call for the game. We DO NOT need data from the usage boxscore endpoint for teams
				# beacuse the values for all of them are 1. No need to download (and eventually give the neural
				# network) more information if we don't need it. Especially since this will mean 82 less runs of
				# the team_API_call method above speeding up the compilation process!
				dfs_tuple = self.game_data_compiler( GameID = gameID , 
													 player_data = False, 
													 pd_index = game_index, 
													 print_url = False,
													 endpoint_one = 'boxscoreadvancedv2' , 
						  							 endpoint_two = 'boxscorefourfactorsv2' , 
						  							 endpoint_three = 'boxscoremiscv2' , 
						  							 endpoint_four = 'boxscorescoringv2' , 
						  							 endpoint_five = 'boxscoretraditionalv2' )
				for df in dfs_tuple:
					if str( int(df.iloc[0]['TEAM_ID']) ) == teamID:
						team_dfs_list.append(df)
				print('\tCompiled data from {}/{} games'.format(game_index+1 , num_games))

			season_df = pd.concat(team_dfs_list , axis = 0)

			return season_df

		
	def close_driver(self, *args, **kwargs):
		"""
		Quit the webdriver that was opened up when the class was instantiated.
		"""
		self.driver.quit()
		pass

### Execute
if __name__ == '__main__':
	### additional neccessary import statements.
	import os

	### message for the user.
	print("Running the script directly.")

	### initial instantsiation of the class to get teams_list
	api_caller = nba_stats_API()

	### make years and teams list.
	years_list = ['20{}-{}'.format(i , i+1) for i in range(18 , 9 , -1)] + ['2009-10'] + ['200{}-0{}'.format(i , i+1) for i in range(8 , 3 , -1)]
	teams_list = list(api_caller.teamIDS_dict.keys())

	### close driver. Will instantiate the class again below.
	api_caller.close_driver()

	### get the game results
	change to the directory where the game results files will be saved
	final_path = '/Users/sebas12/Documents/Python/sports_betting/data/processed/game_results'
	os.chdir(final_path)

	# get the data iteratively 
	for year in years_list:
		print('Getting game results data for the {} season.'.format(year))

		api_caller = nba_stats_API()

		save_year = year[2:4] + year[5::]
		starting_index = 0
		ending_index = 30
		team_iter_index = starting_index

		for team in teams_list[starting_index:ending_index:]:
			print('   Obtaining game results data for {} ({}/30)'.format(team , team_iter_index + 1))
			game_results_df = api_caller.game_results_API_call(season_year = year , team_abbreviation = team)

			if team_iter_index == 0:
				game_results_df.to_hdf('{}_game_results.h5'.format(save_year) , key = team , mode = 'w')
			else:
				game_results_df.to_hdf('{}_game_results.h5'.format(save_year) , key = team , mode = 'a')
			team_iter_index += 1

		api_caller.close_driver()


	### get the team data.
	# change to the directory where the team files will be saved
	final_path = '/Users/sebas12/Documents/Python/sports_betting/data/interim/team_data'
	os.chdir(final_path)

	# get the data iteratively 
	for year in years_list:
		print('Getting team data for the {} season.'.format(year))

		save_year = year[2:4] + year[5::]

		starting_index = 0
		ending_index = 30

		team_iter_index = starting_index

		for team in teams_list[starting_index:ending_index:]:
			# instantiate the class for each team because of timing out issues that lead to the webdriver getting
			# hung up indefinetly (despite efforts to add time_out exceptions above...).
			api_caller = nba_stats_API()
			print('   Obtaining team data for {} ({}/30)'.format(team , team_iter_index + 1))
			team_df = api_caller.season_data_compiler( season_year = year, 
													   team_abbreviation = team, 
													   give_player_data = False )
			if team_iter_index == 0:
				team_df.to_hdf('{}_team_data.h5'.format(save_year), key = team, mode = 'w')
			else:
				team_df.to_hdf('{}_team_data.h5'.format(save_year), key = team, mode = 'a')
			api_caller.close_driver()
			team_iter_index += 1

	### get the player data.
	change to the directory where the player files will be saved
	final_path = '/Users/sebas12/Documents/Python/sports_betting/data/interim/player_data'
	os.chdir(final_path)

	# get the data iteratively
	for year in years_list:
		print('Getting player data for the {} season.'.format(year))

		save_year = year[2:4] + year[5::]

		starting_index = 0
		ending_index = 29

		team_iter_index = starting_index

		for team in teams_list[starting_index:ending_index:]:
			# instantiate the class for each team because of timing out issues that lead to the webdriver getting
			# hung up indefinetly (despite efforts to add time_out exceptions above...).
			api_caller = nba_stats_API()
			print('   Obtaining player data for {} ({}/30)'.format(team , team_iter_index + 1))
			players_df = api_caller.season_data_compiler( season_year = year, 
													      team_abbreviation = team, 
													      give_player_data = True )
			if team_iter_index == 0:
				players_df.to_hdf('{}_game_data.h5'.format(save_year), key = team, mode = 'w')
			else:
				players_df.to_hdf('{}_game_data.h5'.format(save_year), key = team, mode = 'a')
			api_caller.close_driver()
			team_iter_index += 1



