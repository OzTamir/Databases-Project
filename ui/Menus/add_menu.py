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
# Filename:		add_menu.py
# Description:	This file defines a menu that add items
#
####################################
from menu_base import MenuBase

class AddMenu(MenuBase):
	''' Class for a menu that add items '''
	def __init__(self, config, ui_manager):
		options = [
			('Add a new product', ui_manager.new_product),
			('Add a new purchase', ui_manager.new_purchase)
		]
		super(AddMenu, self).__init__(options, config)