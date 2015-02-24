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
# Filename:		system.py
# Description:	This is the main object, representing the whole system
#
####################################

from __future__ import print_function
import logging
import sys

from config import Config
from database import Database
from ui import UIManager

# Import the modules in which there are global variables
import utils
import ui.ui_utils as ui_utils

logger = None

class System(object):
	''' The main object, representing the BMS (Bakery Managment System)'''
	def __init__(self, config_file):
		'''
		Initialize all the objects and set global variables
		Parameters:
			- config_file (str): the name of the configuration file
		'''
		global logger

		try:
			# Create a Config object
			self.conf = Config(config_file, True)
			
			# Set a global config global variable at utils
			self.set_global(None, self.conf)

			# Create the logger
			logger = utils.get_logger('core.system', logging.DEBUG)
			if self.conf.debug:
				logger.setLevel(logging.DEBUG)

			else:
				logger.setLevel(logging.WARNING)

			# Create a Database object
			self.db = Database(self.conf)
			
			# Set a global db global variable at ui_utils
			self.set_global(self.db, None)
			
			# Create a UIManager object
			self.ui_manager = UIManager(self.db, self.conf)
		
		except Exception as e:
			logger.debug('Exception: %s' % str(e.message))
			logger.error('Error in system init. Aborting...')
			sys.exit(1)

	def set_global(self, db=None, config=None):
		'''
		Set global variables in modules that are not classes
		Parameters:
			- db (Database): The Database object
			- config (Config): The Config object
		'''
		if db is not None:
			ui_utils.db = db
		if config is not None:
			utils.config = config















