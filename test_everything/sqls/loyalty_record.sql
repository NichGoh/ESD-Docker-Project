CREATE DATABASE IF NOT EXISTS `loyalty_record` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `loyalty_record`;

-- --------------------------------------------------------

--
-- Table structure for table `loyalty_record`
--

DROP TABLE IF EXISTS `loyalty_record`;
CREATE TABLE IF NOT EXISTS `loyalty_record` (
    username VARCHAR(60) PRIMARY KEY,
    loyalty_points INTEGER
);

INSERT INTO loyalty_record (username, loyalty_points)
VALUES
    ('user1', 3),
    ('user2', 6),
    ('user3', 5);

-- --------------------------------------------------------

--
-- Table structure for table `books`
--
DROP TABLE IF EXISTS `voucher_codes`;
CREATE TABLE IF NOT EXISTS `voucher_codes` (
    voucher_code CHAR(10) PRIMARY KEY
);

INSERT INTO voucher_codes (voucher_code)
VALUES
    ('AAAAAAAAAA')

-- main things i changed:
-- table name from loyaltypoints to loyalty_record
-- the column user_id was changed to username so all the user_id previously were changed to username
-- loyalty_points is now integer instead of a string

