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