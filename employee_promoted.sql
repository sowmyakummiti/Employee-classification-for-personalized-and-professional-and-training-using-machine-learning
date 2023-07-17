/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - employee_ promoted
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`employee_promoted` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `employee_promoted`;

/*Table structure for table `employee1` */

DROP TABLE IF EXISTS `employee1`;

CREATE TABLE `employee1` (
  `s no` int(100) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`s no`,`name`,`email`,`password`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `employee1` */

insert  into `employee1`(`s no`,`name`,`email`,`password`) values (1,'Sowmya','sowmya@gmail.com','12345678'),(2,'Swathi','swathi@gmail.com','444444'),(3,'shasi','shasi@gmail.com','7654321'),(4, 'Siddartha','siddartha@gmail.com', '123456');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
SET SQL_SAFE_UPDATES = 1;

select * from employee1;
