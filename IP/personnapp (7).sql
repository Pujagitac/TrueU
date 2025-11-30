-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 30, 2025 at 09:23 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `personnapp`
--

-- --------------------------------------------------------

--
-- Table structure for table `contactform`
--

CREATE TABLE `contactform` (
  `submissionId` int(11) NOT NULL,
  `message` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contactform`
--

INSERT INTO `contactform` (`submissionId`, `message`) VALUES
(5, 'hello');

-- --------------------------------------------------------

--
-- Table structure for table `person`
--

CREATE TABLE `person` (
  `personId` int(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `fname` varchar(100) NOT NULL,
  `lname` varchar(60) DEFAULT NULL,
  `DOB` date NOT NULL,
  `profilePic` varchar(100) NOT NULL,
  `role` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `person`
--

INSERT INTO `person` (`personId`, `username`, `password`, `fname`, `lname`, `DOB`, `profilePic`, `role`) VALUES
(1, 'h', 'h', 'Babe', 'Meow', '2025-10-21', 'catto-2.webp', 1),
(2, 'j', 'j', 'jj', 'jj', '2015-11-01', 'catto-2.webp', 2),
(7, 'Tester', 'Tester', 'Tester', 'Test', '2025-11-01', '', 1);

-- --------------------------------------------------------

--
-- Table structure for table `person-mood`
--

CREATE TABLE `person-mood` (
  `entryID` int(100) NOT NULL,
  `personId` int(100) NOT NULL,
  `fname` varchar(100) NOT NULL,
  `moodName` varchar(100) NOT NULL,
  `entryDate` date NOT NULL,
  `diaryEntry` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `person-mood`
--

INSERT INTO `person-mood` (`entryID`, `personId`, `fname`, `moodName`, `entryDate`, `diaryEntry`) VALUES
(2, 1, 'Babe', 'Happy', '2025-11-01', 'Had a great morning walk.'),
(3, 1, 'Babe', 'Sad', '2025-11-02', 'Felt a bit low today.'),
(4, 1, 'Babe', 'Neutral', '2025-11-03', 'Normal day, nothing special.'),
(5, 1, 'Babe', 'Happy', '2025-11-04', 'Went out with friends, had fun.'),
(6, 1, 'Babe', 'Angry', '2025-11-05', 'Got frustrated at work.'),
(7, 1, 'Babe', 'Happy', '2025-11-06', 'Watched a movie I loved.'),
(8, 1, 'Babe', 'Neutral', '2025-11-07', 'Ordinary day, stayed home.'),
(9, 1, 'Babe', 'Sad', '2025-11-08', 'Missed someone I care about.'),
(10, 1, 'Babe', 'Happy', '2025-11-09', 'Received good news from a friend.'),
(11, 1, 'Babe', 'Angry', '2025-11-10', 'Traffic jam made me late.'),
(12, 1, 'Babe', 'Happy', '2025-11-11', 'Cooked a nice meal.'),
(13, 1, 'Babe', 'Neutral', '2025-11-12', 'Just a calm day.'),
(14, 1, 'Babe', 'Sad', '2025-11-13', 'Feeling under the weather.'),
(15, 1, 'Babe', 'Happy', '2025-11-14', 'Had a productive work session.'),
(16, 1, 'Babe', 'Happy', '2025-11-15', 'Went for a run in the park.'),
(17, 1, 'Babe', 'Neutral', '2025-11-16', 'Did some household chores.'),
(18, 1, 'Babe', 'Angry', '2025-11-17', 'Had a disagreement with a friend.'),
(19, 1, 'Babe', 'Happy', '2025-11-18', 'Enjoyed a nice cup of coffee.'),
(20, 1, 'Babe', 'Sad', '2025-11-19', 'Missed a deadline.'),
(21, 1, 'Babe', 'Happy', '2025-11-20', 'Watched the sunset.'),
(22, 1, 'Babe', 'Neutral', '2025-11-21', 'Routine day.'),
(23, 1, 'Babe', 'Happy', '2025-11-22', 'Had a fun conversation with a colleague.'),
(24, 1, 'Babe', 'Angry', '2025-11-23', 'Lost my keys today.'),
(25, 1, 'Babe', 'Happy', '2025-11-24', 'Tried a new recipe, it turned out great.'),
(26, 1, 'Babe', 'Neutral', '2025-11-25', 'Watched some TV shows.'),
(27, 1, 'Babe', 'Sad', '2025-11-26', 'Feeling a bit lonely.'),
(28, 1, 'Babe', 'Happy', '2025-11-27', 'Had a relaxing bath.'),
(29, 1, 'Babe', 'Happy', '2025-11-28', 'Finished a book I liked.'),
(30, 1, '', 'Neutral', '2025-11-19', 'Did some light cleaning and repair.'),
(31, 1, '', 'Happy', '2025-11-10', 'Ended the month on a positive note.'),
(32, 1, 'Babe', 'Happy', '2025-11-29', 'I made this page today'),
(33, 1, 'Babe', 'Happy', '2025-11-29', 'TESTING ENTRY'),
(34, 1, 'Babe', 'Happy', '2025-11-29', 'TESTING HAPPY COUNT was 16 - should be 17'),
(35, 1, 'Babe', 'Happy', '2025-11-29', 'TESTING 18'),
(36, 1, 'Babe', 'Happy', '2025-11-29', 'hi'),
(38, 1, 'Babe', 'Happy', '2025-11-29', 'hi'),
(41, 2, 'jj', 'Happy', '2025-11-30', 'My first entry'),
(42, 1, 'Babe', 'Happy', '2025-11-30', 'Project done!!');

-- --------------------------------------------------------

--
-- Table structure for table `prediction`
--

CREATE TABLE `prediction` (
  `predictionID` int(100) NOT NULL,
  `predictions` varchar(100) NOT NULL,
  `spirit` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prediction`
--

INSERT INTO `prediction` (`predictionID`, `predictions`, `spirit`) VALUES
(1, 'A joyful surprise awaits you.', 'Joy'),
(2, 'Be cautious in your choices today.', 'Caution'),
(5, 'You will make someone smile.', 'Smile'),
(6, 'A small challenge will teach you a lot.', 'Challenge');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contactform`
--
ALTER TABLE `contactform`
  ADD PRIMARY KEY (`submissionId`);

--
-- Indexes for table `person`
--
ALTER TABLE `person`
  ADD PRIMARY KEY (`personId`);

--
-- Indexes for table `person-mood`
--
ALTER TABLE `person-mood`
  ADD PRIMARY KEY (`entryID`);

--
-- Indexes for table `prediction`
--
ALTER TABLE `prediction`
  ADD PRIMARY KEY (`predictionID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contactform`
--
ALTER TABLE `contactform`
  MODIFY `submissionId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `person`
--
ALTER TABLE `person`
  MODIFY `personId` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `person-mood`
--
ALTER TABLE `person-mood`
  MODIFY `entryID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `prediction`
--
ALTER TABLE `prediction`
  MODIFY `predictionID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
