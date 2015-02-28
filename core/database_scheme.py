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
# Filename:		database_scheme.py
# Description:	Defines the database's scheme
#
####################################

DB_NAME = 'user11-db'

DROPS = [
	"DROP TABLE IF EXISTS `Inventory`;",
	"DROP TABLE IF EXISTS `Orders`;",
	"DROP TABLE IF EXISTS `ProductCategories`;",
	"DROP TABLE IF EXISTS `Products`;",
	"DROP TABLE IF EXISTS `Purchases`;",
	"DROP TABLE IF EXISTS `Suppliers`;",
	"DROP TABLE IF EXISTS `PurchasesItems`;"
]

DATA = [
	"INSERT INTO `ProductCategories` VALUES (1,'Pastries');",
	"INSERT INTO `Purchases` VALUES (1,1,1,'0000-00-00'),(9,4,4,'0000-00-00'),(10,5,17,'0000-00-00'),(11,7,19,'0000-00-00'),(12,3,15,'2015-02-24'),(13,3,3,'2015-02-25');",
	"INSERT INTO `Suppliers` VALUES (1,'Simshon Pastries'),(2,'Yossi Corn');",
	"INSERT INTO `Products` VALUES (1,'Corn',1,NULL,'Corn, as in Popcorn'),(8,'Burakas',5,1,'Yummy, filled with cheese');",
	"INSERT INTO `Inventory` VALUES (1,1,4,2),(2,8,4,1);",
	"INSERT INTO `PurchasesItems` VALUES (9,1,4),(10,8,3),(10,1,2),(11,8,3),(11,1,4),(12,8,3),(13,1,3);",
	"INSERT INTO `Orders` VALUES (1,2,1,6,1,'2015-02-21',0),(2,2,1,2,1,'2015-02-25',1);"
]

TABLES = {}

TABLES['Inventory'] = (
	"CREATE TABLE `Inventory` ("
	"  `InventoryItemID` int(11) NOT NULL AUTO_INCREMENT,"
	"  `Product` int(11) NOT NULL,"
	"  `UnitsInStock` int(11) DEFAULT NULL,"
	"  `Supplier` int(11) DEFAULT '0',"
	"  PRIMARY KEY (`InventoryItemID`),"
	"  KEY `PID_idx` (`Product`),"
	"  KEY `UnitsInStock` (`UnitsInStock`),"
	"  CONSTRAINT `PID` FOREIGN KEY (`Product`) REFERENCES `Products` (`PID`) ON DELETE CASCADE ON UPDATE CASCADE"
	") ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;")

TABLES['Orders'] = (
	"CREATE TABLE `Orders` ("
	"  `OID` int(11) NOT NULL AUTO_INCREMENT,"
	"  `SupplierID` int(11) DEFAULT NULL,"
	"  `ProductID` int(11) DEFAULT NULL,"
	"  `Amount` int(11) DEFAULT '0',"
	"  `PricePerUnit` float DEFAULT '0',"
	"  `OrderDate` date NOT NULL,"
	"  `Recived` tinyint(1) DEFAULT '0',"
	"  PRIMARY KEY (`OID`),"
	"  KEY `fk_PID_idx` (`ProductID`),"
	"  KEY `fk_SID_idx` (`SupplierID`),"
	"  CONSTRAINT `fk_PID` FOREIGN KEY (`ProductID`) REFERENCES `Products` (`PID`) ON DELETE NO ACTION ON UPDATE NO ACTION,"
	"  CONSTRAINT `fk_SID` FOREIGN KEY (`SupplierID`) REFERENCES `Suppliers` (`SID`) ON DELETE NO ACTION ON UPDATE NO ACTION"
	") ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;")

TABLES['ProductCategories'] = (
	"CREATE TABLE `ProductCategories` ("
	"  `CID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Category ID',"
	"  `CategoryName` varchar(255) NOT NULL,"
	"  PRIMARY KEY (`CID`)"
	") ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;")


TABLES['Products'] = (
	"CREATE TABLE `Products` ("
	"  `PID` int(11) NOT NULL AUTO_INCREMENT,"
	"  `ProductName` varchar(255) NOT NULL,"
	"  `PricePerUnit` double DEFAULT '0',"
	"  `Category` int(11) DEFAULT NULL,"
	"  `Description` tinytext,"
	"  PRIMARY KEY (`PID`),"
	"  UNIQUE KEY `ProductID_UNIQUE` (`PID`),"
	"  KEY `CID_idx` (`Category`),"
	"  CONSTRAINT `CID` FOREIGN KEY (`Category`) REFERENCES `ProductCategories` (`CID`) ON DELETE SET NULL ON UPDATE CASCADE"
	") ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;")

TABLES['Purchases'] = (
	"CREATE TABLE `Purchases` ("
	"  `PurchaseID` int(11) NOT NULL AUTO_INCREMENT,"
	"  `Amount` int(11) DEFAULT '0',"
	"  `Total` float DEFAULT '0',"
	"  `PurchaseDate` date NOT NULL,"
	"  PRIMARY KEY (`PurchaseID`)"
	") ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;")

TABLES['Suppliers'] = (
	"CREATE TABLE `Suppliers` ("
	"  `SID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Supplier ID',"
	"  `SupplierName` varchar(255) NOT NULL,"
	"  PRIMARY KEY (`SID`)"
	") ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;")

TABLES['PurchasesItems'] = (
	"CREATE TABLE `PurchasesItems` ("
	"  `PurchaseID` int(11) NOT NULL,"
	"  `ProductID` int(11) NOT NULL,"
	"  `Amount` int(11) NOT NULL,"
	"  KEY `fk_PurchaseID_idx` (`PurchaseID`),"
	"  KEY `fk_ProductID_idx` (`ProductID`),"
	"  CONSTRAINT `fk_ProductID_idx` FOREIGN KEY (`ProductID`) REFERENCES `Products` (`PID`) ON DELETE CASCADE ON UPDATE CASCADE,"
	"  CONSTRAINT `fk_PurchaseID_idx` FOREIGN KEY (`PurchaseID`) REFERENCES `Purchases` (`PurchaseID`) ON DELETE CASCADE ON UPDATE CASCADE"
	") ENGINE=InnoDB DEFAULT CHARSET=latin1;")