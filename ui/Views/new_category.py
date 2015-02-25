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
# Filename:		new_category.py
# Description:	Defines a view for creating new categories
#
####################################

from view_base import ViewBase
from ui.ui_utils import *

class NewCategory(ViewBase):
	''' Add categories '''

	def show_view(self):
		'''
		Implement the abstrect method show_view
		'''
		self.new_category()

	def new_category(self):
		'''
		Add to the categories table
		'''

		#### Constants ####
		CATEGORY_TABLE = 'ProductCategories'
		CATEGORY_COLUMNS = ['CategoryName']

		#### --- ####

		# Get the new category's name from the user
		new_cat = raw_input('Enter the new category\'s name: ')

		try:
			# Insert it to the database
			self.db.insert(CATEGORY_TABLE, CATEGORY_COLUMNS, [str(new_cat)], True)
		except Exception, e:
			# Print an error
			print('Error while creating new category.')











