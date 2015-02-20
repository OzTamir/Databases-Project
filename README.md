# Databases-Project
End of semester project in Databases - A Bakery Management System, with MySQL backend &amp; Python CLI

***

## How to use
Requirements:
  - MySQL Database with the attached scheme (scheme will be commited soon)
  - Python 2.7
  - MySQL Connector for Python 2.7
  
In order to run the project, change those details in *config.json*:
  - db.host : Your MySQL server's IP
  - db.username : Username used to login to your MySQL server
  - db.password : Password used to login to your MySQL server (Should match with the username...)
  - db.name : The database's name on the server
  - db.port : The port in which the database is configured to listen
  
You can tweak additonal settings by changing the other parameters in the config.json file.

## Project Structure
  - README.md: Instructions for how to run the project
  - config.json: Configuration file
  - config.py: Configuration Class definition
  - database.py: Database Class definition (Responsiable for interacting with the MySQL server)
  - ui.py: Base class for all UI elements
  - project.py: Main project file

***

## TODO:
Those are the things left to do before I submit the project. The sub-lists are randomly ordered.

  - Finish the actual project part:
    - Main menu
    - Viewing the inventory, suppliers, orders, and purchases (All including search option)
    - Adding purchases, orders, products, and if there is time left suppliers.
    
  - Move towards MVC design pattren:
    - Add a class to handle errors and present it to the user (Singleton)
    - Rewrite the architacture of the UI (Split it to menus, table views, input views etc.)
    - Add a main I/O (reading input and printing output) handler which will be used as the controller and 
      will make sure that we go back to the menu whenever -1 is being recived as input(Singleton)
  
  - Minor improvments (By order of importance):
    - Better documentation
    - Bettre error handling (Exit status codes need to mean something)
    - Change the project structure to a package like (with folders and more files/modolarity)
    - Add a log file
    - Add more options to the configuration file
    - Add a settings view, allowing to change the configuration
  
  
  
  
  
