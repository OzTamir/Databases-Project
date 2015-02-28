####################################
#
# Databases project - core Package
#
####
#
# Written by:	Oz Tamir
# Email:		TheOzTamir@gmail.com
# Date:			25 - 02 - 2015
#
####
#
# Filename:		setup.py
# Description:	Setup the database on the server
#
####################################

from database_scheme import TABLES, DROPS, DATA
import utils
import sys

try:
	import mysql.connector
	from mysql.connector import errorcode
except ImportError:
	print('MySQL connector couldn\'t be found. Please reinstall and try again.')
	sys.exit(0)

logger = None

class Setup(object):
	''' Setup the database on the remote server '''
	def __init__(self, db, config):
		global logger

		# Set the logger
		logger = utils.get_logger('core.setup')

		# Since we might destroy data, inform the user
		print('The system will now setup the database on the server.')
		print('This might cause loss of data, exsiting scheme and such.')
		quit = raw_input('Would you like to continue? (Y/N)')
		# If he does want out,
		if quit.lower() == 'n' or quit.lower() == 'no':
			print('Database setup canceled, quitting.')
			sys.exit(0)

		# Save the database, config
		self.db = db
		self.config = config

		# Run the setup
		self.run_setup()

		# Ask if the user wants to populate the tables with sample data
		quit = raw_input('Would you like to populate the DB with sample data? (Y/N)')
		# If he does want out,
		if quit.lower() == 'n' or quit.lower() == 'no':
			return
		# Else, fill it with data
		self.populate_tables()

	def run_setup(self):
		'''
		Create the database scheme on the db
		'''
		# Use our DB
		self.db.execute('USE `%s`;' % str(self.config.name))

		# Drop all exsiting tables
		for drop in DROPS:
			self.db.execute(drop)

		# Iterate over the tables
		for name, ddl in TABLES.iteritems():
			# Try to create the table
			try:
				logger.info('Creating table %s: ' % str(name))
				self.db.execute(ddl)
			
			except mysql.connector.Error as err:				
				logger.warning('Warning: %s' % str(err.msg))
			
			else:
				logger.debug('Table %s created.' % str(name))

			logger.debug('\n')

		# Commit changes
		self.db.commit()

	def populate_tables(self):
		'''
		Populate the tables with sample data
		'''
		# Use our DB
		self.db.execute('USE `%s`;' % str(self.config.name))

		# Insert data
		for insert in DATA:
			self.db.execute(insert)

		# Commit changes
		self.db.commit()