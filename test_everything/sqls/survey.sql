CREATE DATABASE IF NOT EXISTS `survey_record` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `survey_record`;
-- --------------------------------------------------------

--
-- Table structure for table `survey_record`
--

DROP TABLE IF EXISTS `survey_record`;
CREATE TABLE IF NOT EXISTS `survey_record` (
    username VARCHAR(60) PRIMARY KEY,
    pref_location VARCHAR(60),
    pref_cuisine VARCHAR(60),
    pref_price INTEGER
);

INSERT INTO survey_record (username, pref_location, pref_cuisine,pref_price)
VALUES
    ('user1', "south", "Western",2),
    ('user2', "south", "Japanese",2);