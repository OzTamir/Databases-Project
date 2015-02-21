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
    - __init__.py   : Package file
  	- config.py 	  : Defines Config, the configuration object
  	- database.py 	: Defines Database, which is the wrapper for the MySQL object
  	- system.py 	  : Defines the System object, which is the main object in this project
  	- utils.py 		  : Defines various utility functions
  
  - ui/
    - Menus/
      - __init__.py       : Package file
      - main_menu.py 			: Includes class for the main menu
      - menu_base.py 			: Includes the base class for menus
      - add_menu.py			  : Defines a menu that add items
      - view_menu.py			: Defines a menu that shows items
    
    - Views/
      - __init__.py         : Package file
      - inventory_view.py   : Defines a class that allows to view the inventory
      - suppliers_view.py   : Defines a class that allows the user to view suppliers
      - orders_view.py      : Defines a class that allows the user to view orders
      - purchase_view.py    : Defines a class that allows the user to view purchases
      - new_product.py      : Includes class for new product
      - new_purchase.py     : Includes class for new purchase
      - new_order.py        : Defines a class for new orders
      - view_base.py        : Includes the base class for views
    
    - ui_utils.py 	: Includes utility functions for UI
    - ui_manager.py : Define the UIManager, responsible for handling UI
	 
  - README.md   : Instructions for how to run the project
  - config.json : Configuration file
  - project.py  : Main project file
  - .gitignore  : Make git ignore configuration files and python compiled files

```

***

## TODO:
Those are the things left to do before I submit the project. The sub-lists are by order of importance.

  - Finish the actual project part:
    - Editing/Deleting inventory, products, categories, suppliers, orders
    - Viewing products, categories
    - Creating categories
  
  - Minor improvments :
    - Better documentation
    - Add a first-time setup screen, allowing to set initial setting for the config file
    - Add a settings view, allowing to change the configuration
    - Bettre error numbring (Exit status codes need to mean something)
    - Add more options to the configuration file
    - Add a log file
  
  
  
  
  
