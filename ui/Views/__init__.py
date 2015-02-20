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
	- new_product.py 		: Includes class for new product
	- new_purchase.py 		: Includes class for new purchase
	- view_base.py 			: Includes the base class for views
'''

from view_base import ViewBase
from new_product import NewProduct
from new_purchase import NewPurchase