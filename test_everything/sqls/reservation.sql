--
-- Database: reservation
--
CREATE DATABASE IF NOT EXISTS `reservation` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `reservation`;

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `reservation`;
CREATE TABLE IF NOT EXISTS `reservation` (
    user_username VARCHAR(60),
    restaurant_username VARCHAR(60),
    restaurant_name VARCHAR(60),
    reservation_date DATE NOT NULL,
    reservation_time TIME NOT NULL,
    num_of_pax INTEGER,
    special_requests VARCHAR(60),
    reservation_id INTEGER PRIMARY KEY
);

-- Insert sample data into the Reservation table
    INSERT INTO reservation (user_username, restaurant_username, restaurant_name, reservation_date, reservation_time, num_of_pax, special_requests, reservation_id)
    VALUES ('JohnDoe', 'WineConnection' ,'The Great Restaurant', '2024-04-01', '18:00:00', 4, 'Vegetarian option', 1),
        ('JaneSmith', 'WineConnection' , 'The Great Restaurant', '2024-04-02', '19:00:00', 2, 'No nuts', 2),
        ('AliceJohnson', 'WineConnection' , 'The Great Restaurant', '2024-04-03', '20:00:00', 6, 'Separate check', 3);