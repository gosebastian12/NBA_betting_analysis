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

	def api_call(self, endpoint, *args, **kwargs):
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
		if endpoint == 'boxscoreadvancedv2':
			dict_keys_to_keep = []

		if endpoint == '':
			dict_keys_to_keep = []

		if endpoint == '':
			dict_keys_to_keep = []

		if endpoint == '':
			dict_keys_to_keep = []

		if endpoint == '':
			dict_keys_to_keep = []

### Execute
if __name__ == '__main__':
	print("Running script directly.")
