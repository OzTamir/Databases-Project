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
# Filename:		__init__.py
# Description:	This is the init file for the UI.Menus package
#
####################################

'''
This package contains all the classes that defines Menus

Files:
	- menu_base.py 			: Includes the base class for menus
	- main_menu.py 			: Includes class for the main menu

	- add_menu.py			: Defines a menu that add items
	- view_menu.py			: Defines a menu that shows items
	- purchase_menu.py		: Defines a menu that shows purchases options
	- orders_menu.py		: Defines a menu that shows orders options
'''

from menu_base import MenuBase
from main_menu import MainMenu
from add_menu import AddMenu
from view_menu import ViewMenu
from purchase_menu import PurchaseMenu
from orders_menu import OrdersMenu