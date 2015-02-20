import datetime

class UIBase(object):
	''' Base class for database UIs '''
	def __init__(self, db, config, call_main=True):
		''' Create a UI object and call the mainUI '''
		self.db = db
		self.config = config
		print(self.config.title_msg)
		print('-' * 10)
		if call_main:
			self.mainUI()

	def print_error(self):
		''' Prints an error message if the option is not valid '''
		print('Error, no such option.')

	def __add_entry(self, table, auto_commit=True):
		''' Add an entry to the table '''
		# Get the column names
		columns = self.db.get_columns(table)
		values = ['' for col in columns]
		print('Please enter the following details:')
		for index, column in enumerate(columns):
			# If the column type is a date
			if column[1] == 10:
				print('Please enter date in the following format: DD.MM.YYYY')
			values[index] = raw_input('%s: ' % str(column[0]))
			# If the column type is a date
			if column[1] == 10:
				try:
					# Try to parse values and create a datetime object
					day, mnt, year = values[index].split('.')
					values[index] = datetime.datetime(int(year), int(mnt), int(day))
				except (TypeError, ValueError):
					# If the user didn't follow the format, present an erro an send default values
					print("Error in date format, inserting '1'.'1'.'1' as date")
					values[index] = datetime.datetime(1, 1, 1)
		try:
			self.db.insert(table, [i[0] for i in columns], values, auto_commit)
		except ValueError, e:
			print('Error: %s' % str(e))
			return
		print('Inserted the follwoing entry into %s:' % str(table))
		print(' | '.join([str(val) for val in values]))

	def __print_columns(self, table):
		''' Print the columns of a table '''
		columns = ['#'] + self.db.get_column_names(table)
		print(' | '.join(columns))

	def __print_results(self, table, enumerator):
		''' Print a query result in a nice form '''
		# Print the columns of the table
		self.__print_columns(table)
		cnt = 0
		# Print each entry in a formatted line
		for index, entry in enumerator:
			entry = [str(val) for val in entry]
			print(('%d | ' % (index + 1)) + ' | '.join(entry))
			cnt += 1
		# Display the amount of entries found
		print('%d results found.' % cnt)

	def __print_table(self, table):
		''' Print a table '''
		table_enum = enumerate(self.db.iter_entries(table))
		self.__print_results(table, table_enum)

	# def search_library(self, bookname):
	# 	''' Search for books in the library '''
	# 	res_enum = enumerate(self.db.search('Books', 'Name', bookname, True, False))
	# 	self.__print_results('Books', res_enum)

	def new_order(self):
		''' Add new order '''
		self.__add_entry('PurchasesItems')
		print('-' * 10)
	
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

		# Get the products in the purchase
		while not product is None:
			# Get the next products
			product = self.get_product_in_purchase()
			# Add it to the purchase list
			products_in_purchase.append(product)

		# Remove None items from the list (The last item will always be None due to how the while is working)
		products_in_purchase = filter(None, products_in_purchase)

		# Get the amount and the total
		for product, cnt in products_in_purchase:
			amount += cnt
			total += (cnt * product[PRICE_IDX])

		# Create the values list expected by self.db.insert
		values = [amount, total]

		# Insert the purchase to the 'Purchases' Table
		try:
			self.db.insert('Purchases', P_COLUMNS, values, False)
		except ValueError, e:
			print('Error: %s' % str(e))
			return

		# Get the newly created PurchaseID
		purchase_id = self.db.get_entries('Purchases')[-1][PurchaseID_IDX]

		# Insert the items from the purchase to 'PurchasesItems' table
		for product, amount in products_in_purchase:
			# Empty the values list and size it properly
			values = [0 for x in xrange(3)]
			
			# Add the details to the values list
			values[PurchaseID_IDX] = purchase_id
			values[1] = product[ProductID_IDX]
			values[2] = amount

			# Insert it to the 'PurchasesItems' table
			try:
				self.db.insert('PurchasesItems', PI_COLUMNS, values, False)
			except ValueError, e:
				print('Error: %s' % str(e))
				continue

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
			return self.get_product_in_purchase()

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























