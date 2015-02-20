from __future__ import print_function
import utils
import json
import sys

class Config(object):
	'''Configuration object to hold data about the current configuration'''
	def __init__(self, filename='config.json', debug=False):
		'''
		Initialize the configuration object.
		'''
		self.config_file = filename
		self.config_dict = self.get_config(debug)

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

		# Finally, if there is no such key, raise a KeyError
		raise KeyError('No attribute named %s' % str(name))






