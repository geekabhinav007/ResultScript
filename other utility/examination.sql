-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 11, 2022 at 03:18 AM
-- Server version: 10.5.16-MariaDB-1:10.5.16+maria~focal
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `examination`
--

-- --------------------------------------------------------

--
-- Table structure for table `all_awards`
--

CREATE TABLE `all_awards` (
  `branch_code` int(2) DEFAULT NULL,
  `university_roll_no` int(7) DEFAULT NULL,
  `subject_code` varchar(8) DEFAULT NULL,
  `attendance_status` varchar(8) DEFAULT NULL,
  `obtained_marks` varchar(5) DEFAULT NULL,
  `max_marks` int(3) DEFAULT NULL,
  `Int_Ext` varchar(2) DEFAULT NULL,
  `umc_status` varchar(2) DEFAULT NULL,
  `branch` varchar(100) NOT NULL,
  `credit` varchar(10) NOT NULL,
  `mcode` varchar(10) NOT NULL,
  `student_name` varchar(100) NOT NULL,
  `father_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `branch_code`
--

CREATE TABLE `branch_code` (
  `branch_code` int(2) DEFAULT NULL,
  `branch_name` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `result`
--

CREATE TABLE `result` (
  `branch_name` varchar(100) NOT NULL,
  `urn` varchar(50) NOT NULL,
  `s_name / f_name` varchar(500) NOT NULL,
  `result` varchar(400) NOT NULL,
  `sgpa` varchar(10) NOT NULL,
  `credit_earn` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `schema_data`
--

CREATE TABLE `schema_data` (
  `branch_code` int(2) DEFAULT NULL,
  `subject_code` varchar(8) DEFAULT NULL,
  `m_code` int(5) DEFAULT NULL,
  `credit` int(1) DEFAULT NULL,
  `theory_practical` varchar(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `student_data`
--

CREATE TABLE `student_data` (
  `branch_code` int(2) DEFAULT NULL,
  `university_roll_no` int(7) DEFAULT NULL,
  `student_name` varchar(10) DEFAULT NULL,
  `father_name` varchar(15) DEFAULT NULL,
  `Result` varchar(77) DEFAULT NULL,
  `SGPA` varchar(10) DEFAULT NULL,
  `Credit earned` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
