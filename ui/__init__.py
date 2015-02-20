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
# Filename:		__init__.py
# Description:	This is the init file for the UI package
#
####################################

'''
This package contains all the file, classes and functions used in the
context of User Interface.

Files:
	- ui.py 		: Includes the base classes for the UI
	- views.py 		: Includes definitions of views
	- menu_base.py 	: Defines the base class for menus
	- main_menu.py 	: Defines the main menu class

'''

import ui_utils
from views import NewPurchaseView
from menu_base import MenuBase
from main_menu import MainMenu
from ui_manager import UIManager
