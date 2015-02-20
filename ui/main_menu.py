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
# Filename:		main_menu.py
# Description:	This file defines the main menu class
#
####################################
from menu_base import MenuBase

class MainMenu(MenuBase):
	''' The main menu class '''
	def __init__(self, config, ui_manager):
		options = [
			('Create a new order', ui_manager.new_order),
			('Create a new purchase', ui_manager.new_purchase)
		]
		super(MainMenu, self).__init__(options, config)