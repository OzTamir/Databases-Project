####################################
#
# Databases project - UI.Menus Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			24 - 02 - 2015
#
####
#
# Filename:		purchase_menu.py
# Description:	This file defines a menu that shows items
#
####################################

from menu_base import MenuBase

class PurchaseMenu(MenuBase):
	''' Class for the purchase viewing menu '''
	def __init__(self, config, ui_manager):
		options = [
			('Create new Purchase', ui_manager.new_purchase),
			('View All Purchases', ui_manager.purchase_view),
			('Search by year', ui_manager.purchase_view.by_year),
			('Search by month', ui_manager.purchase_view.by_month),
		]
		super(PurchaseMenu, self).__init__(options, config)