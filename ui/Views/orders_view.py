####################################
#
# Databases project - UI.Views Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			21 - 02 - 2015
#
####
#
# Filename:		orders_view.py
# Description:	Defines a class that allows the user to view orders
#
####################################

from view_base import ViewBase
from ui.ui_utils import *

# We need InventoryView.get_product()
from inventory_view import InventoryView

class OrdersView(ViewBase):
	''' View orders '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		self.view_orders()

	def view_orders(self):
		'''
		View the orders table
		'''

		#### Constants ####
		
		ORDERS_VIEW_COLUMNS = ('OrderID', 'Product', '# Units', 'Total', \
								'Supplier','Date')

		# For Suppliers Table
		SUPPLIERS_TABLE = 'Suppliers'
		SUPPLIER_ID_IDX = 0
		SUPPLIER_NAME_IDX = 1

		# For Orders Table
		ORDERS_TABLE = 'Orders'
		OID_IDX = 0
		SID_IDX = 1
		PRODUCT_ID_IDX = 2
		AMOUNT_IDX = 3
		PRICE_PER_UNIT_IDX = 4
		DATE_IDX = 5

		# For Products Table
		PRODUCTS_TABLE = 'Products'
		PID_IDX = 0
		PRODUCT_NAME_IDX = 1

		#### --- ####

		# Get the orders in the table
		entries = self.db.get_entries(ORDERS_TABLE)

		# Create a list to hold the data
		orders = []

		# Iterate over the orders
		for idx, order in enumerate(entries):
			# Get the details of the order
			oid, sid, pid, amount, price_per_unit, date = order
			
			# Get the supplier's name
			supplier = self.db.get_single_result(SUPPLIERS_TABLE, 'SID', str(sid))
			supplier_name = supplier[SUPPLIER_NAME_IDX]
			
			# Get the product's name
			product = self.db.get_single_result(PRODUCTS_TABLE, 'PID', str(pid))
			product_name = product[PRODUCT_NAME_IDX]
			
			# Create  a tuple with the values
			values = (str(oid), str(product_name), str(amount), \
						str(float(price_per_unit) * int(amount)) + \
						self.config.currency, \
						str(supplier_name), str(date))

			# Add it to the orders list
			orders.append(values)

		# Print the table
		show_table(ORDERS_VIEW_COLUMNS, orders, 'Orders')











