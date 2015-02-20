####################################
#
# Databases project - UI Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			20 - 02 - 2015
#
####
#
# Filename:		ui_utils.py
# Description:	This file defines a utilities class with utility functions
#
####################################

import datetime


'''

Note:
	This was initially meant to be a Singleton class,
	but it has occured to me that it will be a better idea to just use
	a module with many functions a global variable for the Database.

	This is not something I would have done have I thought that there is a more
	elegant way.

	This note is here to point out this code structure, and to highlight that
	changing any global variable in more than one designated place would be
	a very bad idea.

'''


# Global Variables
db = None

# Functions
def print_error():
	'''
	Prints an error message if the option is not valid
	'''
	print('Error, no such option.')

def __add_entry(table, auto_commit=True):
	'''
	Add an entry to the table
	Parameters:
		- table (str) : The table to add into
		- auto_commit (bool): whether or not should the function commit changes
	'''
	# Get the column names
	columns = db.get_columns(table)
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
		db.insert(table, [i[0] for i in columns], values, auto_commit)
	except ValueError, e:
		print('Error: %s' % str(e))
		return
	print('Inserted the follwoing entry into %s:' % str(table))
	print(' | '.join([str(val) for val in values]))

def __print_columns(table):
	'''
	Print the columns of a table
	Parameters:
		- table (str): the table to be printed
	'''
	columns = ['#'] + db.get_column_names(table)
	print(' | '.join(columns))

def __print_results(table, enumerator):
	'''
	Print a query result in a nice form
	Parameters:
		- table (str): the name of the table to be printed
		- enumerator (sequence of tuples): entries from the table
	'''
	# Print the columns of the table
	__print_columns(table)
	cnt = 0
	# Print each entry in a formatted line
	for index, entry in enumerator:
		entry = [str(val) for val in entry]
		print(('%d | ' % (index + 1)) + ' | '.join(entry))
		cnt += 1
	# Display the amount of entries found
	print('%d results found.' % cnt)

def __print_table(table):
	'''
	Print a table
	Parameters:
		- table (str): the name of the table to be printed
	'''
	table_enum = enumerate(db.iter_entries(table))
	__print_results(table, table_enum)

def print_seperetor(size=10):
	'''
	Print a seperetor to sepreate different sections of the UI
	Parameters:
		- size (int): the size of the seperetor
	'''
	# Make sure it's an int
	if not isinstance(size, int):
		size = 10
	print('-' * size)

# def search_library(bookname):
# 	''' Search for books in the library '''
# 	res_enum = enumerate(db.search('Books', 'Name', bookname, True, False))
# 	__print_results('Books', res_enum)





