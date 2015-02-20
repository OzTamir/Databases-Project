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
# Filename:		__init__.py
# Description:	This is the init file for the Core package
#
####################################

'''
This package contains all the file, classes and functions that are 
the backbone of this project.

Files:
	- config.py 	: Defines Config, the configuration object
	- database.py 	: Defines Database, which is the wrapper for the MySQL object
	- system.py 	: Defines the System object, which is the main object in this project
	- utils.py 		: Defines various utility functions
'''

from config import Config
from database import Database
from system import System
from utils import *