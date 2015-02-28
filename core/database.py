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

logger = None

class Database(object):
	def __init__(self, config):
		'''
		Intialize a Database object and connect to the database
		Parameters:
			- config (Config): the configuration object
		'''
		global logger

		# Set the logger
		logger = utils.get_logger('core.database')

		self.conf = config
		self.host = config.host
		self.name = config.name
		self.debug = config.debug
		self.conn = None
		self.db_created = False
		
		# Try to connect to the database, and if there were any
		# errors report then and quit.
		try:
			self.conn = self.get_connector(config.username, config.password,\
																 config.port)
		
		# Catch any exceptions that are MySQL's "fault"
		except mysql.connector.Error as err:
			logger.debug('MySQL exception: %s' % str(err))
			logger.error('Error connecting to the host.')
		
		# Catch other exceptions
		except Exception, e:
			logger.error(str(e))
		
		# There were no errors!
		else:
			logger.debug('Connected to databse!')
		
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
		# Announce what we are doing
		logger.debug('Connecting to database...')
		# If there is an active connection ,return it
		if isinstance(self.conn, mysql.connector.connection.MySQLConnection):
			logger.debug('Already connected!')
			return self.conn
		
		# Create a connection and return in
		cnx = mysql.connector.connect(user = username, password = dbpass, \
										host = self.host, port=port)

		try:
			# Set the connection's database
			cnx.database = '`%s`' % str(self.conf.name)
			self.db_created = False
			return cnx

		except mysql.connector.Error as err:
			# If the problem is that the database doesn't exsist, create it
			if err.errno == errorcode.ER_BAD_DB_ERROR:
				self.create_database(cnx.cursor(), self.conf.name)
				cnx.database = self.conf.name
				self.db_created = True
				return mysql.connector.connect(user = username, password = dbpass, \
												host = self.host, \
												database = self.name, port=port)
			# Else, pass it to the caller
			else:
				raise err
	
	def create_database(self, cursor, db_name, charset='latin1'):
		'''
		Create a new database on the server
		Parameters:
			- cursor (mysql.connector.cursor): the cursor object
			- db_name (str): the name of the new database
			- charset (str): the default charset of the new database
		'''
		query = 'CREATE DATABASE IF NOT EXISTS `%s`'\
				 % str(db_name)#, str(charset))
		logger.debug(query)
		# Try to create the database
		try:
			cursor.execute(query)
		except mysql.connector.Error as err:
			# Log the error and pass the exception to caller
			logger.error('Error while creating database.')
			raise err

	def execute(self, query, multi_stmts=False, data=None):
		'''
		Excecute SQL query
		Parameters:
			- query (str): the query to execute
			- data (iterable): values to pass to the query
			- multi_stmts (bool): are we running multiple statments
		'''
		# Log the query
		logger.debug('Query: %s', str(query))
		logger.debug('Values: %s', str(data))

		# Excecute the query
		if data is not None:
			self.cursor.execute(query, data, multi=multi_stmts)
		else:
			self.cursor.execute(query, multi=multi_stmts)

	def __get_results(self, query, err_msg='Database.__get_results', \
															data=None):
		'''
		Return all the results from a query
		Parameters:
			- query (str): the query to run
			- err_msg (str): What should the error message read
			- data (iterable): any data that should be passed to the query
		'''
		# Log the query
		logger.debug('Query: %s', str(query))
		logger.debug('Values: %s', str(data))

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
			logger.debug('MySQL InternalError: %s' % str(e))
			logger.info('No results for query: %s' % str(query))
			logger.info('Passed data: %s' % str(data))
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
		# Log the query
		logger.debug('Query: %s', str(query))
		logger.debug('Values: %s', str(data))

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
			logger.debug('MySQL InternalError: %s' % str(e))
			logger.info('No results for query: %s' % str(query))
			logger.info('Passed data: %s' % str(data))
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
		logger.debug('Connection closed.')

	def clear_cursor(self):
		'''
		Clear the cursor if we don't need results (used in get_columns)
		'''
		logger.info('Clearing cursor...')
		self.cursor.fetchall()

	def commit(self):
		'''
		Commit changes to the remote DB
		'''
		logger.info('Commiting changes...')
		self.conn.commit()

	def rollback(self):
		'''
		Rollback changes in case of errors of any kind
		'''
		logger.info('Rolling back...')
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
		if len(columns) == 1:
			columns = str('(%s)' % str(columns[0]))
		else:
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
			logger.debug('Error running Query: %s' % str(query_stmt))
			logger.debug('With Values: %s' % str(values))
			logger.debug('Exception info: %s' % str(e))
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
			logger.debug('Exception: %s' % str(e))
			# Rollback the changes from the current transaction
			self.rollback()
			raise ValueError("Can't update entry, please try again \
							(maybe with different values?)")

	def search_range(self, table, column, start, end, include_edges=True):
		'''
		Return all the results in a certing range
		Parameters:
			- table (str): the table to search in
			- column (str): the column to match against
			- start (type(column)): the minimal value
			- end (type(column)): the maximal value
			- include_edges (bool): whether to return the edges (>= or >)
		'''
		# Check if we want edges
		if include_edges:
			op_suffix = '='
		else:
			op_suffix = ''

		# Craft the select statment
		select_stmt = 'SELECT * FROM %s WHERE' % str(table)

		# Craft the between statment
		range_stmt = '%s >%s \'%s\' and %s <%s \'%s\'' % (
					str(column), op_suffix, str(start), str(column), \
					op_suffix, str(end))

		# Build to query from it's parts
		query = ' '.join([select_stmt, range_stmt])
		return self.__get_results(query, 'search_range')

	def sum_column(self, table, column, match=None, res_range=None):
		'''
		Get the sum of all the values in a column
		Parameters:
			- table (str): the table to search in
			- column (str): the column whose values we want to sum
			- match (tuple): a tuple of (column, value) to filter by
			- res_range (tuple): a tuple of (column, start, end) to 
								threshold results (column is the column to 
								thresh by, for example date column)
		'''

		# Craft the select statment
		select_stmt = 'SELECT sum(%s) FROM %s' % (str(column), str(table))

		# Store the query's other parts in a list
		query = []

		# If we want to filter results
		if match is not None:
			query.append('%s=%s' % (str(match[0]), str(match[1])))

		# If we have a range
		if res_range is not None:
			# Get the range details
			col, start, end = res_range
			# Craft the between statment
			range_stmt = '%s >= \'%s\' and %s <= \'%s\'' % \
							(str(col), str(start), str(col), str(end))
			query.append(range_stmt)

		# Check to see if we have a where clause
		if len(query) > 0:
			query = ' '.join([select_stmt, 'WHERE', \
						' and '.join(query)])
		else:
			query = select_stmt

		return self.__get_results(query, 'sum_column')[0][0]

	def sorted_results(self, table, sort_by_column, match=None, desc=False):
		'''
		Get sorted results from the DB
		Parameters:
			- table (str): the table to search in
			- sort_by_column (str): the column to sort results by
			- match (tuple): if we want to filter, we pass (column, value)
			- desc (bool): if True, values will be sorted in a descending order
		'''
		# Store the different parts of the query here
		query = []

		# Craft the select statment
		select_stmt = 'SELECT * FROM %s' % str(table)
		query.append(select_stmt)

		# Craft the where clause
		if match is not None:
			where_stmt = 'WHERE %s=%s' % (str(match[0]), str(match[1]))
			query.append(where_stmt)

		# Craft the order by clause
		order_by_stmt = 'ORDER BY %s' % str(sort_by_column)
		query.append(order_by_stmt)

		# Set the sort order
		choose_func = lambda desc: ('DESC' * int(desc)) + ('ASC' * int(not desc))
		sort_order = choose_func(desc)
		query.append(sort_order)

		# Get the query string and return the results
		query_str = ' '.join(query)
		return self.__get_results(query_str, 'sorted_results')

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

