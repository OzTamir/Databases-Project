####################################
#
# Databases project - UI.Views Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			28 - 02 - 2015
#
####
#
# Filename:		redeem_order.py
# Description:	Redeem an order and add it to the inventory
#
####################################

from view_base import ViewBase
from ui.ui_utils import *

# We need OrdersView.view_orders()
from orders_view import OrdersView

class RedeemOrder(ViewBase):
	''' Redeem an order '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		self.redeem_order()

	def redeem_order(self):
		'''
		Redeem an order
		'''

		#### Constants ####
		
		SUPPLIERS_VIEW_COLUMNS = ('SID', 'Name', '# Products', 'Products')

		# For Orders Table
		ORDERS_TABLE = 'Orders'
		RECIVED_COL = 'Recived'
		PRODUCT_IDX = 2
		AMOUNT_IDX = 3

		# For Inventory Table
		INVENTORY_TABLE = 'Inventory'
		PRODUCT_INVENTORY_IDX = 1
		UNITS_IN_STOCK_IDX = 2

		# For Products Table
		PRODUCTS_TABLE = 'Products'
		PID_IDX = 0
		PRODUCT_NAME_IDX = 1

		#### --- ####

		# Show all the un-redeemed orders
		entries = list(self.db.search(ORDERS_TABLE, RECIVED_COL, 0))
		OrdersView.view_orders(self, entries, 'Unredeemed Orders')

		# Ask what order would the user like to redeem
		redeem_id = input_with_exit('Please enter OrderID to redeem: ',\
									'exit', 'Nothing Redeemed', True)
		# Make sure we got a valid input
		if redeem_id is None:
			return

		# Get the order with this id
		order_to_redeem = self.db.get_single_result(ORDERS_TABLE, 'OID', redeem_id)

		# If nothing found, print an error and make a recursive call to try again
		if order_to_redeem is None:
			print('No such order found. Please enter a valid ID.')
			return self.redeem_order()

		# Get the product and the amount
		product_id = order_to_redeem[PRODUCT_IDX]
		amount = order_to_redeem[AMOUNT_IDX]

		# Get the amount from the inventory
		product_inventory = self.db.get_single_result(INVENTORY_TABLE, \
													'Product', product_id)
		units_in_stock = product_inventory[UNITS_IN_STOCK_IDX]

		# Get the new amount to put in inventory
		new_amount = units_in_stock + amount

		# Create data required for update
		match = ('Product', product_id)
		update_dict = {'UnitsInStock' : new_amount}
		
		# Update the product in the inventory
		try:
			self.db.update(INVENTORY_TABLE, match, update_dict, False)
		except Exception, e:
			print('Error while redeeming order, please try again.')
			return

		# Create data required for updating orders table
		match = ('OID', redeem_id)
		update_dict = {'Recived' : 1}

		# Update the order and mark it as recived
		try:
			self.db.update(ORDERS_TABLE, match, update_dict, False)
		except Exception, e:
			print('Error while marking order as redeemed.')
			print('Changes were reverted, please try again.')
			return

		# If we got no errors, commit the changes
		else:
			self.db.commit()













