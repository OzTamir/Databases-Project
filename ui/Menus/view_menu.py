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
# Filename:		view_menu.py
# Description:	This file defines a menu that shows items
#
####################################

from menu_base import MenuBase

class ViewMenu(MenuBase):
	''' Class for a menu that shows items '''
	def __init__(self, config, ui_manager):
		options = [
			('View Products', ui_manager.products_view),
			('View Inventory', ui_manager.inventory_view),
			('View Previous Purchases', ui_manager.purchase_view),
			('View Orders', ui_manager.orders_view),
			('View Suppliers', ui_manager.suppliers_view)
		]
		super(ViewMenu, self).__init__(options, config)