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
	def __init__(self, db):
		self.db = db

	def __call__(self):
		'''
		Make View objects callable
		'''
		self.show_view()

	def show_view(self):
		'''
		Abstract method in which the view is presented
		'''
		raise NotImplemented
