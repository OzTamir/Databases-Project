####################################
#
# Databases project - Main Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			20 - 02 - 2015
#
####
#
# Filename:		system.py
# Description:	This is the main object, representing the whole project
#
####################################

from __future__ import print_function
from config import Config
from database import Database
from ui import UIManager

# Import the modules in which there are global variables
import utils
import ui.ui_utils as ui_utils

class System(object):
	''' The main object, representing the BMS (Bakery Managment System)'''
	def __init__(self, config_file):
		'''
		Initialize all the objects and set global variables
		Parameters:
			- config_file (str): the name of the configuration file
		'''
		try:
			# Create a Config object
			self.conf = Config(config_file, True)
			# Create a Database object
			self.db = Database(self.conf)
			
			# Set global variables
			self.set_global(self.db, self.conf)
			
			# Create a UIManager object
			self.ui_manager = UIManager(self.db, self.conf)
		
		except Exception, e:
			print('Error in system init. Aborting...')

	def set_global(self, db, config):
		'''
		Set global variables in modules that are not classes
		Parameters:
			- db (Database): The Database object
			- config (Config): The Config object
		'''
		ui_utils.db = db
		utils.config = config















