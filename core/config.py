####################################
#
# Databases project - Core Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			20 - 02 - 2015
#
####
#
# Filename:		config.py
# Description:	Defines the configuration object, used to configure the system
#
####################################

from __future__ import print_function
import utils
import json
import os
import sys

class Config(object):
	'''Configuration object to hold data about the current configuration'''
	def __init__(self, filename='config.json', debug=False):
		'''
		Initialize the configuration object.
		'''
		self.config_file = filename
		self.new_config = False
		# Check if we have a configuration file
		if os.path.isfile(filename):
			self.config_dict = self.get_config(debug)
		# else, create one
		else:
			self.config_dict = self.setup()
			self.new_config = True

	def get_config(self, debug):
		'''
		Get the configuration details from the configuration file.
		Those details include database logins, different options and more.
		Note: The configuration file is expected to be a JSON file.
		'''
		data = None
		json_data = None
		try:
			# Read the raw configuration file
			with open(self.config_file, 'r') as file:
				data = file.read()
			
			# Try to get the JSON data
			json_data = json.loads(data)

			# Return the parsed data
			return json_data

		except Exception, e:
			# Inform the user about the error and quit
			utils.error(e, 'Error while reading configuration file.', 'get_config', True)

	def setup(self):
		'''
		Create a configuration file
		'''
		# Tell the user what is happening
		print('Welcome to your new system!')
		print('Since we couldn\'t find a configuration file, let\'s create one!')

		# Get the DB's details
		db = self.get_db_details()

		# Get the other configuration details
		config = self.get_config_details(db)

		# Save to file
		self.save_config(config)

		# return the configuration dict
		return config

	def get_db_details(self):
		'''
		Get the DB's details from the user
		'''
		# Default values
		db = {
			'host' : 'localhost',
			'username' : None,
			'password' : None,
			'name' : None,
			'port' : 3306
		}

		# Get the details from the user
		db = utils.get_dict(db, 'Database')
		# return the dictionary
		return db


	def get_config_details(self, db):
		'''
		Get the configuration details from the user
		Parameters:
			- db (dictionary): the dict created in self.get_db_details()
		'''

		# Default values
		config = {
			'title' : None,
			'currency' : '$'
		}

		# Get the details from the user
		config = utils.get_dict(config, 'System')

		# Ask the user if he want to set debug mode
		debug = raw_input('Would you like to set debug mode on? (Y/N):')

		# Check the input
		if debug.lower() == 'y':
			print('Debug mode is now on.')
			debug = True

		else:
			debug = False

		# Set the debug mode
		config['debug'] = debug

		# Set the Database variable
		config['db'] = db

		return config


	def save_config(self, config):
		'''
		Save the configuration to a file
		Parameters:
			- config (dict): the dictionary created in self.get_config_details()
		'''
		# Create the json object
		config_json = json.dumps(config)

		# Save to file
		try:
			with open(self.config_file, 'w') as file:
				file.write(config_json)
		
		# Inform users about exceptions
		except Exception, e:
			# We don't use a logger because this module dosen't have one :(
			print('Error while saving configuration file. Please try again.')
			if config['debug']:
				print('Exception: %s' % str(e))
			# This is a fatal error. Quit.
			sys.exit(1)

	def __getattr__(self, name):
		'''
		Get atteribute from the config details.
		Parameters:
			- name (str): The attribute requested
		'''
		# A special case: we are asked for the entire configuration data
		if name == 'config_dict':
			return self.config_dict

		# Else, check if the required attribute is in the configuration keys
		# This allows for 'Config.x'
		if name in self.config_dict.keys():
			return self.config_dict[name]

		# Else, check if it's in a sub-dict
		# This allows for 'Config.x.y' to be retrived by 'Config.y'
		for value in self.config_dict.values():
			if isinstance(value, dict) and name in value.keys():
				return value[name]

		# else, check if it's an actual attribute
		if name in self.__dict__.keys():
			return self.__dict__[name]

		# Finally, if there is no such key, raise a KeyError
		raise KeyError('No attribute named %s' % str(name))






