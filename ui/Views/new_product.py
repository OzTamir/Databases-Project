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
# Filename:		new_product.py
# Description:	This file defines NewProduct
#
####################################

from view_base import ViewBase
from ui.ui_utils import input_with_exit
import core.utils as utils

logger = None

class NewProduct(ViewBase):
	''' A view presented when creating a new product entry '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		global logger

		# Set the logger
		logger = utils.get_logger('ui.views.new_product')

		self.new_product()

	def new_product(self):
		'''
		Add a new product
		'''
		## Constants
		# ----

		# 'Products' Column names (spaces will be removed later)
		P_COLUMNS = ('Product Name', 'Price Per Unit', 'Category', 'Description')
		# The index of the Category in the 'Products' table
		CATEGORY_IDX = 2
		# The index of the ID in the 'ProductCategories' table
		CID_IDX = 0

		## Variables
		# ----

		# List to hold details of the product
		values = [None for i in P_COLUMNS]

		## Code
		# ----

		print('To cancel, please enter "exit"')

		for idx, val in enumerate(P_COLUMNS):
			# The Category must exist, so we need to search for it
			if idx == CATEGORY_IDX:
				# Get the CategoryID (CID)
				cat_id = self.get_category()[CID_IDX]
				# Add it to the values
				values[idx] = cat_id
				# Continue the loop
				continue
			
			else:
				values[idx] = input_with_exit( \
								'Please Enter The %s: ' % str(val), \
								'exit', \
								'New Product deleted.')
				if values[idx] is None:
					return

		# Remove spacing from column names
		columns = tuple([''.join(x.split(' ')) for x in P_COLUMNS])
		# Insert the product to the 'Products' Table
		try:
			self.db.insert('Products', columns, values)
		
		except ValueError, e:
			logger.error('Error while adding product. Please try again.')
			logger.debug('Exception: %s' % str(e))
			return

	def get_category(self):
		'''
		Get the details of one product included in the purchase.
		'''
		# Ask the user for the category
		category = raw_input('Enter a category name or ID: ')

		# If we got a name, search by column 'CategoryName'
		if not category.isdigit():
			column = 'CategoryName'
		# Else, search by column 'CID'
		else:
			column = 'CID'

		# Get the products from the table
		search_results = self.db.search('ProductCategories', column, category, False)
		
		# Iterate over the retrived results
		for res in search_results:
			# Check if this is the category the user searched for.
			print(res)
			this = raw_input('Was this the category you were looking for? (Y/N): ')
			# If it is, quit the loop
			if this.lower() == 'y':
				return res
		
		# If none of the products matched, try again using recursion
		if not isinstance(category, tuple):
			print('Nothing found, please try again.')
			print('Note: Product names must be entered fully (the search is case-sensetive)')
			return self.get_category()
