####################################
#
# Databases project - UI.Views Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			20 - 02 - 2015
#
####
#
# Filename:		inventory_view.py
# Description:	Defines a class that allows the user to view the inventory
#
####################################

from mysql.connector.errors import *

from view_base import ViewBase
from ui.ui_utils import *

class InventoryView(ViewBase):
	''' View the inventory '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		self.view_inventory()

	def view_stats(self):
		'''
		View genarel information about the inventory
		'''
		# Get stats
		entries = self.db.get_entries(INVENTORY_TABLE)
		product_cnt = len(entries)
		units_cnt = sum([product[UNITS_IDX] for product in entries])

		# Print stats
		print('Stats:')
		print('Total Products:	%d' % int(product_cnt))
		print('Total Unit:		%d' % int(units_cnt))

	def view_inventory(self):
		'''
		View the inventory table
		'''

		#### Constants ####
		
		INVENTORY_VIEW_COLUMNS = ('Product', 'Amount In Stock', 'Price Per Unit', 'Stock Worth', 'Supplier')

		# For Inventory Table
		INVENTORY_TABLE = 'Inventory'
		PRODUCT_IDX = 1
		UNITS_IDX = 2
		SUPPLIER_IDX = 3

		# For Products Table
		PRDUCTS_TABLE = 'Products'
		NAME_IDX = 1
		PRICE_PER_UNIT_IDX = 2

		#### --- ####

		# Get the entries
		entries = self.db.get_entries(INVENTORY_TABLE)
		# Create a list to hold the data
		rows = [0 for x in entries]
		# Get more details for each product in inventory
		for idx, product in enumerate(entries):
			# Get the product's details
			product_details = self.get_product(self, product[PRODUCT_IDX])
			# Make sure we found the product
			if product_details is None:
				continue
			# Get the amount in inventory
			product_amount = product[UNITS_IDX]
			# Get the worth of the stock of the product
			product_worth = str(product_amount * \
							product_details[PRICE_PER_UNIT_IDX]) + \
							self.config.currency
			# Get details about the supplier
			product_supplier = self.get_supplier(product[SUPPLIER_IDX])
			# Add as a tuple in the rows list
			rows[idx] = (product_details[NAME_IDX], product_amount, \
						str(product_details[PRICE_PER_UNIT_IDX]) + \
						self.config.currency, product_worth, product_supplier)

		# Print the table
		show_table(INVENTORY_VIEW_COLUMNS, rows, 'Inventory')

	# Because we need this function in suppliers_view, I made it a 
	# static method in order to avoid duplicating the code.
	@staticmethod
	def get_product(self, pid):
		'''
		Get a single prdouct from the products table
		Parameters:
			- pid (int / str): the ProductID of the requested product
		'''
		try:
			# Sometimes an unread result will raise an exception
			self.db.clear_cursor()
			# Get the products from the table as a list
			search_results = [x for x in self.db.search('Products', 'PID', str(pid), False)]

		# And sometimes MySQL will raise an InterfaceError, requiring us
		# to run the search again.
		except InterfaceError:
			# Get the products from the table as a list
			search_results = [x for x in self.db.search('Products', 'PID', str(pid), False)]

		# Make sure we have a product
		if len(search_results) == 0:
			return None

		# Return the first item found (there should only be one)
		return search_results[0]

	def get_supplier(self, sid):
		'''
		Get supplier's details
		Parameters:
			- sid (int / str): the id of the requested supplier
		'''
		SUPPLIER_NAME_IDX = 1

		# Get the suppliers from the table as a list
		search_results = list(self.db.search('Suppliers', 'SID', str(sid), False))

		# Make sure we have a supplier
		if len(search_results) == 0:
			return 'NULL'

		# Return the first item found (there should only be one)
		return search_results[0][SUPPLIER_NAME_IDX]





















