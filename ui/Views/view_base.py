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
# Filename:		view_base.py
# Description:	Defines the base class for views
#
####################################

class ViewBase(object):
	''' A base class for views '''
	def __init__(self, db, config=None, edit=False):
		'''
		Initialize the ViewBase object
		Parameters:
			- db (Database): the database object
			- config (Config): optional configuration object
			- edit (bool): Should we allow editing the data after viewing it
		'''
		self.db = db
		self.edit = edit
		# We sometimes need things from the configuration file
		if config is not None:
			self.config = config

	def __call__(self):
		'''
		Make View objects callable
		'''
		# Print a newline
		print('')

		# Show the view
		self.show_view()

		# If we allow editing, run the function
		if self.edit:
			self.show_edit()

	def show_view(self):
		'''
		Abstract method in which the view is presented
		'''
		raise NotImplemented

	def show_edit(self):
		'''
		Abstract method in which the edit view is presented
		'''
		raise NotImplemented
