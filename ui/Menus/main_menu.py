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
# Filename:		main_menu.py
# Description:	This file defines the main menu class
#
####################################
from menu_base import MenuBase

class MainMenu(MenuBase):
	''' The main menu class '''
	def __init__(self, config, ui_manager):
		options = [
			('Add new items', ui_manager.add_menu),
			('View existing items', ui_manager.view_menu),
			('Manage Purchases', ui_manager.purchase_menu),
			('Manage Orders', ui_manager.orders_menu)
		]
		super(MainMenu, self).__init__(options, config, True)