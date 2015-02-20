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
# Filename:		ui_manager.py
# Description:	This file defines a UI Manager class, 
#				which is the main object used in UI context
#
####################################

import ui_utils
from core.utils import error
from views import NewPurchaseView
from main_menu import MainMenu
import sys

def lol():
	print('lol')

class UIManager(object):
	''' UIManager is the main object used in UI context '''
	def __init__(self, db, config):
		'''
		Create a UI object and set it's properties
		'''
		# Set the DB object
		self.db = db
		# Set the Configuration object
		self.config = config

		# Set the views
		self.new_purchase = NewPurchaseView(db)
		self.new_order = lol

		# Set the menus
		self.main_menu = MainMenu(config, self)

		# Keep a log of menus hierarchy
		# This is used like a stack of views
		self.stack = [self.main_menu]

	def __call__(self):
		'''
		Make UIManager callable.
		This will run the top (last) item from the stack list
		and will pop it. If the stack is empty, it will quit the program.
		'''
		# If the view stack is empty, than there is nowhere to return to and we
		# will quit the program.
		if len(self.stack) == 0:
			# Inform the user
			print('Shutting down...')
			# Close the connection to the database
			self.db.close_connection()
			# Quit
			sys.exit(0)
		
		# Get the view
		view = self.stack.pop(-1)
		# Try to call the view
		try:
			view()
		# If it's not callable, something went wrong and we need to quit
		except Exception, e:
			error(e, 'Error: View is not callable', 'UIManager.__call__', True)





