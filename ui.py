import datetime

class UIBase(object):
	''' Base class for database UIs '''
	def __init__(self, db, msg, call_main=True):
		''' Create a UI object and call the mainUI '''
		self.db = db
		print(msg)
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
		''' Wrapper function for __add_entry to specificly for the Books table '''
		# Get the column names
		purchase = {'PurchaseID' : 0, 'Amount' : 0, 'Total' : 0.0}
		purchase_columns = ['PurchaseID', 'Amount', 'Total']
		purchase_items = []
		item_columns = ['PurchaseID', 'ProductID', 'Amount']
		print('Please enter the following details:')
		purchase['PurchaseID'] = raw_input('PurchaseID: ')
		purchase['Amount'] = int(raw_input('Number of items purchased: '))
		for item_idx in xrange(purchase['Amount']):
			item = [purchase['PurchaseID']]
			item.append(raw_input('ProductID: '))
			item.append(int(raw_input('Number of units purchased: ')))
			purchase['Amount'] -= item[-1]
			if purchase['Amount'] < 0:
				raise ValueError('Negative number of item, please try again.')
			purchase['Total'] += (float(raw_input('Price per unit: ')) * item[-1])
			purchase_items.append(item)
		try:
			self.db.insert('Purchases', purchase_columns, [purchase[i] for i in purchase_columns], auto_commit)
		except ValueError, e:
			print('Error: %s' % str(e))
			return

		for x in purchase_items:
			try:
				self.db.insert('PurchasesItems', item_columns, x, auto_commit)
			except ValueError, e:
				print('Error: %s' % str(e))
				return
		print('Inserted the follwoing entry into %s:' % str(table))
		print(' | '.join([str(val) for val in values]))
		print('-' * 10)



