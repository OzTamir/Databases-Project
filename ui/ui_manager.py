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
# Filename:		ui_manager.py
# Description:	This file defines a UI Manager class, 
#				which is the main object used in UI context
#
####################################

# Import utilities
import ui_utils
from core.utils import error

# Import Views
from Views import NewPurchase
from Views import NewProduct
from Views import NewOrder
from Views import OrdersView
from Views import InventoryView
from Views import SuppliersView
from Views import PurchaseView

# Import Menus
from Menus import MainMenu
from Menus import AddMenu
from Menus import ViewMenu

# Import sys for sys.exit (avoided 'from sys import exit' to maintain standart)
import sys

class UIManager(object):
	''' UIManager is the main object used in UI context '''
	def __init__(self, db, config):
		'''
		Create a UI object and set it's properties
		'''
		# Set the DB object
		self.db = db
		# Set the Configuration object
		self.config = config

		# Set the views (creating)
		self.new_purchase = NewPurchase(db)
		self.new_product = NewProduct(db)
		self.new_order = NewOrder(db, config)
		
		# Set the views (viewing)
		self.inventory_view = InventoryView(db, config, True)
		self.suppliers_view = SuppliersView(db)
		self.purchase_view = PurchaseView(db, config)
		self.orders_view = OrdersView(db, config)


		# Set the menus
		self.add_menu = AddMenu(config, self)
		self.view_menu = ViewMenu(config, self)
		self.main_menu = MainMenu(config, self)

		# Keep a log of menus hierarchy
		# This is used like a stack of views
		self.stack = [self.main_menu]

		# Print the title message
		print(config.title_msg)
		ui_utils.print_seperetor()

	def __call__(self):
		'''
		Make UIManager callable.
		This will run the top (last) item from the stack list
		and will pop it. If the stack is empty, it will quit the program.
		'''
		
		# If the view stack is empty, than there is nowhere to return to and we
		# will quit the program.
		if len(self.stack) == 0:
			# Inform the user
			print('Shutting down...')
			
			# Close the connection to the database
			# This is done inside a try block because sometimes, 
			# MySQL won't quit and an exception will be raised
			try:
				self.db.close_connection()
			
			# Since we're quiting, there is no point in handling any exceptions
			finally:
				# Quit
				sys.exit(0)
		
		try:
			# Get the view
			view = self.stack.pop(-1)
			# Try to call the view
			view()
		
		# If it's not callable, something went wrong and we need to quit
		except TypeError, e:
			error(e, 'Error: View is not callable', 'UIManager.__call__', True)
		
		# If something else went wrong...
		except Exception, e:
			error(e, '', 'UIManager.__call__', True)
		
		# Make a recursive call to reach the stopping condition
		finally:
			self.__call__()





