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

	def show_edit(self):
		'''
		Implement the abstrect method show_edit
		'''
		self.edit_inventory()

	def edit_inventory(self):
		'''
		Allow editing of the inventory
		'''
		
		#### Constants ####

		# User present-able names
		EDITABLE_COLUMNS = ('Product', 'Units In Stock', 'Supplier')

		# Ask if the user want to edit
		want_to_edit = raw_input('Would you like to edit the data? (Y/N): ')
		# If the answer is anything but yes, return
		if not (want_to_edit.lower() == 'y' or want_to_edit.lower() == 'yes'):
			return

		# We need a loop to make sure we get data
		inventory = None

		while inventory is None:
			# Ask for the inventory number to edit
			inventory_id = input_with_exit('Please enter the ID: ', \
											'Editing cancled', 'exit')

			# If the user is asking to quit
			if inventory_id is None:
				return

			# Get the inventory details
			inventory = self.db.get_single_result('Inventory', \
													'InventoryItemID', \
													str(inventory_id))
			if inventory is None:
				print('Please enter a valid ID.')

		# Create the new_val dict for db.update
		new_values = dict()

		# This is used to prompt the user

		# Instruct the user
		print('Please enter new values, or blank to leave it as it is')
		for key in EDITABLE_COLUMNS:
			# Since Product and suppliers require ID, show the table
			if key == 'Product' or key == 'Supplier':
				# Get all the products
				items = [item[:2] for item in \
							self.db.get_entries(str(key) + 's')]
				
				# Print a table
				show_table(('ID', 'Name'), items, str(key) + 's')

				# Set the prompt
				prompt = 'Please enter the new %s\'s ID: ' % str(key)
			# Else, Set the prompt for the units
			else:
				prompt = 'Please enter the amount of Units in stock: '

			# Get the user's input
			new_val = raw_input(prompt)

			# Make sure it's valid
			if new_val != '':
				# Set the value in the new_val dict to the new value
				# The split and join are to make sure that the key is correct
				new_values[''.join(key.split(' '))] = new_val

		# Print the new values for confirmation
		keys = []
		values = []
		for key, value in new_values.items():
			keys.append(key)
			values.append(value)

		# Show the new values
		show_table(keys, values, 'New Values')

		# Confirm with the user
		confirm = input_with_exit('Are you sure you want to update ' + \
									'these values? (Y/N) :', \
									'n', 'Update aborted.')
		# If the update was canceled
		if confirm is None:
			return

		# Else, update
		match = ('InventoryItemID', inventory[0])
		self.db.update('Inventory', match, new_values)

		print('Values updated.')



	def view_inventory(self):
		'''
		View the inventory table
		'''

		#### Constants ####
		
		INVENTORY_VIEW_COLUMNS = ('ID', 'Product', 'Amount In Stock', \
									'Price Per Unit', 'Stock Worth', \
									'Supplier')

		# For Inventory Table
		INVENTORY_TABLE = 'Inventory'
		INVENTORY_ITEM_ID_IDX = 0
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
			# Get the inventory ID
			inventory_id = product[INVENTORY_ITEM_ID_IDX]
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
			rows[idx] = (inventory_id, product_details[NAME_IDX], \
						product_amount, \
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





















