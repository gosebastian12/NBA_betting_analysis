#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Wed Jul 17 11:25:47 2019
# @author: sebas12


### Neccessary import statements
import numpy as np
import pandas as pd
import os

### Define Class
class data_cummulation:
	"""
	Hi


	Attributes
	--------

	1. 


	Parameters
	--------
		path_to_data - *str* (default = data/interim)

		kwargs - **


	See Also
	--------

	1.
	"""
	def __init__(self, path_to_data = 'data/interim/', *args, **kwargs):
		self.project_root = '/Users/sebas12/Documents/Python/sports_betting/'
			# this is of course assuming that you have kept this file in the ../src/features sub-directory of 
			# the project.
		self.data_loc = self.project_root + path_to_data
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
		self.per_min_stats = [ 'PTS_OFF_TOV',
							   'PTS_2ND_CHANCE',
							   'PTS_FB',
							   'PTS_PAINT',
							   'OPP_PTS_OFF_TOV',
							   'OPP_PTS_2ND_CHANCE',
							   'OPP_PTS_FB',
							   'OPP_PTS_PAINT',
							   'BLK',
							   'BLKA',
							   'PF',
							   'PFD',
							   'FGM',
							   'FGA',
							   'FG3M',
							   'FG3A',
							   'FTM',
							   'FTA',
							   'OREB',
							   'DREB',
							   'REB',
							   'AST',
							   'STL',
							   'TO',
							   'PTS' ]

		pass

	def load_in_df(self, file_name, df_key, player_data = True, *args, **kwargs):
		"""
		Hi


		Parameters
		--------
			file_name - *str*

			df_key - *str*

			player_data - *bool* (default = True)
		

		See Also
		--------

		1.
		"""
		try:
			file_name.index('.')
		except ValueError:
			file_name += '.h5'

		if player_data:
			path_to_data = self.data_loc + "player_data"
			os.chdir(path_to_data)

		else:
			path_to_data = self.data_loc + "team_data"
			os.chdir(path_to_data)

		df = pd.read_hdf(file_name , key = df_key)

		return df

	def type_converter(self, file_name, df_key, player_data = True, *args, **kwargs):
		"""
		Hi


		Parameters
		--------
			file_name - *str*

			df_key - *str*

			player_data - *bool* (default = True)
		

		See Also
		--------

		1.
		"""
		if player_data:
			df = self.load_in_df(file_name, df_key)

		else:
			df = self.load_in_df(file_name, df_key, player_data = False)

		df['MIN'] = df['MIN'].apply( lambda x: int(x[:3:]) // 5 )

		stats_list = list(df.columns)[3::]
		type_dict = dict( zip(stats_list , [float]*len(stats_list)) )

		return df.astype(type_dict)


	def per_minute_norm(self, file_name, df_key, player_data = True, *args, **kwargs):
		"""
		Hi


		Parameters
		--------

			file_name - *str*

			df_key - *str*
			
			player_data - *bool* (default = True)

			kwargs - *str object(s)*
		

		See Also
		--------

		1.
		"""
		if kwargs:
			stats_to_norm = list(kwargs.values())

		else:
			stats_to_norm = self.per_min_stats

		if player_data:
			new_df = self.type_converter(file_name, df_key, player_data = True)

		else:
			new_df = self.type_converter(file_name, df_key, player_data = False)

		for stat in stats_to_norm:
			new_df[stat] = new_df[stat].divide(new_df['MIN'])

		return new_df


	def cumavg(self, file_name, df_key, player_data = True, *args, **kwargs):
		"""
		Hi


		Parameters
		--------
		
			file_name - *str*

			df_key - *str*
			
			player_data - *bool* (default = True)

			kwargs - *str object(s)*
		

		See Also
		--------

		1.
		"""
		if player_data:
			cum_df = self.per_minute_norm(file_name , df_key , player_data = True)
		else:
			cum_df = self.per_minute_norm(file_name , df_key , player_data = False)

		num_games_series = pd.Series(np.arange(1 , 82))
		cum_df.iloc[:,2:] = cum_df.iloc[:,2:].cumsum(axis = 0).divide(num_games_series , axis = 0)

		return cum_df

	def save_cum_df(self, file_name, df_key, player_data = True, *args, **kwargs):
		"""
		Hi


		Parameters
		--------
		
			file_name - *str*

			df_key - *str*
			
			player_data - *bool* (default = True)

			kwargs - *str object(s)*
		

		See Also
		--------

		1.
		"""
		pass


if __name__ == '__main__':
	pass

