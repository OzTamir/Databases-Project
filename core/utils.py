####################################
#
# Databases project - UI Package
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


def read(prompt, type_expected=None):
	'''
	Read information from the user, and check for type
	Parameters:
		- prompt (str): The message asking the user for input
		- type_expected (type): the type of which the input should be
	'''
	data = input(prompt)
	# If the caller don't care about the type or the type is correct, return
	if type_expected is None or isinstance(data, type_expected):
		return data

	# Else, ask for input again
	print('Please enter data of type %s' % str(type_expected))
	return read(prompt, type_expected)







