####################################
#
# Databases project - UI.View Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			21 - 02 - 2015
#
####
#
# Filename:		new_order.py
# Description:	This file defines NewOrder
#
####################################

from view_base import ViewBase
from ui.ui_utils import show_table

# For OrderDate, we need to figure out what is the current date
from datetime import date

# We need NewPurchase.get_product_in_purchase()
from new_purchase import NewPurchase

# We need InventoryView.get_product()
from inventory_view import InventoryView

class NewOrder(ViewBase):
	''' A view presented when creating a new order entry '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		self.new_order()


	def new_order(self):
		'''
		Add a new order
		'''

		'''
		- choose product to order
		- will display:
			* supplier
			* price per unit
		- ask for amount
		- will display:
			* supplier (name)
			* product (name)
			* amount
			* total
		- the user need to confirm
			* if yes, insert to db, allow to add another order
			* if no, return to menu
		'''


		#### Constants ####

		# Order View names (for viewing)
		O_VIEW_COLUMNS = ('Supplier Name', 'Product Name', 'Amount', 'Total')

		# 'Orders' table's columns (for the actual query)
		O_COLUMNS = ('SupplierID', 'ProductID', 'Amount', 'PricePerUnit', 'OrderDate')

		# For Products Table
		PRODUCTS_TABLE = 'Products'
		PID_IDX = 0
		PRODUCT_NAME_IDX = 1
		PRICE_PER_UNIT_IDX = 2
		
		# For Suppliers Table
		SUPPLIER_NAME_IDX = 1


		#### --- ####

		# List to hold details of the order
		values = [None for i in O_COLUMNS]

		# Get the product the user wants to order
		print('To create an order, please pick a product to order.')
		product = NewPurchase.get_product_in_purchase(self)

		if product is None:
			return

		product, amount = product

		# Get the product's supplier
		supplier = self.get_supplier_for_product(product)

		# Create something that we can present the user with
		view_values = [(supplier[SUPPLIER_NAME_IDX], product[PRODUCT_NAME_IDX],\
						str(amount), str(int(amount) * \
						int(product[PRICE_PER_UNIT_IDX])) + self.config.currency)]

		# Print the order table for confirmation
		show_table(O_VIEW_COLUMNS, view_values, 'New Order Details')


	def get_supplier_for_product(self, product):
		'''
		Get a product's supplier's details
		Parameters:
			- product (iterable): an entry from the products table
		'''

		#### Constants ####

		# For Suppliers Table
		SUPPLIERS_TABLE = 'Suppliers'

		# For Inventory Table
		INVENTORY_TABLE = 'Inventory'
		SID_IDX = 3

		# For Products Table
		PID_IDX = 0

		#### --- ####

		# Get the ProductID
		pid = product[PID_IDX]

		# Get the row in the inventory
		inventory_row = self.db.get_single_result(INVENTORY_TABLE, 'Product', str(pid))

		# Get the SupplierID
		sid = inventory_row[SID_IDX]

		# Return the supplier
		return self.db.get_single_result(SUPPLIERS_TABLE, 'SID', str(sid))



















