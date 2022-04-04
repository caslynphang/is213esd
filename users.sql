-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 04, 2022 at 05:32 AM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `users`
--

DROP DATABASE IF EXISTS users
CREATE DATABASE users

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
  user_id char(32) NOT NULL,
  first_name varchar(120) NOT NULL,
  last_name varchar(120) NOT NULL,
  email varchar(120) NOT NULL,
  password_hash varchar(120) NOT NULL,
  time_created datetime NOT NULL,
  last_updated datetime NOT NULL,
  PRIMARY KEY (user_id),
  UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
