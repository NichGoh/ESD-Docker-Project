-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Feb 25, 2024 at 10:38 AM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `user`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--
CREATE DATABASE IF NOT EXISTS `user`;
USE `user`;
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `Username` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL,
  `Email` varchar(255) COLLATE utf8mb3_bin NOT NULL,
  `Name` varchar(255) COLLATE utf8mb3_bin NOT NULL,
  `PasswordHash` varchar(255) COLLATE utf8mb3_bin NOT NULL,
  `PasswordSalt` varchar(255) COLLATE utf8mb3_bin NOT NULL,
  `UserType` enum('restaurant_owner','user') COLLATE utf8mb3_bin NOT NULL,
  `Token` varchar(1000) COLLATE utf8mb3_bin DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`Username`),
  UNIQUE KEY `Email` (`Email`),
  UNIQUE KEY `Username` (`Username`),
  UNIQUE KEY `Username_2` (`Username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`Username`, `Email`, `Name`, `PasswordHash`, `PasswordSalt`, `UserType`, `Token`, `createdAt`, `updatedAt`) VALUES
('user1', 'user@example.com', 'User One', '$2b$10$jbz1jvl2pivUFp7v7/JsnuXxlgio6DXLDqox4jsEYbs3xbIr6u/9C', '$2b$10$jbz1jvl2pivUFp7v7/Jsnu', 'user', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySUQiOiJ1c2VyMSIsIlVzZXJUeXBlIjoidXNlciIsIlVzZXJuYW1lIjoidXNlcjEiLCJFbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJOYW1lIjoiVXNlciBPbmUiLCJpYXQiOjE3MDg4NTY2MzUsImV4cCI6MTcwODk0MzAzNX0.xXXKKcxw5uqPIVMhVprtH1RwsoWv3iIZO5OCMJ', '2024-02-25 07:34:44', '2024-02-25 10:23:55'),
('resturant', 'resturant@gmail.com', 'restOwner', '$2b$10$ZMji.oSjUcJnBHbiYmDrQOFr5Fqi4gGUWhgjlHD6Qh1j0zknltbdy', '$2b$10$ZMji.oSjUcJnBHbiYmDrQO', 'restaurant_owner', NULL, '2024-02-25 10:37:35', '2024-02-25 10:37:35');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
