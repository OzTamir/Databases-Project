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
# Filename:		orders_view.py
# Description:	Defines a class that allows the user to view orders
#
####################################

from view_base import ViewBase
from ui.ui_utils import *

class OrdersView(ViewBase):
	''' View orders '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		self.view_all()

	def view_all(self):
		'''
		View all the records in Orders table
		'''

		ORDERS_TABLE = 'Orders'
		
		# Get Orders details
		entries = self.db.get_entries(ORDERS_TABLE)

		self.view_orders(self, entries)

	def by_year(self):
		'''
		View Orders from a certin year
		'''
		ORDERS_TABLE = 'Orders'

		# Get input from the user
		year = ''
		while not year.isdigit() or not len(year) == 4:
			year = raw_input('Please enter a year (Must be a number of length 4): ')

		# Create the start and end dates
		start = '%s-01-01' % str(year)
		end = '%s-12-31' % str(year)

		# Get the entries
		entries = self.db.search_range(ORDERS_TABLE, 'OrderDate', start,\
										end)

		self.view_orders(self, entries)

	def by_month(self):
		'''
		View Purchases from a certin month
		'''
		ORDERS_TABLE = 'Orders'

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
		entries = self.db.search_range(ORDERS_TABLE, 'OrderDate', start,\
										end)

		self.view_orders(self, entries)

	# We need it in redeem_order.py, so I made it static
	@staticmethod
	def view_orders(self, entries, title='Orders'):
		'''
		View the orders table
		'''

		#### Constants ####
		
		ORDERS_VIEW_COLUMNS = ('OrderID', 'Product', '# Units', 'Total', \
								'Supplier','Date', 'Order Recived')

		# For Suppliers Table
		SUPPLIERS_TABLE = 'Suppliers'
		SUPPLIER_ID_IDX = 0
		SUPPLIER_NAME_IDX = 1

		# For Orders Table
		ORDERS_TABLE = 'Orders'
		OID_IDX = 0
		SID_IDX = 1
		PRODUCT_ID_IDX = 2
		AMOUNT_IDX = 3
		PRICE_PER_UNIT_IDX = 4
		DATE_IDX = 5
		RECIVED_IDX = 6

		# For Products Table
		PRODUCTS_TABLE = 'Products'
		PID_IDX = 0
		PRODUCT_NAME_IDX = 1

		#### --- ####

		# Create a list to hold the data
		orders = []

		# Iterate over the orders
		for idx, order in enumerate(entries):
			# Get the details of the order
			oid, sid, pid, amount, price_per_unit, date, recvied = order
			
			# Get the supplier's name
			supplier = self.db.get_single_result(SUPPLIERS_TABLE, 'SID', str(sid))
			supplier_name = supplier[SUPPLIER_NAME_IDX]
			
			# Get the product's name
			product = self.db.get_single_result(PRODUCTS_TABLE, 'PID', str(pid))
			product_name = product[PRODUCT_NAME_IDX]
			
			# Convert the recive value to boolean
			recvied = bool(recvied)
			recived_text = ('True' * int(recvied)) + ('False' * int(not recvied))

			# Create  a tuple with the values
			values = (str(oid), str(product_name), str(amount), \
						str(float(price_per_unit) * int(amount)) + \
						self.config.currency, \
						str(supplier_name), str(date), recived_text)

			# Add it to the orders list
			orders.append(values)

		# Print the table
		show_table(ORDERS_VIEW_COLUMNS, orders, title)











