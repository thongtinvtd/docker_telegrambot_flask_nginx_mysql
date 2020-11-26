-- phpMyAdmin SQL Dump
-- version 4.0.4.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 06, 2020 at 07:14 PM
-- Server version: 5.6.13
-- PHP Version: 5.4.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `test`
--
CREATE DATABASE IF NOT EXISTS `data_bot` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `data_bot`;

-- --------------------------------------------------------

--
-- Table structure for table `admin_manager`
--

CREATE TABLE IF NOT EXISTS `admin_manager` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`user_name`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `admin_manager`
--

INSERT INTO `admin_manager` (`id`, `user_name`, `password`, `status`) VALUES
(1, 'admin', 'pbkdf2:sha256:150000$D8JNnhoz$d01241d60f042c53b1721fbf95508f7439ace95e51ff471aa686e6e0bc377aca', 1);

-- --------------------------------------------------------

--
-- Table structure for table `alert_list`
--

CREATE TABLE IF NOT EXISTS `alert_list` (
  `user_id` varchar(50) CHARACTER SET cp1251 COLLATE cp1251_bin NOT NULL,
  `time_create` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_name` varchar(50) CHARACTER SET cp1251 COLLATE cp1251_bin NOT NULL,
  `permission` varchar(50) CHARACTER SET cp1251 COLLATE cp1251_bin NOT NULL,
  `comment` varchar(200) CHARACTER SET cp1251 COLLATE cp1251_bin DEFAULT NULL,
  `expiration` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `climate`
--

CREATE TABLE IF NOT EXISTS `climate` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `Time_request` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Temperature` decimal(10,2) NOT NULL,
  `Humidity` decimal(10,2) NOT NULL,
  `Temperature_set` decimal(7,2) DEFAULT NULL,
  `Humidity_set` decimal(7,2) DEFAULT NULL,
  `Profile No.` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Profile Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Profile Cycles` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Active Cycles` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Total Loops` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Act Loops` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Segment` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Active Time` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Profile Time` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Total Time` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Segment Type` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Segment Total Time` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Segment Remain Time` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `Status` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;

-- Table structure for table `para_manager`
--

CREATE TABLE IF NOT EXISTS `para_manager` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `parameter` varchar(50) DEFAULT NULL,
  `on_messager` varchar(20) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=23 ;

--
-- Dumping data for table `para_manager`
--

INSERT INTO `para_manager` (`id`, `parameter`, `on_messager`, `value`) VALUES
(1, 'id', 'Yes', NULL),
(2, 'Time_request', 'Yes', NULL),
(3, 'Temperature', 'Yes', NULL),
(4, 'Temperature_set', 'Yes', NULL),
(5, 'Humidity', 'Yes', NULL),
(6, 'Humidity_set', 'Yes', NULL),
(7, 'Profile No.', 'No', NULL),
(8, 'Profile Name', 'No', NULL),
(9, 'Profile Cycles', 'No', NULL),
(10, 'Active Cycles', 'No', NULL),
(11, 'Total Loops', 'No', NULL),
(12, 'Act Loops', 'No', NULL),
(13, 'Segment', 'No', NULL),
(14, 'Active Time', 'No', NULL),
(15, 'Profile Time', 'No', NULL),
(16, 'Total Time', 'No', NULL),
(17, 'Segment Type', 'No', NULL),
(18, 'Segment Total Time', 'No', NULL),
(19, 'Segment Remain Time', 'No', NULL),
(20, 'Status', 'No', NULL),
(21, 'Time_cycle', 'No', '13'),
(22, 'Time_req', 'No', '0.2');

insert into climate(temperature, humidity) values(0,0);-- --------------------------------------------------------
