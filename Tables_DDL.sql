-- create a test database to organize the tables
CREATE DATABASE testdb;
-- use the above created database
use testdb;
-- create the customer table
CREATE TABLE `customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `aadhar_number` varchar(12) DEFAULT NULL,
  `mobile_number` varchar(10) DEFAULT NULL,
  `bal` int(45) DEFAULT NULL,
  `account_number` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
-- create the cards table and use customer id as Foreign key
CREATE TABLE `carddetails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `card_number` varchar(16) DEFAULT NULL,
  `cvv` varchar(3) DEFAULT NULL,
  `mpin` varchar(4) DEFAULT NULL,
  `type` char(1) DEFAULT NULL,
  `cust_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_carddetails_1_idx` (`cust_id`),
  CONSTRAINT `fk_carddetails_1` FOREIGN KEY (`cust_id`) REFERENCES `customer` (`id`) ON UPDATE CASCADE
);
/*
create the transactions table and create to_account and from_account as foreign keys that refers
to the customer id in cusomer table.
*/ 
CREATE TABLE `transactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_account` int(11) DEFAULT NULL,
  `to_account` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_transactions_1_idx` (`from_account`),
  KEY `fk_transactions_2_idx` (`to_account`),
  CONSTRAINT `fk_transactions_1` FOREIGN KEY (`from_account`) REFERENCES `customer` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transactions_2` FOREIGN KEY (`to_account`) REFERENCES `customer` (`id`) ON UPDATE CASCADE
);
-- create beneficiaries table to send data directly using account number and ifsc code
-- use customer id as foreign key
CREATE TABLE `beneficiary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `b_name` varchar(255) DEFAULT NULL,
  `ifsc_code` varchar(11) DEFAULT NULL,
  `account_number` varchar(12) DEFAULT NULL,
  `cust_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_beneficiary_1_idx` (`cust_id`),
  CONSTRAINT `fk_beneficiary_1` FOREIGN KEY (`cust_id`) REFERENCES `customer` (`id`) ON UPDATE CASCADE
)
