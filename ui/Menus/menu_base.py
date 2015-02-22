####################################
#
# Databases project - UI.Menus Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			20 - 02 - 2015
#
####
#
# Filename:		menu_base.py
# Description:	This file defines the base class for menus
#
####################################

import ui.ui_utils
import core.utils as utils

class MenuBase(object):
	'''
	A Base class for menus
	'''

	def __init__(self, options_list, config, should_loop=False):
		'''
		Initialize a menu object
		Parameters:
			- options_list (list of tuples): List from the form [(label, function)]
			- config (Config): Configuration object
		'''
		# Save the configuration
		self.conf = config
		
		# The signal returned upon sucsesful run
		self.should_loop = should_loop

		# Save the options list
		self.options = options_list
		
		# Save the labels and the actions
		self.options_labels = [option[0] for option in options_list]
		self.options_actions = [option[1] for option in options_list]

		# This signal when the user wants out
		self.exit_code = len(self.options_labels) + 1

	def __call__(self):
		'''
		Make menus callable
		'''
		self.run_menu()

	def print_options(self):
		'''
		Print the options of the menu
		'''
		# Print a newline
		print('')
		
		# Instruct the user
		print('Choose an action:')
		
		# Print all the available options
		for index, option in enumerate(self.options_labels):
			print('%d. %s' % (index + 1, option))

		# Add an option to exit
		print('%d. Exit' % (len(self.options_labels) + 1))

	def get_choice(self):
		'''
		Get the user's choice
		'''

		# Get input from the user
		choice = raw_input('Please enter the number of your choice: ')
		
		# Make sure that we got a valid input
		if not (choice.isdigit() and int(choice) - 1 <= len(self.options_labels)):
			# If not, print an error and try again using recursion
			print('Please enter a valid choice.')
			return self.get_choice()

		# If it's valid, return the choice as an int
		return int(choice)

	def do_action(self, choice):
		'''
		Run an action based on user choice
		Parameters:
			- choice (int): the return value of self.get_choice()
		'''
		# The user is requesting the N + 1 action (+1 to avoid showing 0)
		action = choice - 1

		# Run the requested action
		try:
			# Run the requested action
			self.options_actions[action]()
			# Return sucsess code
			return 0
		
		# If we are out of index, the user want to quit
		except IndexError:
			return -1
		
		except Exception, e:
			# Print an error message
			utils.error(e, 'Error while running action %s' % \
						str(self.options_labels[action]), 'Menu.do_action()')
			# Return an error code
			return -2

	def run_menu(self):
		'''
		Run the entire menu flow
		'''
		# Print the options
		self.print_options()

		# Get the user's choice
		choice = self.get_choice()

		# Check if the user is trying to quit
		if choice == self.exit_code:
			return

		# Run the asked action
		ret_signal = self.do_action(choice)

		# If there was an error, try again
		if ret_signal == -2:
			print('Please try again.')
			return self.run_menu()

		# If we should loop, loop
		if self.should_loop:
			return self.run_menu()

