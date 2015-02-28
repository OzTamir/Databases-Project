####################################
#
# Databases project - UI.Menus Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			25 - 02 - 2015
#
####
#
# Filename:		orders_menu.py
# Description:	This file defines a menu that shows orders options
#
####################################

from menu_base import MenuBase

class OrdersMenu(MenuBase):
	''' Class for the orders viewing menu '''
	def __init__(self, config, ui_manager):
		options = [
			('Create new Orders', ui_manager.new_order),
			('Redeem an Order', ui_manager.redeem_order),
			('View All Orders', ui_manager.orders_view),
			('Search by year', ui_manager.orders_view.by_year),
			('Search by month', ui_manager.orders_view.by_month),
		]
		super(OrdersMenu, self).__init__(options, config)