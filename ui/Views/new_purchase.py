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
# Filename:		new_purchase.py
# Description:	This file defines NewPurchase
#
####################################

from view_base import ViewBase
import core.utils as utils

from datetime import date

logger = None

class NewPurchase(ViewBase):
	''' A view presented when creating a new purchase entry '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		global logger

		# Set the logger
		logger = utils.get_logger('ui.views.new_purchase')

		self.new_purchase()

	def new_purchase(self):
		'''
		Add a new purchase
		'''
		## Constants
		# ----

		# 'Purchases' Column names
		P_COLUMNS = ('Amount', 'Total')
		# 'PurchasesItems' Column names
		PI_COLUMNS = ('PurchaseID', 'ProductID', 'Amount')
		# The index of the price in the 'Products' table
		PRICE_IDX = 2
		# The index of the ProductID in the 'Products' table
		ProductID_IDX = 0
		# The Index of the PurchaseID in the 'Purchases' table
		PurchaseID_IDX = 0

		## Variables
		# ----

		# List to hold details of products in purchase
		products_in_purchase = []
		# Total of the order
		total = 0
		# Amount of items
		amount = 0
		# The ID of the purchase
		purchase_id = -1
		# Variable to hold a given product in the purchase
		product = (None, None)

		## Code
		# ----

		# Seperetor
		print('')

		# Tell the user how to quit
		print('To finish entring products, enter "exit" or just press enter')

		# Get the products in the purchase
		while not product is None:
			# Get the next products
			product = self.get_product_in_purchase(self)
			# Add it to the purchase list
			products_in_purchase.append(product)

		# Remove None items from the list (The last item will always be None due to how the while is working)
		products_in_purchase = filter(None, products_in_purchase)

		# Get the amount and the total
		for product, cnt in products_in_purchase:
			amount += cnt
			total += (cnt * product[PRICE_IDX])

		# Add 'PurchaseDate' to the columns list
		columns = [x for x in P_COLUMNS]
		columns.append('PurchaseDate')
		columns = tuple(columns)

		# Create the values list expected by self.db.insert
		values = [amount, total, date.today()]

		# Insert the purchase to the 'Purchases' Table
		try:
			# We don't commit yet, as we still update to enter PurchaseDetails
			self.db.insert('Purchases', columns, values, False)
		except ValueError, e:
			logger.error('Error while adding purchase. Please try again.')
			logger.debug('Exception: %s' % str(e))
			return

		# Get the newly created PurchaseID
		purchase_id = self.db.get_entries('Purchases')[-1][PurchaseID_IDX]

		try:
			# Insert the items from the purchase to 'PurchasesItems' table
			for product, amount in products_in_purchase:
				# Empty the values list and size it properly
				values = [0 for x in xrange(3)]
				
				# Add the details to the values list
				values[PurchaseID_IDX] = purchase_id
				values[1] = product[ProductID_IDX]
				values[2] = amount

				# Insert it to the 'PurchasesItems' table
				self.db.insert('PurchasesItems', PI_COLUMNS, values, False)

				# Update the amount in the inventory
				self.update_product(product, amount)
		
		# If there was any exception, do a rollback
		except Exception, e:
			logger.error('Error while adding purchase. Please try again.')
			logger.debug('Exception: %s' % str(e))
			self.db.rollback()

		# Only if there were no errors, commit changes
		else:
			self.db.commit()


	def update_product(self, product, amount):
		'''
		Update product's amount in the inventory
		Parameters:
			- products (iterable): an entry from Products table
			- amount (int): the amount bought in the purchase
		'''
		## Constants ##

		# For products table
		PID_IDX = 0

		# For inventory table
		INVENTORY_TABLE = 'Inventory'
		AMOUNT_COLUMN = 'UnitsInStock'
		PRODUCT_COLUMN = 'Product'
		PID_INVENTORY_IDX = 1
		UNITS_IN_STOCK_IDX = 2

		# Get the current amount in stock for this product
		pid = product[PID_IDX]
		product_in_inventory = self.db.get_single_result(INVENTORY_TABLE,\
								 PRODUCT_COLUMN, pid)
		current_amount = product_in_inventory[UNITS_IN_STOCK_IDX]

		# Calculate the new amount in inventory
		# TODO: If negative result, suggest to order more units
		new_amount = max(0, current_amount - amount)

		# Create the data needed for an update call
		match = (PRODUCT_COLUMN, pid)
		update_dict = {AMOUNT_COLUMN : new_amount}

		# Update this column
		# We won't put this in try/except since we do that in new_purchase()
		self.db.update(INVENTORY_TABLE, match, update_dict, False)


	# This method is used in new_order.py, so I made it static
	@staticmethod
	def get_product_in_purchase(self):
		'''
		Get the details of one product included in the purchase.
		'''
		# Ask the user for the next product in the purchase
		product = raw_input('Enter a product name or ID: ')
		
		# If we got input that could signal end of order, ask the user
		if product == '' or product.lower() in ['exit', 'done']:
			# Ask the user
			ans = raw_input('Finished adding products? (Y/N): ')
			# If we are done
			if ans.lower() == 'y':
				return None
			# If it was a mistake, make a tail recursive call to return a value
			# This recursion saves us from having to recall in self.new_purchase()
			return self.get_product_in_purchase(self)

		# If we got a name, search by column 'ProductName'
		if not product.isdigit():
			column = 'ProductName'
		# Else, search by column 'PID'
		else:
			column = 'PID'

		# Get the products from the table
		search_results = self.db.search('Products', column, product, False)
		
		# Iterate over the retrived results
		for res in search_results:
			# Check if this is the item the user searched for.
			print(res)
			this = raw_input('Was this the product you were looking for? (Y/N): ')
			# If it is, quit the loop
			if this.lower() == 'y':
				product = res
				break
		
		# If none of the products matched, try again using recursion
		if not isinstance(product, tuple):
			print('Nothing found, please try again.')
			print('Note: Product names must be entered fully (the search is case-sensetive)')
			return self.get_product_in_purchase()

		# Now, we ask for the amount purchased
		amount = ''
		# Make sure we recive a number
		while not amount.isdigit():
			amount = raw_input('Enter the amount of %s being purchased (should be a number): ' % str(product[1]))
		# Cast the input to an integer
		amount = int(amount)

		# Finally, return a tuple with product's info and the amount
		return (product, amount)