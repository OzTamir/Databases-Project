# Databases-Project
End of semester project in Databases - A Bakery Management System, with MySQL backend &amp; Python CLI

***

## How to use
Requirements:
```
  - MySQL Database with the attached scheme (scheme will be commited soon)
  - Python 2.7
  - MySQL Connector for Python 2.7
```

In order to run the project, change those details in *config.json*:
```
  - db.host : Your MySQL server's IP
  - db.username : Username used to login to your MySQL server
  - db.password : Password used to login to your MySQL server (Should match with the username...)
  - db.name : The database's name on the server
  - db.port : The port in which the database is configured to listen
```

You can tweak additonal settings by changing the other parameters in the config.json file.

## Project Structure
```
- Databases-Project

  - core/
    - __init__.py		: Package file
    
    - config.py			      : Defines Config, the configuration object
    - database.py		      : Defines Database, which is the wrapper for the MySQL object
    - system.py			      : Defines the System object, which is the main object in this project
    - datebase_scheme.py  : The Database's scheme
    - setup.py            : Setup the database scheme
    - utils.py			      : Defines various utility functions
  
  - ui/
    - Menus/
      - __init__.py       	: Package file
      - menu_base.py 		: Includes the base class for menus
      - main_menu.py 		: Includes class for the main menu
      
      - add_menu.py		: Defines a menu that add items
      - view_menu.py		: Defines a menu that shows items
      - purchase_menu.py	: Defines a menu that shows purchases options
      - orders_menu.py		: Defines a menu that shows orders options
    
    - Views/
      - __init__.py         	: Package file
      - view_base.py		: Includes the base class for views

      - redeem_order.py   : Redeem an order and add it to the inventory
      
      - inventory_view.py	: Defines a class that allows to view the inventory
      - suppliers_view.py 	: Defines a class that allows the user to view suppliers
      - orders_view.py 		: Defines a class that allows the user to view orders
      - products_view.py 	: Defines a class that allows the user to view products
      - purchase_view.py	: Defines a class that allows the user to view purchases
      - categories_view.py	: Defines a class that allows the user to view categories
      - stats_view.py		: Defines a class that shows systam statistics
      
      - new_product.py 		: Includes class for new product
      - new_purchase.py 	: Includes class for new purchase
      - new_order.py		: Defines a class for new orders
      - new_category.py   : Defines a view for creating new categories
    
    - ui_utils.py		: Includes utility functions for UI
    - ui_manager.py		: Define the UIManager, responsible for handling UI
	 
  - README.md			: Instructions for how to run the project
  - config.json			: Configuration file
  - project.py			: Main project file
  - .gitignore			: Make git ignore configuration files and python compiled files

```
  
  
  
  
  
