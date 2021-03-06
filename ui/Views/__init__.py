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
# Filename:		__init__.py
# Description:	This is the init file for the UI.Views package
#
####################################

'''
This package contains all the classes that defines views

Files:
	- inventory_view.py		: Defines a class that allows to view the inventory
	- suppliers_view.py 	: Defines a class that allows the user to view suppliers
	- orders_view.py 		: Defines a class that allows the user to view orders
	- products_view.py 		: Defines a class that allows the user to view products
	- purchase_view.py		: Defines a class that allows the user to view purchases
	- categories_view.py	: Defines a class that allows the user to view categories
	- stats_view.py			: Defines a class that shows systam statistics

	- new_product.py 		: Includes class for new product
	- new_purchase.py 		: Includes class for new purchase
	- new_order.py			: Defines a class for new orders
	- new_category.py		: Defines a view for creating new categories

	- redeem_order.py		: Redeem an order and add it to the inventory

	- view_base.py 			: Includes the base class for views
'''

from view_base import ViewBase

# Views for adding data
from new_product import NewProduct
from new_purchase import NewPurchase
from new_order import NewOrder
from new_category import NewCategory

# Views for viewing data
from inventory_view import InventoryView
from suppliers_view import SuppliersView
from purchase_view import PurchaseView
from orders_view import OrdersView
from products_view import ProductsView
from categories_view import CategoriesView
from stats_view import StatsView

# Other
from redeem_order import RedeemOrder


