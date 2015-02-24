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
# Filename:		purchase_view.py
# Description:	Defines a class that allows the user to view purchases
#
####################################

import core.utils as utils

from view_base import ViewBase
from ui.ui_utils import *

# We need InventoryView.get_product()
from inventory_view import InventoryView

logger = None

class PurchaseView(ViewBase):
	''' View purchases '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		global logger

		# Set the logger
		logger = utils.get_logger('ui.views.purchase_view')
		
		self.view_all()

	def view_all(self):
		'''
		View all the records in Purchases table
		'''
		PRODUCT_VIEW_COLUMNS = ('Purchase ID', '# Items', 'Total', 'Date')
		PURCHASES_TABLE = 'Purchases'
		
		# Get Purchases details
		entries = [[str(item) for item in purchase] \
					for purchase in self.db.get_entries(PURCHASES_TABLE)]

		self.view_purchases(entries)

	def by_year(self):
		'''
		View Purchases from a certin year
		'''
		PURCHASES_TABLE = 'Purchases'

		# Get input from the user
		year = ''
		while not year.isdigit() or not len(year) == 4:
			year = raw_input('Please enter a year (Must be a number of length 4): ')

		# Create the start and end dates
		start = '%s-01-01' % str(year)
		end = '%s-12-31' % str(year)

		# Get the entries
		entries = self.db.search_range(PURCHASES_TABLE, 'PurchaseDate', start,\
										end)

		self.view_purchases(entries)

	def by_month(self):
		'''
		View Purchases from a certin month
		'''
		PURCHASES_TABLE = 'Purchases'

		# Get input from the user
		year = ''
		while not year.isdigit() or not len(year) == 4:
			year = raw_input('Please enter a year (Must be a number of length 4): ')

		# Get input from the user
		month = ''
		while not month.isdigit() or not len(month) <= 2:
			month = raw_input('Please enter a month: ')

		# Format the month
		if len(month) == 1:
			month = '0%s' % str(month)

		# Create the start and end dates
		start = '%s-%s-01' % (str(year), str(month))
		end = '%s-%s-31' % (str(year), str(month))

		# Get the entries
		entries = self.db.search_range(PURCHASES_TABLE, 'PurchaseDate', start,\
										end)

		self.view_purchases(entries)


	def view_purchases(self, entries):
		'''
		View the purchases table
		'''

		#### Constants ####
		
		PRODUCT_VIEW_COLUMNS = ('Purchase ID', '# Items', 'Total', 'Date')

		# For Purchases Table
		PURCHASES_TABLE = 'Purchases'
		PID_IDX = 0
		TOTAL_IDX = 2

		#### --- ####
		
		'''
		 - Print Purchase Table
		 - Ask the user for specific ID (while true loop)
		 	- If not on list or not int, ask if he want out
		 	- else, print that specific purchase (function)
		 	- than ask for another purchaseID
		 '''

		# # Get Purchases details
		# entries = [[str(item) for item in purchase] \
		# 			for purchase in self.db.get_entries(PURCHASES_TABLE)]

		# Create a dictionary of PID:Purchases pairs
		purchases_dict = dict()

		# Add currency symbol and the purchase to the dict
		for purchase in entries:
			# Make the tuple a list
			purchase = list(purchase)
			# Add the currency to the price units
			purchase[TOTAL_IDX] = str(purchase[TOTAL_IDX]) + \
									self.config.currency
			
			# Add the purchase to the dict
			purchases_dict[str(purchase[PID_IDX])] = purchase

		# Print the Purchases table
		show_table(PRODUCT_VIEW_COLUMNS, entries, 'Purchases')

		# Let the user view specific purchases
		while True:
			# Instruct the user and get his selected PurchaseID
			print('To return to the main menu, enter "exit".')
			selected_pid = input_with_exit( \
							'To view individual Purchase, enter it\'s ID: ', \
							'exit', \
							'', True)
			# If the user wanted out
			if selected_pid is None:
				return

			# If he gave us a PID, let's make sure it's valid
			elif selected_pid not in purchases_dict.keys():
				print('Please enter a valid PurchaseID.')

			# If we got a valid PurchaseID, show the Purchase details
			else:
				self.get_purchase(purchases_dict.get(selected_pid, None))


	def get_purchase(self, purchase):
		'''
		Get details about a single purchase
		Parameters:
			- purchase (list): a row from the table Purchases
		'''

		#### Constants ####
		
		PURCHASE_VIEW_COLUMNS = ('Item', 'Amount', 'Price')

		# For Purchases Table
		PURCHASES_TABLE = 'Purchases'
		PID_IDX = 0
		AMOUNT_IDX = 1
		TOTAL_IDX = 2

		# For Products Table
		PRODUCTS_TABLE = 'Products'
		PRODUCT_NAME_IDX = 1
		PRICE_PER_UNIT_IDX = 2

		# For PurchasesItems Table
		PURCHASE_ITEMS_TABLE = 'PurchasesItems'
		PURCHASE_ID_IDX = 0
		PRODUCT_ID_IDX = 1
		PRODUCT_AMOUNT_IDX = 2

		#### --- ####
		
		# Make sure we got a valid purchase
		if purchase is None:
			logger.debug('Purchase is None')
			logger.warning('Error viewing Purchase. Please try again.')
			return

		# Create a list to store the purchase details
		rows = []

		# Get all the products in this purchase
		pid = purchase[PID_IDX]
		items = list(self.db.search('PurchasesItems', 'PurchaseID', pid, False))

		# Iterate over the items
		for idx, item in enumerate(items):
			# Get the product's details
			product = InventoryView.get_product(self, item[PRODUCT_ID_IDX])

			# Get the product's name, amount, and price per unit
			product_name = product[PRODUCT_NAME_IDX]
			amount = item[PRODUCT_AMOUNT_IDX]
			product_price_per_unit = product[PRICE_PER_UNIT_IDX]
			
			# Create a string for the price (amount x ppu = price)
			price_str = ' '.join([str(amount), 'x', \
							str(product_price_per_unit), '=', \
							str(amount * product_price_per_unit) + \
							 self.config.currency])
			
			# Add to the items-on-purchase list
			rows.append((product_name, amount, price_str))
		
		# Add seperetor and final line for Total
		rows.append(('-', '-', '-'))
		rows.append(('', '', 'Total: %s' % str(purchase[TOTAL_IDX])))

		# Print the purchase table
		show_table(PURCHASE_VIEW_COLUMNS, rows, 'Purchase #%s' % str(pid))













