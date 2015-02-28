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
# Filename:		project.py
# Description:	This file is the file you run to load the system
#
####################################

from __future__ import print_function
from core import System
import os

def main():
	# Clear the console screen
	os.system('cls' if os.name == 'nt' else 'clear')
	system = System('my_config.json')
	system.ui_manager()

if __name__ == '__main__':
	main()