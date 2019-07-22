#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Wed Jul 17 11:25:47 2019
# @author: sebas12


### Neccessary import statements
import numpy as np
import requests as req
import pandas as pd

### Define Class
class nba_stats_API:
	def __init__(self, *args, **kwargs):
		self.base_url = kwargs.get('base_url' , 'https://stats.nba.com/stats/')
		self.headers = kwargs.get('headers' , { 
											    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
									            "Accept-Encoding": "gzip, deflate, br",
									            "Accept-Language": "en-US,en;q=0.9",
									            "Cache-Control": "max-age=0",
									            "Connection": "keep-alive",
									            "Cookie": "AMCVS_248F210755B762187F000101%40AdobeOrg=1; check=true; ug=5d0cd3b10b83700a3f860700164715d4; _ga=GA1.2.412748446.1561143701; s_cc=true; AMCVS_7FF852E2556756057F000101%40AdobeOrg=1; s_vi=[CS]v1|2E8694CB0507E274-6000011AE000E29F[CE]; s_ecid=MCMID%7C14709208357575941801497752433680962893; __gads=ID=c21c4efceb03c255:T=1561143702:S=ALNI_MYlaJ_C1OWNfhTea7WQWR_VN2qJGQ; _fbp=fb.1.1561143705102.1785013179; cto_lwid=97a29d31-7332-444a-b662-fce0eaadd644; s_sq=%5B%5BB%5D%5D; AMCV_248F210755B762187F000101%40AdobeOrg=1687686476%7CMCIDTS%7C18096%7CMCMID%7C14707037169098885711497493531647293234%7CMCAAMLH-1564017749%7C9%7CMCAAMB-1564017749%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1563420149s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.0.0; _gid=GA1.2.1207795445.1563412951; ugs=1; AMCV_7FF852E2556756057F000101%40AdobeOrg=1687686476%7CMCIDTS%7C18096%7CMCMID%7C14709208357575941801497752433680962893%7CMCAAMLH-1564017752%7C9%7CMCAAMB-1564017752%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1563420152s%7CNONE%7CMCAID%7C2E8694CB0507E274-6000011AE000E29F%7CvVersion%7C3.0.0; mbox=PC#4c40b03a69be4bc586d4e55f1f721b18.17_73#1626657751|session#b6d45e6c7f374f8b97e480c6fac59d3a#1563414891; ak_bmsc=96F503DCD06356E21EB5030CE24502C3172B394F4A530000F4AD305D64229650~plADQOl1yH7Kos8l5RXyQgKQ620Ko2Xd338nG84590Yj0Hmb+ChuMhgCBxXt6pE8yuZgspZzoH0LhdWZoFNqHALc+UDWwAx2JREDrRm3YwpDcMDVB4rTx88xk4jJWDdnE7YEmNZ4B+9H3ienjLw9BAS3JQBLF/XwnSvBCMqmSRokW4bAofEYcWICfZOp4LYgIAvJRqDsEEo1b8QOa+H/3mYXMVj0oM8tYoiUhq4bW5viZkVHUADihKwAw+B2dKIvNj; bm_sv=C19BA976DED9B6990B5F6A89F0980852~OPAyhc5unNYzr4TYvgHKfau6n4B0lNanvfBWGrluEvXt6XE/5H+WRq+T0UGliQiBg4gb3skqrBCPdGK4eVrn4coQZ/sFLdlTB94XKx79U+qO7gAXvWVwKGwKGbVAGMobWtuDdvyZu3kZrDKQFC0E5Q==",
									            "Host": "stats.nba.com",
									            "Upgrade-Insecure-Requests": "1",
									            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Mobile Safari/537.36"
        				}  )

	def player_API_call(self, endpoint, *args, **kwargs):
		"""
		:Purpose: 

		:Details:

		:type args:
		:param args:

		:type kwargs:
		:param kwargs:

		:type endpoint:
		:param endpoint:

		:returns: 

		:Useful Resources: 1.
						   2.
		"""
		### Determine which endpoint we will be useing
		if endpoint == 'boxscoreadvancedv2':
			# define what we will keep
			dict_keys_to_keep = [ "MIN" , 
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
								  "PIE" ]
			# set the neccessary parameters
			try: 
				kwargs['GameID']
			except KeyError:
				print('Incorrect usage of kwargs; No valid value for GameID is given. \n This is the one required keyword argument. \n Check to see if the right letters are capitalized.')

			if len(kwargs) == 1: 
				# that is, user only passed in a value for GameID (the one required keyword argument).
				kwargs['EndPeriod'] = 0
				kwargs['EndRange'] = 0
				kwargs['RangeType'] = 0
				kwargs['StartPeriod'] = 0
				kwargs['StartRange'] = 0
			elif 1 < len(kwargs) < 6:
				# this is, user passed in more keywords than just GameID, but NOT all
				all_params = ['GameID', 'EndPeriod', 'EndRange', 'RangeType', 'StartPeriod', 'StartRange']
				for param in list(kwargs.keys()):
					all_params.remove(param)
				for param in all_params:
					kwargs[param] = 0

			elif len(kwargs) == 6:
				# that is, user passed in a value for all of this endpoints parameters
				kwargs = kwargs
			else:
				# that is, user passed in too many keyword arguments.
				return 'Too many values were passed into **kwargs. \n {} does not have that many parameters. \n {} parameters were given when {} only takes 6.'.format(endpoint , len(kwargs) , endpoint)

			# define the URL
			kwargs_list = []
			_ = [ kwargs_list.extend( [i[0] , i[1]] ) for i in list(kwargs.items()) ]
			api_url = self.base_url + '{}?'.format(endpoint) + len(kwargs)*'{}={}&'.format(*kwargs_list)
			requests_obj = req.get(api_url , headers = self.headers)

			if requests_obj.status_code == 200:
				return('Request was successful.')
			else:
				return('Request was not successful. Status code is: {}.'.format(requests_obj.status_code))

		# if endpoint == '':
		# 	# define what we will keep
		# 	dict_keys_to_keep = []

		# if endpoint == '':
		# 	# define what we will keep
		# 	dict_keys_to_keep = []
		# 	# set the neccessary parameters
		# 	# define the URL

		# if endpoint == '':
		# 	# define what we will keep
		# 	dict_keys_to_keep = []
		# 	# set the neccessary parameters
		# 	# define the URL

		# if endpoint == '':
		# 	# define what we will keep
		# 	dict_keys_to_keep = []
		# 	# set the neccessary parameters
		# 	# define the URL

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

### Execute
if __name__ == '__main__':
	print("Running script directly.")
