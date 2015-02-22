####################################
#
# Databases project - UI.Views Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			22 - 02 - 2015
#
####
#
# Filename:		products_view.py
# Description:	Defines a class for viewing the Products table
#
####################################

from view_base import ViewBase
from ui.ui_utils import *

class ProductsView(ViewBase):
	''' View products '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		self.view_products()

	def view_products(self):
		'''
		View the products table
		'''

		#### Constants ####
		
		PRODUCTS_VIEW_COLUMNS = ('ID', 'Name', 'Price Per Unit', 'Category', \
								'Description')

		# For Products Table
		PRODUCTS_TABLE = 'Products'
		PID_IDX = 0
		PRODUCT_NAME_IDX = 1
		PRICE_PER_UNIT_IDX = 2
		CATEGORY_ID_IDX = 3
		DESCRIPTION_IDX = 4

		# For the ProductCategories table
		CATEGORIES_TABLE = 'ProductCategories'
		CID_IDX = 0
		CATEGORY_NAME_IDX = 1

		#### --- ####

		# Get the products in the table
		entries = self.db.get_entries(PRODUCTS_TABLE)

		# Create a list to hold the data
		products = []

		# Iterate over the products
		for idx, product in enumerate(entries):
			# Get the details of the order
			pid, name, price_per_unit, cid, desc = product
			
			# Get the category's name
			# First, check that the product has a category
			if cid is None:
				category_name = 'NULL'
			else:
				cat = self.db.get_single_result(CATEGORIES_TABLE, 'CID', str(cid))
				category_name = cat[CATEGORY_NAME_IDX]
			
			# Create  a tuple with the values
			values = (str(pid), str(name), str(price_per_unit) \
						+ self.config.currency, \
						str(category_name), str(desc))

			# Add it to the products list
			products.append(values)

		# Print the table
		show_table(PRODUCTS_VIEW_COLUMNS, products, 'Products')