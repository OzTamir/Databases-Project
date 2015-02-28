####################################
#
# Databases project - UI.Views Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			25 - 02 - 2015
#
####
#
# Filename:		stats_view.py
# Description:	Defines a class that shows systam statistics
#
####################################

from view_base import ViewBase
from ui.ui_utils import *

from datetime import date

class StatsView(ViewBase):
	''' View statistics '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		self.view_stats()

	def get_year(self):
		'''
		Ask the user the year for which he wants stats
		'''
		# Get input from the user
		year = ''
		while not year.isdigit() or not len(year) == 4:
			year = raw_input('Please enter a year (Must be a number of length 4): ')

		return year

	def total_income(self, year):
		'''
		Get the total income of the store at a given year
		Parameters:
			- year (str): the year in which we are intrested
		'''
		# Create the range
		year_start = '%s-01-01' % str(year)
		year_end = '%s-12-31' % str(year)

		# Create the res_range tuple
		date_column = 'PurchaseDate'
		res_range = (date_column, year_start, year_end)

		# Get the sum of the customers purchases (the income)
		income = self.db.sum_column('Purchases', 'Total', None, res_range)

		# Handle Nones
		if income is None:
			income = 0
		return ('Total income', str(income) + self.config.currency)
		
	def total_expenses(self, year):
		'''
		Get the total expenses of the store at a given year
		Parameters:
			- year (str): the year in which we are intrested
		'''
		## Constants ##

		# For Orders table
		ORDERS_TABLE = 'Orders'
		DATE_COLUMN = 'OrderDate'
		AMOUNT_IDX = 3
		PRICE_PER_UNIT_IDX = 4

		# Create the range
		year_start = '%s-01-01' % str(year)
		year_end = '%s-12-31' % str(year)
		
		# Create a variable to keep the total
		total = 0

		# Get the sum of the customers purchases (the income)
		for order in self.db.search_range(ORDERS_TABLE, DATE_COLUMN, year_start, \
										year_end):
			# Get the price and the amount
			amount = order[3]
			price = order[4]

			# Add the price of the order to the total
			total += (amount * price)
		
		# Handle Nones
		if total is None:
			total = 0
		
		return ('Total Expenses', str(total) + self.config.currency)

	def popular_products(self, year, amount=5):
		'''
		Get the most popular products at a given year
		Parameters:
			- year (str): the year in which we are intrested
			- amount (int): the amount of products to display
		'''
		## Constants ##

		# For the Purchases table
		PURCHASES_TABLE = 'Purchases'
		PURCHASE_DATE_COL = 'PurchaseDate'
		PURCHASE_ID_IDX = 0

		# For the PurchasesItems
		PI_TABLE = 'PurchasesItems'
		PURCHASE_ID_PI_IDX = 0
		PID_PI_IDX = 1
		AMOUNT_IDX = 2

		# For the Products table
		PRODUCTS_TABLE = 'Products'
		PID_COL = 'PID'
		PID_IDX = 0
		PRODUCT_NAME_IDX = 1

		# Create the range
		year_start = '%s-01-01' % str(year)
		year_end = '%s-12-31' % str(year)

		# Get all the purchases in this period
		purchases = self.db.search_range(PURCHASES_TABLE, PURCHASE_DATE_COL,\
								 year_start, year_end)

		# Store all the products
		products = dict()

		# Iterate over the purchases
		for purchase in purchases:
			pid = purchase[PURCHASE_ID_IDX]
			items = list(self.db.search('PurchasesItems', 'PurchaseID', pid,\
							False))
			# Iterate over the products in the purchase
			for product in items:
				# Get PID and amount in purchase
				product_id = product[PID_PI_IDX]
				amount = product[AMOUNT_IDX]
				# Add it to the dict
				products[product_id] = products.get(product_id, 0) + amount
		
		# Get the most popular products
		most_populars = [(pid, total_amount) for pid, total_amount \
						in products.items()]
		# Sort the list and get only the amount needed
		amount = min(amount, len(most_populars))
		most_populars = sorted(most_populars, key=lambda x: x[1], reverse=True)
		most_populars = most_populars[:amount]

		# Get names for the products
		products_names = []

		# Iterate over the most popular list to get names
		for pid, amount in most_populars:

			# Get the products from the Products table
			product = self.db.get_single_result(PRODUCTS_TABLE, \
												PID_COL, pid)
			
			# Get the product's name
			product_name = product[PRODUCT_NAME_IDX]

			# Create a stats string
			product_stat = '%s (Units: %s)' % (str(product_name), str(amount))

			# Add it to the list
			products_names.append(product_stat)

		# Format the result to a string
		res_string = ' | '.join(products_names)

		# Handle empty strings
		if res_string == '':
			res_string = 'Nothing yet...'

		return ('Most Popular Products', res_string)



	def view_stats(self):
		'''
		View statistics about the whole system and the store
		'''
		# Get the year from the user
		year = '2015'#self.get_year()

		# View titles
		TITLE = 'Statistics Report for %s' % str(year)
		COLUMNS = None

		# Get the stats
		income = self.total_income(year)
		expenses = self.total_expenses(year)
		most_populars = self.popular_products(year)
		print(income)
		print(expenses)
		print(most_populars)
		# Make sure we handle Nones
		if income[1] is None:	
			income = (income[0], '0$')
		if expenses[1] is None:
			expenses = (expenses[0], '0$')
		if most_populars[1] is None:
			most_populars = (most_populars[0], 'Nothing...')


		revenue = float(income[1][:-1]) - float(expenses[1][:-1])
		total_revenue = ('Total Revenue', str(revenue) + self.config.currency)

		# Print the stats in a nice table
		show_table(COLUMNS, (income, expenses, total_revenue, most_populars), TITLE, True)











