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
# Filename:		categories_view.py
# Description:	Defines a class that allows the user to view categories
#
####################################

from view_base import ViewBase
from ui.ui_utils import *

# We need InventoryView.get_product()
from inventory_view import InventoryView

class CategoriesView(ViewBase):
	''' View categories '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		self.view_categories()

	def view_categories(self):
		'''
		View the categories table
		'''

		#### Constants ####
		
		CATEGORY_VIEW_COLUMNS = ('ID', 'Name', '# Products In Category')

		# For the ProductCategories table
		CATEGORIES_TABLE = 'ProductCategories'
		CID_IDX = 0
		CATEGORY_NAME_IDX = 1

		# For Products Table
		PRODUCTS_TABLE = 'Products'
		PRODUCT_NAME_IDX = 1
		CATEGORY_ID_IDX = 3

		#### --- ####

		# Get the categories in the table
		entries = self.db.get_entries(CATEGORIES_TABLE)

		# Create a list to hold the data
		categories = [0 for x in entries]

		# Iterate over the categories
		for idx, category in enumerate(entries):
			# Get the details of the category
			cid, name = category
			
			# Get all the products for this category
			search_results = list(self.db.search(PRODUCTS_TABLE, 'Category', cid))
			
			# Count the number of products in this category
			category_products = len(search_results)

			# Create a tuple according to the SUPPLIERS_VIEW_COLUMNS
			category_row = (str(cid), str(name), str(category_products))

			# Add it to the categories list
			categories[idx] = category_row

		# Print the table
		show_table(CATEGORY_VIEW_COLUMNS, categories, 'Categories')











