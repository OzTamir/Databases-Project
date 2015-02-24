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
import core.utils as utils

# For OrderDate, we need to figure out what is the current date
from datetime import date

# We need NewPurchase.get_product_in_purchase()
from new_purchase import NewPurchase

logger = None

class NewOrder(ViewBase):
	''' A view presented when creating a new order entry '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		global logger

		# Set the logger
		logger = utils.get_logger('ui.views.new_order')
		
		self.new_order()


	def new_order(self):
		'''
		Add a new order
		'''
		#### Constants ####

		# Order View names (for viewing)
		O_VIEW_COLUMNS = ('Supplier Name', 'Product Name', 'Amount', 'Total')

		# 'Orders' table's columns (for the actual query)
		O_COLUMNS = ('SupplierID', 'ProductID', 'Amount', 'PricePerUnit', \
					 'OrderDate')

		# For Products Table
		PRODUCTS_TABLE = 'Products'
		PID_IDX = 0
		PRODUCT_NAME_IDX = 1
		PRICE_PER_UNIT_IDX = 2
		
		# For Suppliers Table
		SUPPLIER_ID_IDX = 0
		SUPPLIER_NAME_IDX = 1


		#### --- ####

		# List to hold details of the order
		values = [None for i in O_COLUMNS]

		# Get the product the user wants to order
		print('To create an order, please pick a product to order.')
		product = self.get_product_in_purchase(obj)

		# Make sure we are done
		if product is None:
			return

		product, amount = product

		# Get the product's supplier
		supplier = self.get_supplier_for_product(product)

		# Create something that we can present the user with
		view_values = [(supplier[SUPPLIER_NAME_IDX], product[PRODUCT_NAME_IDX],\
						str(amount), str(int(amount) * \
						int(product[PRICE_PER_UNIT_IDX])) + \
						self.config.currency)]

		# Print the order table for confirmation
		show_table(O_VIEW_COLUMNS, view_values, 'New Order Details')

		# Confirm the order's details with the user
		confirm = raw_input('Would you like to place this order? (Y/N)')
		
		# If the user didn't replied yes, cancel the order
		if confirm.lower() != 'y':
			print('Order canceled.')
			return

		# Create the values required
		supplier_id = supplier[SUPPLIER_ID_IDX]
		product_id = product[PID_IDX]
		price_per_unit = product[PRICE_PER_UNIT_IDX]
		order_date = date.today()

		# Create a tuple with all the values
		values = (supplier_id, product_id, amount, price_per_unit, order_date)

		# Insert the order details to the 'Orders' Table
		try:
			self.db.insert('Orders', O_COLUMNS, values)
		
		except ValueError, e:
			logger.error('Error while creating a new order. Please try again.')
			logger.debug('Exception: %s' % str(e))


	def get_product_in_purchase(self, obj):
		'''
		Since we call a static method which has a recursive element,
		we implement this function to avoid exceptions.
		'''
		return NewPurchase.get_product_in_purchase(obj)


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



















