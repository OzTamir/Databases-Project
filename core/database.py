####################################
#
# Databases project - Core Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			20 - 02 - 2015
#
####
#
# Filename:		database.py
# Description:	Define a database object which is the gateaway to the db server
#
####################################

from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.errors import *
import sys
import utils

class Database(object):
	def __init__(self, config):
		'''
		Intialize a Database object and connect to the database
		Parameters:
			- config (Config): the configuration object
		'''
		self.conf = config
		self.host = config.host
		self.name = config.name
		self.debug = config.debug
		self.conn = None
		
		# Try to connect to the database, and if there were any
		# errors report then and quit.
		try:
			self.conn = self.get_connector(config.username, config.password,\
																 config.port)
		
		# Catch any exceptions that are MySQL's "fault"
		except mysql.connector.Error as err:
			utils.error(err, 'Error connecting to the host.', \
						'Database.__init__()', True)
		
		# Catch other exceptions
		except Exception, e:
			utils.error(e, '', 'Database.__init__()', True)
		
		if self.debug:
			print('Connected to host.')
		
		# Get the cursor
		self.cursor = self.conn.cursor()

	def get_connector(self, username, dbpass, port=3306):
		'''
		Connect to the database and return the connector
		Parameters:
			- username (str): the database's username
			- dbpass (str): the database's password
			- port (int): the MySQL server's port (default - 3306)
		'''
		if self.debug:
			print('Connecting to database...')
		# If there is an active connection ,return it
		if isinstance(self.conn, mysql.connector.connection.MySQLConnection):
			if self.debug:
				print('Already connected!')
			return self.conn
		
		# Create a connection and return in
		return mysql.connector.connect(user = username, password = dbpass, \
										host = self.host, \
										database = self.name, port=port)

	def __get_results(self, query, err_msg='Database.__get_results', \
															data=None):
		'''
		Return all the results from a query
		Parameters:
			- query (str): the query to run
			- err_msg (str): What should the error message read
			- data (iterable): any data that should be passed to the query
		'''
		
		# Try to run the query
		try:
			# If there is data, run the query and pass the data
			if data:
				self.cursor.execute(query, data)
			# Else, just run the query
			else:
				self.cursor.execute(query)
		
		# Report any errors
		except InternalError as e:
			utils.error(e, e.msg, err_msg)
			return []
		
		# Return the results
		return self.cursor.fetchall()

	def __iter_results(self, query, err_msg='Database.__get_results', \
															data=None):
		'''
		Return a generetor that yields results from a query
		Parameters:
			- query (str): the query to run
			- err_msg (str): What should the error message read
			- data (iterable): any data that should be passed to the query
		'''
		
		# Try to run the query
		try:
			# If there is data, run the query and pass the data
			if data:
				self.cursor.execute(query, data)
			# Else, just run the query
			else:
				self.cursor.execute(query)
		
		# Report any errors
		except InternalError as e:
			utils.error(e, e.msg, err_msg)
			raise StopIteration
		
		# yield the results
		for entry in self.cursor:
			yield entry

	def get_entries(self, table):
		'''
		Return all the entries from a given table in the database
		Parameters:
			- table (str): the table from which we want to get entries
		'''
		return self.__get_results('SELECT * FROM %s' % str(table), \
									'get_entries')

	def iter_entries(self, table):
		'''
		Return a generetor that yields entries from a given
		table in the database.
		Parameters:
			- table (str): the table from which we want to get entries
		'''
		return self.__iter_results('SELECT * FROM %s' % str(table),\
									'iter_entries')

	def get_column_names(self, table):
		'''
		Wrapper for get_columns, only return the names and not types
		Parameters:
			- table (str): the table from which we want to get columns
		'''
		return [col[0] for col in self.get_columns(table)]

	def get_columns(self, table):
		'''
		Get the column names in a given table in the database
		Parameters:
			- table (str): the table from which we want to get columns
		'''
		self.cursor.execute('SELECT * FROM %s' % str(table))
		# Return the column names and types from the cursor description {n : t}
		columns = [(i[0], i[1]) for i in self.cursor.description]
		# Clear the buffer to avoid 'Unread result'
		self.clear_cursor()
		# Return the result
		return columns

	def close_connection(self):
		'''
		Close the connection
		'''
		self.conn.close()
		if self.debug:
			print('Connection closed.')

	def clear_cursor(self):
		'''
		Clear the cursor if we don't need results (used in get_columns)
		'''
		if self.debug:
			print('Clearing cursor...')
		self.cursor.fetchall()

	def commit(self):
		'''
		Commit changes to the remote DB
		'''
		if self.debug:
			print('Commiting changes...')
		self.conn.commit()

	def rollback(self):
		'''
		Rollback changes in case of errors of any kind
		'''
		if self.debug:
			print('Rolling back...')
		self.conn.rollback()

	def insert(self, table, columns, values, auto_commit=True):
		'''
		Insert a new entry into a table with given values
		Parameters:
			- table (str): the table we want to insert into
			- columns (iterable): the columns we want to insert into
			- values (iterable): the values we want to insert
			- auto_commit (bool): wheter or not should the function commit		
		'''
		# Get the columns's names
		columns = str(tuple([str(x) for x in columns]))
		# Create the query statment
		query = 'INSERT INTO %s %s' % (table, columns.replace("'", ''))
		values_query = 'VALUES (' + ('%s, ' * len(values))[:-2] + ')'
		query_stmt = ' '.join([
			query,
			values_query
		])
		
		# Try to execute the query
		try:
			self.cursor.execute(query_stmt, values)
			# If the function should commit changes
			if auto_commit:
				# Commit the changes to the remote DB
				self.commit()
		
		# Catch any exceptions and initiate a rollback
		except Exception, e:
			# Print exception details if in debug mode
			utils.error(e, '', 'Database.insert')
			# Rollback the changes from the current transaction
			self.rollback()
			raise ValueError("Can't add entry, please try again \
							(maybe with different values?)")

	def search(self, table, column, value, partial=False, case_sensetive=True):
		'''
		Search for value in table
		Parameters:
			- table (str): the table we want to search in
			- column (str): the column we want to compare to
			- value (str): the value we want to compare to
			- partial (bool): wheter a partial match will suffice
			- case_sensetive (bool): wheter the search should be case_sensetive
		'''

		# Create the basic select statment
		select_stmt = 'SELECT * FROM %s WHERE' % str(table)
		
		# If we want that partial match will suffice
		if partial:
			sql_function = 'LIKE'
			value = '%%%s%%' % str(value)
		else:
			sql_function = '='
		
		# If we want the search to be case sensetive
		if case_sensetive:
			condition = '''`%s` %s "%s"''' % (str(column), \
									sql_function, str(value))
		else:
			condition = '''LOWER(`%s`) %s LOWER("%s")''' % \
						(str(column), sql_function, str(value))
		
		# Build to query from it's parts
		query = ' '.join([select_stmt, condition])
		query = query.replace("'", '')
		return self.__iter_results(query, 'search')


	def get_single_result(self, table, column, value):
		'''
		Get a single result from a table
		Parameters:
			- table (str): the table to search in
			- column (str): the column to search on
			- value (str): the value to match for
		'''
		# Get the entries
		try:
			# Sometimes an unread result will raise an exception
			self.clear_cursor()
			# Get the values from the table as a list
			search_results = [x for x in self.search(table, column, str(value), False)]

		# And sometimes MySQL will raise an InterfaceError, requiring us
		# to run the search again.
		except InterfaceError:
			# Get the values from the table as a list
			search_results = [x for x in self.search(table, column, str(value), False)]

		# Make sure we have a product
		if len(search_results) == 0:
			return None

		# Return the first value
		return search_results[0]

	def update(self, table, match, update_dict, auto_commit=True):
		'''
		Update existing values in a table
		Parameters:
			- table (str): the table in which we would like to update values
			- match (tuple): a tuple of kind (column, value) to match against
			- update_dict (dictionary): dictionary of kind (column : new value)
			- auto_commit (bool): should the function commit changes
		'''
		# Initial UPDATE query
		update_stmt = 'UPDATE %s SET' % str(table)

		# Create a list for keys and a list of items (dict is unordered)
		keys = []
		values = []
		for key, value in update_dict.items():
			keys.append(str(key))
			values.append(value)

		# Create the keys string
		keys_str = ', '.join(['%s=%%s' % key for key in keys])

		# Create the where clause
		where_stmt = 'WHERE %s=%s' % (str(match[0]), str(match[1]))

		# Create the query statment
		query_stmt = ' '.join([
			update_stmt,
			keys_str,
			where_stmt
			])

		# Try to execute the query
		try:
			self.cursor.execute(query_stmt, values)
			# If the function should commit changes
			if auto_commit:
				# Commit the changes to the remote DB
				self.commit()
		
		# Catch any exceptions and initiate a rollback
		except Exception, e:
			# Print exception details if in debug mode
			utils.error(e, '', 'Database.update')
			# Rollback the changes from the current transaction
			self.rollback()
			raise ValueError("Can't update entry, please try again \
							(maybe with different values?)")

	def __del__(self):
		'''
		Called upon object deletion, make sure the connection
		to the DB is closed to avoid resource exhustion.
		'''
		try:
			# If the connection wasn't closed already
			if self.conn is not None:
				self.close_connection()
		# At this point, we don't care if there were any exceptions
		except Exception:
			pass

