from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.errors import *
import sys
import utils

class Database(object):
	def __init__(self, config):#dbhost, dbuser, dbpass, dbname, debug=False, port=3306):
		''' Intialize a Database object and connect to the database '''
		self.conf = config
		self.host = config.host
		self.name = config.name
		self.debug = config.debug
		self.conn = None
		# Try to connect to the database, and if there were any errors report and quit
		try:
			self.conn = self.get_connector(config.username, config.password, config.port)
		except mysql.connector.Error as err:
			utils.error(err, 'Error connecting to the host.', \
						'Database.__init__()', True)
		
		if self.debug:
			print('Connected to host.')
		# Get the cursor
		self.cursor = self.conn.cursor()

	def get_connector(self, username, dbpass, port):
		''' Connect to the database and return the connector '''
		if self.debug:
			print('Connecting to database...')
		# If there is an active connection ,return it
		if isinstance(self.conn, mysql.connector.connection.MySQLConnection):
			if self.debug:
				print('Already connected!')
			return self.conn
		return mysql.connector.connect(user = username, password = dbpass, host = self.host, database = self.name, port=port)

	def __get_results(self, query, err_msg='get_results', data=None):
		''' Return all the results from a query '''
		try:
			if data:
				self.cursor.execute(query, data)
			else:
				self.cursor.execute(query)
		except InternalError:
			if self.debug:
				print('Error in %s: No results for table %s' % (str(err_msg), str(table)))
			return []
		return self.cursor.fetchall()

	def __iter_results(self, query, err_msg='__iter_results', data=None):
		''' Return a generetor that yields results from a query '''
		try:
			if data:
				self.cursor.execute(query, data)
			else:
				self.cursor.execute(query)
		except InternalError:
			if self.debug:
				print('Error in %s: No results for table %s' % (str(err_msg), str(table)))
			raise StopIteration
		for entry in self.cursor:
			yield entry

	def get_entries(self, table):
		''' Return all the entries from a given table in the database '''
		return self.__get_results('SELECT * FROM %s' % str(table), 'get_entries')

	def iter_entries(self, table):
		''' Return a generetor that yields entries from a given table in the database '''
		return self.__iter_results('SELECT * FROM %s' % str(table), 'iter_entries')

	def get_column_names(self, table):
		''' Wrapper for get_columns, only return the names and not types '''
		return [col[0] for col in self.get_columns(table)]

	def get_columns(self, table):
		''' Get the column names in a given table in the database '''
		self.cursor.execute('SELECT * FROM %s' % str(table))
		# Return the column names and types from the cursor description {n : t}
		columns = [(i[0], i[1]) for i in self.cursor.description]
		# Clear the buffer to avoid 'Unread result'
		self.clear_cursor()
		# Return the result
		return columns

	def close_connection(self):
		''' Close the connection '''
		self.conn.close()
		if self.debug:
			print('Connection closed.')

	def clear_cursor(self):
		''' Clear the cursor if we don't need results (used in get_columns) '''
		if self.debug:
			print('Clearing cursor...')
		self.cursor.fetchall()

	def commit(self):
		''' Commit changes to the remote DB '''
		if self.debug:
			print('Commiting changes...')
		self.conn.commit()

	def rollback(self):
		''' Rollback changes in case of errors of any kind '''
		if self.debug:
			print('Rolling back...')
		self.conn.rollback()

	def insert(self, table, columns, values, auto_commit=True):
		''' Insert a new entry into a table with given values '''
		# Get the columns's names
		columns = str(tuple([str(x) for x in columns]))
		# Create the query statment
		query = 'INSERT INTO %s %s' % (table, columns.replace("'", ''))
		values_query = 'VALUES (' + ('%s, ' * len(values))[:-2] + ')'
		query_stmt = ' '.join([
			query,
			values_query
		])
		try:
			self.cursor.execute(query_stmt, values)
			if auto_commit:
				# Commit the changes to the remote DB
				self.commit()
		except Exception, e:
			# Print exception details if in debug mode
			utils.error(e, '', 'Database.insert')
			# Rollback the changes from the current transaction
			self.rollback()
			raise ValueError("Can't add entry, please try again (maybe with different values?)")

	def search(self, table, column, value, partial=False, case_sensetive=True):
		''' Search for value in table '''
		select_stmt = 'SELECT * FROM %s WHERE' % str(table)
		# If we want that partial match will suffice
		if partial:
			sql_function = 'LIKE'
			value = '%%%s%%' % str(value)
		else:
			sql_function = '='
		# If we want the search to be case sensetive
		if case_sensetive:
			condition = '''`%s` %s "%s"''' % (str(column), sql_function, str(value))
		else:
			condition = '''LOWER(`%s`) %s LOWER("%s")''' % (str(column), sql_function, str(value))
		# Build to query from it's parts
		query = ' '.join([select_stmt, condition])
		query = query.replace("'", '')
		return self.__iter_results(query, 'search')

	def __del__(self):
		''' Called upon object deletion, make sure the connection to the DB is closed '''
		if self.conn is not None:
			self.close_connection()

