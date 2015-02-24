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
# Filename:		utils.py
# Description:	Defines various utility functions
#
####################################
import logging
import sys


# Global Variables
config = None

def get_debug():
	'''
	Make sure we have a debug
	'''
	# If config is None, print an error and return True
	if config is None:
		print('Utils.py: config is None')
		return True

	# Else, return the value
	return config.debug

def error(exception, msg, location, fatal=False, error_code=1):
	'''
	Print message about an exception.
	If the debug flag is true in the config file, print additional data.
	Parameters:
		- exception (Exception): the exception caught
		- msg (str): Short message to describe what happened
		- location (str): Where in the code the exception happened
		- fatal (bool): If the error was so fatal, we need to exit the program
	'''
	# Print the error message
	if msg != '':
		print(str(msg))

	# If we are in debug mode, print additonal information
	if get_debug():
		print('Debug Information')
		print('Error location:	%s' % str(location))
		print('Error Type:		%s' % str(type(exception)))
		print('Error Data:		%s' % exception.message)

	# If the error is fatal, quit
	# TODO: Define error codes
	if fatal:
		sys.exit(error_code)

def get_dict(default_dict, label):
	'''
	Populate default_dict with values from the user
	Parameters:
		- default_dict (dict): a dictionary with the requested keys and 
								a default value (or None if there isn't one)
		- label (str): the thing whose details we ask the user for
	'''
	# Ask the user for details
	for key, item in default_dict.items():
		# If we don't have a default values
		if item is None:
			value = ''
			# This is a while loop to ensure we get a value
			while value == '':
				value = raw_input('Please enter the %s\'s %s (Required):' \
									% (str(label), str(key.title())))
		# If we have a default value
		else:
			value = raw_input('Please enter the %s\'s %s (Default: %s):' \
								% (str(label), str(key), str(item)))
			# If there was no value given, set it to the default
			if value == '':
				value = item

		# If the item is a number, cast it to int
		if isinstance(value, str) and value.isdigit():
			value = int(value)

		# Finally, set the item in the dictionary to the input value
		default_dict[key] = value

	return default_dict

def get_logger(name, level=None):
	'''
	Return a logging.Logger object that can output to stdout
	Parameters:
		- name (str): the logger name
		- level (logging.LEVEL): the level of the logger
		- format (str): the string for the formatter
	'''
	if level is None:
		if get_debug():
			level = logging.DEBUG
		else:
			level = logging.WARNING

	# Get the logger
	log = logging.getLogger(name)
	# Create a handler to output to stdout
	output_handlr = logging.StreamHandler(sys.stdout)
	# Set the formatter
	if level == logging.DEBUG:
		output_handlr.setFormatter(logging.Formatter(\
			'(%(asctime)s) %(name)s - %(module)s.%(funcName)s (Line %(lineno)d): %(message)s', '%H:%M:%S'))
	# If we are not in debug mode, only print the error
	else:
		output_handlr.setFormatter(logging.Formatter('%(message)s'))
	# Set the level for the output handler
	output_handlr.setLevel(level)
	# Add the handler
	log.addHandler(output_handlr)
	# Set the level for the logger
	log.setLevel(level)
	# Return the logger
	return log







