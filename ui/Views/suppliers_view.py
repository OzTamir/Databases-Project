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
# Filename:		suppliers_view.py
# Description:	Defines a class that allows the user to view suppliers
#
####################################

from view_base import ViewBase
from ui.ui_utils import *

# We need InventoryView.get_product()
from inventory_view import InventoryView

class SuppliersView(ViewBase):
	''' View suppliers '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		self.view_suppliers()

	def view_suppliers(self):
		'''
		View the suppliers table
		'''

		#### Constants ####
		
		SUPPLIERS_VIEW_COLUMNS = ('SID', 'Name', '# Products', 'Products')

		# For Suppliers Table
		SUPPLIERS_TABLE = 'Suppliers'

		# For Inventory Table
		INVENTORY_TABLE = 'Inventory'
		PRODUCT_IDX = 1

		# For Products Table
		PRODUCTS_TABLE = 'Products'
		PID_IDX = 0
		PRODUCT_NAME_IDX = 1

		#### --- ####

		# Get the suppliers in the table
		entries = self.db.get_entries(SUPPLIERS_TABLE)

		# Create a list to hold the data
		suppliers = [0 for x in entries]

		# Iterate over the suppliers
		for idx, supplier in enumerate(entries):
			# Get the details of the supplier
			sid, name = supplier
			# Get all the products for this supplier
			search_results = self.db.search(INVENTORY_TABLE, 'Supplier', sid, False)
			# Create a list to hold all the products names
			supplier_products = []
			# Store the amount of products for this supplier (counter variable)
			supplier_amount = 0

			# Iterate over the search results, get the names for products
			for product in search_results:
				# Increase the counter
				supplier_amount += 1
				# Get the ProductID
				pid = product[PRODUCT_IDX]
				# Get the name of the product from Products table
				product_row = InventoryView.get_product(self, pid)
				# Make sure we got a value
				if product_row is None:
					# Restore supplier count to it's previous state
					supplier_amount -= 1
					# Continue the loop
					continue
				#  Else, get the product name
				product_name = product_row[PRODUCT_NAME_IDX]
				# Finally, add the name to the supplier's products list
				supplier_products.append(str(product_name))

			# Make a string out of the products list
			str_supplier_products = str(supplier_products)

			# Create a tuple according to the SUPPLIERS_VIEW_COLUMNS
			supplier_row = (str(sid), str(name), str(supplier_amount), str_supplier_products)

			# Add it to the suppliers list
			suppliers[idx] = supplier_row

		# Print the table
		show_table(SUPPLIERS_VIEW_COLUMNS, suppliers, 'Suppliers')











