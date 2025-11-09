-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 05, 2025 at 12:54 PM
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
-- Database: `tourism_guide`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `icon`, `created_at`) VALUES
(1, 'Tourist Spot', 'fa-camera', '2025-11-04 23:48:18'),
(2, 'Restaurant', 'fa-utensils', '2025-11-04 23:48:18'),
(3, 'Hotel', 'fa-bed', '2025-11-04 23:48:18'),
(4, 'Transport Terminal', 'fa-bus', '2025-11-04 23:48:18'),
(5, 'Landmark', 'fa-landmark', '2025-11-04 23:48:18'),
(6, 'Nature', 'fa-tree', '2025-11-04 23:48:18'),
(7, 'Shopping', 'fa-shopping-bag', '2025-11-04 23:48:18'),
(8, 'Entertainment', 'fa-film', '2025-11-04 23:48:18'),
(10, 'Comfort Room', 'fa-toilet', '2025-11-05 02:30:14'),
(11, 'Favorites', 'fa-heart', '2025-11-05 02:41:51'),
(12, 'Church', 'fa-church', '2025-11-05 06:07:10');

-- --------------------------------------------------------

--
-- Table structure for table `destinations`
--

CREATE TABLE `destinations` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `address` text DEFAULT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `contact_number` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `website` varchar(200) DEFAULT NULL,
  `opening_hours` varchar(100) DEFAULT NULL,
  `entry_fee` varchar(100) DEFAULT NULL,
  `rating` decimal(2,1) DEFAULT 0.0,
  `image_path` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `destinations`
--

INSERT INTO `destinations` (`id`, `name`, `category_id`, `description`, `address`, `latitude`, `longitude`, `contact_number`, `email`, `website`, `opening_hours`, `entry_fee`, `rating`, `image_path`, `is_active`, `created_at`, `updated_at`) VALUES
(8, 'Lake Danao Natural Park', 2, 'A guitar-shaped lake located in the highlands of Ormoc City. Perfect for nature lovers, kayaking, and picnics. The serene environment offers cool climate and stunning mountain views.', 'Barangay Lake Danao, Ormoc City, Leyte', 11.15420000, 124.78310000, '+63-053-255-2345', '', '', '6:00 AM - 6:00 PM', 'PHP 20', 5.0, 'destinations/690b3722b0ae4_1762342690.jpg', 1, '2025-11-05 05:50:01', '2025-11-05 11:38:10'),
(9, 'Tongonan Hot Spring National Park', 2, 'Natural hot springs with therapeutic mineral waters surrounded by lush forests. Features multiple pools with varying temperatures and scenic hiking trails.', 'Barangay Tongonan, Ormoc City, Leyte', 11.11670000, 124.78330000, '+63-053-255-3456', NULL, NULL, '7:00 AM - 5:00 PM', 'PHP 50', 5.0, NULL, 0, '2025-11-05 05:50:01', '2025-11-05 11:22:05'),
(10, 'Kasabangan Island', 2, 'A beautiful island with white sand beaches and crystal clear waters. Perfect for swimming, snorkeling, and beach camping. Accessible by boat from Ormoc port.', 'Kasabangan, Ormoc City, Leyte', 11.04030000, 124.56720000, '+63-917-123-4567', NULL, NULL, '24 Hours', 'PHP 100 (Boat Fee)', 5.0, NULL, 0, '2025-11-05 05:50:01', '2025-11-05 11:22:12'),
(11, 'Altos Peak', 2, 'The highest peak in Ormoc City offering breathtaking views of the city, nearby islands, and Leyte province. Popular hiking and trekking destination.', 'Barangay Lake Danao, Ormoc City, Leyte', 11.14890000, 124.78970000, '+63-917-234-5678', '', '', '24 Hours', 'Free', 5.0, 'destinations/690b139434c6e_1762333588.jpg', 1, '2025-11-05 05:50:01', '2025-11-05 09:06:28'),
(12, 'Sambawan Island Beach', 1, 'Pristine white sand beach with turquoise waters. Known for its stunning sandbar, coral reefs, and camping facilities. Great for island hopping.', 'Sambawan Island, Ormoc City, Leyte', 11.02110000, 124.52340000, '+63-917-345-6789', NULL, NULL, '24 Hours', 'PHP 150', 5.0, NULL, 0, '2025-11-05 05:50:01', '2025-11-05 11:37:18'),
(13, 'Mahagnao Volcano Natural Park', 5, 'Features twin crater lakes, hot springs, and diverse wildlife. A protected area with hiking trails through pristine forests and geothermal features.', 'Barangay Mahagnao, Ormoc City, Leyte', 11.14440000, 124.75560000, '+63-053-255-4567', NULL, NULL, '7:00 AM - 5:00 PM', 'PHP 30', 5.0, NULL, 0, '2025-11-05 05:59:34', '2025-11-05 11:22:09'),
(14, 'Luan-Luan Falls', 6, 'Hidden waterfall surrounded by lush forest. Features multiple cascading tiers and natural pools perfect for swimming. Requires short trek through nature trail.', 'Barangay Lake Danao, Ormoc City, Leyte', 11.15670000, 124.77450000, '+63-917-456-7890', NULL, NULL, '6:00 AM - 5:00 PM', 'PHP 20', 5.0, NULL, 0, '2025-11-05 05:59:34', '2025-11-05 11:35:32'),
(15, 'Bao Hot and Cold Spring', 6, 'Unique natural springs featuring both hot and cold water sources. Locals believe the waters have healing properties. Family-friendly destination.', 'Barangay Bao, Ormoc City, Leyte', 0.00000000, 124.62340000, '+63-917-567-8901', '', '', '6:00 AM - 6:00 PM', 'PHP 30', 5.0, 'destinations/690b31a926ada_1762341289.jpg', 1, '2025-11-05 05:59:34', '2025-11-05 11:17:14'),
(37, 'Ormoc City Plaza', 1, '...', '...', 11.00590000, 124.60750000, '+63-053-561-5200', 'ormoccity@gmail.com', '', '24 Hours', 'Free', 5.0, 'destinations/690b35ea7e743_1762342378.jpg', 1, '2025-11-05 06:04:26', '2025-11-05 11:32:58'),
(38, 'Our Lady of Fatima Shrine', 12, '...', '...', 11.02340000, 124.63120000, '+63-053-561-2345', '', '', '5:00 AM - 7:00 PM', 'Free', 5.0, NULL, 0, '2025-11-05 06:04:26', '2025-11-05 11:21:57'),
(39, 'Ormoc City Superdome', 1, '...', '...', 11.00890000, 124.60890000, '+63-053-561-6789', '', '', '8:00 AM - 10:00 PM', 'Varies', 5.0, 'destinations/690b36df53283_1762342623.jpg', 1, '2025-11-05 06:04:26', '2025-11-05 11:37:03'),
(40, 'Ormoc Veterans Park', 1, '...', '...', 11.00450000, 124.60670000, '+63-053-561-5200', '', '', '24 Hours', 'Free', 5.0, 'destinations/690b36af1cdbe_1762342575.jpg', 1, '2025-11-05 06:04:26', '2025-11-05 11:36:15'),
(41, 'Ormoc Bay Seafood Restaurant', 2, 'Famous for fresh seafood dishes and local Leyteño cuisine. Must-try: grilled fish, kinilaw, and traditional Filipino seafood specialties.', 'Rizal Avenue, Ormoc City, Leyte', 11.00670000, 124.60890000, '+63-053-561-7890', '', '', '10:00 AM - 10:00 PM', '', 5.0, NULL, 0, '2025-11-05 06:08:34', '2025-11-05 11:30:55'),
(42, 'Ormoc Public Market', 7, 'Bustling local market offering fresh produce, seafood, local delicacies, and handicrafts. Best place to experience local culture and food.', 'Bonifacio Street, Ormoc City, Leyte', 11.00780000, 124.60780000, '+63-053-561-8901', '', '', '5:00 AM - 6:00 PM', '', 5.0, 'destinations/690b358e4342f_1762342286.jpg', 1, '2025-11-05 06:08:34', '2025-11-05 11:31:26'),
(43, 'Café Antonio', 2, 'Cozy café serving local coffee, pastries, and light meals. Popular among locals for breakfast and afternoon snacks. Free Wi-Fi available.', 'Real Street, Ormoc City, Leyte', 11.00560000, 124.60710000, '+63-917-678-9012', '', '', '6:00 AM - 9:00 PM', '', 5.0, NULL, 0, '2025-11-05 06:08:34', '2025-11-05 11:31:42'),
(44, 'Don Felipe Hotel', 3, 'Premier hotel in Ormoc City offering comfortable rooms, restaurant, function halls, and excellent service. Convenient location near city center.', 'Bonifacio Street, Ormoc City, Leyte', 11.00710000, 124.60820000, '+63-053-561-9012', 'info@donfelipehotel.com', '', '', '', 5.0, 'destinations/690afeb1e236f_1762328241.webp', 1, '2025-11-05 06:08:54', '2025-11-05 08:51:03'),
(45, 'GV Hotel Ormoc', 3, 'Budget-friendly hotel with clean rooms, air conditioning, and basic amenities. Perfect for travelers looking for affordable accommodation.', 'Real Street, Ormoc City, Leyte', 11.00630000, 124.60730000, '+63-053-561-9123', 'gvormoc@gvhotels.com.ph', '', '', '', 5.0, 'destinations/690b00c3bb9e6_1762328771.jpg', 1, '2025-11-05 06:08:54', '2025-11-05 08:51:03'),
(46, 'Ormoc Villa Hotel', 3, 'Mid-range hotel with modern facilities, swimming pool, restaurant, and conference rooms. Family-friendly with spacious rooms.', 'Aviles Street, Ormoc City, Leyte', 11.00810000, 124.60910000, '+63-053-561-9234', 'reservations@ormocvillahotel.com', '', '', '', 5.0, 'destinations/690b35305c563_1762342192.jpg', 1, '2025-11-05 06:08:54', '2025-11-05 11:29:52'),
(47, 'Robinsons Place Ormoc', 7, 'Major shopping mall featuring department store, supermarket, cinema, restaurants, and retail shops. Air-conditioned and family-friendly.', 'Real Street, Ormoc City, Leyte', 11.02516804, 124.60520309, '+63-053-561-9345', '', '', '10:00 AM - 9:00 PM', '', 5.0, 'destinations/690b2c8c9acbc_1762339980.webp', 1, '2025-11-05 06:09:08', '2025-11-05 10:53:00'),
(49, 'Ormoc Pasalubong Center', 7, 'One-stop shop for local products and souvenirs. Features Ormoc delicacies, handicrafts, and regional specialties. Perfect for gifts.', 'Rizal Avenue, Ormoc City, Leyte', 11.00650000, 124.60770000, '+63-917-789-0123', '', '', '8:00 AM - 7:00 PM', '', 5.0, 'destinations/690b3135da062_1762341173.jpg', 1, '2025-11-05 06:09:08', '2025-11-05 11:12:53'),
(50, 'Ormoc City Terminal', 4, '', '', 11.00476371, 124.60709824, '', '', '', '', '', 5.0, 'destinations/690b30fc0b5e9_1762341116.jpg', 1, '2025-11-05 06:37:04', '2025-11-05 11:11:56');

-- --------------------------------------------------------

--
-- Table structure for table `destination_images`
--

CREATE TABLE `destination_images` (
  `id` int(11) NOT NULL,
  `destination_id` int(11) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `caption` varchar(200) DEFAULT NULL,
  `is_primary` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `destination_images`
--

INSERT INTO `destination_images` (`id`, `destination_id`, `image_path`, `caption`, `is_primary`, `created_at`) VALUES
(4, 44, 'destinations/690afeb1ea56d_1762328241.webp', '', 0, '2025-11-05 07:37:21'),
(5, 44, 'destinations/690afec9924f0_1762328265.webp', '', 0, '2025-11-05 07:37:45'),
(6, 45, 'destinations/690b00c3c4ab0_1762328771.jpg', '', 0, '2025-11-05 07:46:11'),
(8, 47, 'destinations/690b2806622aa_1762338822.jpg', '', 0, '2025-11-05 10:33:42'),
(9, 15, 'destinations/690b31a92f5f0_1762341289.jpg', '', 0, '2025-11-05 11:14:49'),
(10, 37, 'destinations/690b35ea8607b_1762342378.jpg', '', 0, '2025-11-05 11:32:58'),
(11, 37, 'destinations/690b35ff3e7c8_1762342399.jpg', '', 0, '2025-11-05 11:33:19'),
(12, 37, 'destinations/690b3610e81f3_1762342416.jpg', '', 0, '2025-11-05 11:33:36'),
(13, 8, 'destinations/690b3722b701d_1762342690.jpg', '', 0, '2025-11-05 11:38:10');

-- --------------------------------------------------------

--
-- Stand-in structure for view `destination_ratings`
-- (See below for the actual view)
--
CREATE TABLE `destination_ratings` (
`id` int(11)
,`name` varchar(200)
,`review_count` bigint(21)
,`average_rating` decimal(12,1)
,`five_star` decimal(22,0)
,`four_star` decimal(22,0)
,`three_star` decimal(22,0)
,`two_star` decimal(22,0)
,`one_star` decimal(22,0)
);

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL,
  `destination_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `rating` int(11) NOT NULL CHECK (`rating` >= 1 and `rating` <= 5),
  `comment` text DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`id`, `destination_id`, `user_id`, `user_name`, `rating`, `comment`, `is_approved`, `created_at`) VALUES
(11, 8, NULL, 'Maria Santos', 3, 'Lake Danao is absolutely breathtaking! Perfect for a peaceful getaway. The guitar shape is amazing from the viewpoint.', 1, '2024-10-15 02:30:00'),
(12, 11, 1, 'HinzoHana', 2, 'Wews', 1, '2025-11-05 08:43:11'),
(13, 15, 1, 'Sample', 5, 'Sample rate', 1, '2025-11-05 08:57:17'),
(14, 11, 1, 'Hello', 5, 'sample 2 ratings', 1, '2025-11-05 08:58:44'),
(15, 47, 1, 'Hans', 5, 'Suroyanan', 1, '2025-11-05 10:32:59');

-- --------------------------------------------------------

--
-- Table structure for table `routes`
--

CREATE TABLE `routes` (
  `id` int(11) NOT NULL,
  `route_name` varchar(200) DEFAULT NULL,
  `origin_id` int(11) DEFAULT NULL,
  `destination_id` int(11) DEFAULT NULL,
  `transport_mode` enum('jeepney','taxi','bus','van','tricycle','walking') NOT NULL,
  `distance_km` decimal(6,2) DEFAULT NULL,
  `estimated_time_minutes` int(11) DEFAULT NULL,
  `base_fare` decimal(8,2) DEFAULT NULL,
  `fare_per_km` decimal(8,2) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `routes`
--

INSERT INTO `routes` (`id`, `route_name`, `origin_id`, `destination_id`, `transport_mode`, `distance_km`, `estimated_time_minutes`, `base_fare`, `fare_per_km`, `description`, `is_active`, `created_at`) VALUES
(26, 'Ormoc City Terminal to Lake Danao Natural Park', 50, 8, 'jeepney', 0.00, 0, 30.00, 0.00, '0', 1, '2025-11-05 06:19:01'),
(27, 'Ormoc City Plaza to Tongonan Hot Spring', 37, 9, 'jeepney', 0.00, 0, 30.00, 0.00, '0', 1, '2025-11-05 06:19:01'),
(28, 'Ormoc Port (near Plaza) to Kasabangan Island', 37, 10, '', 8.50, 30, 100.00, 0.00, 'Boat ride from Ormoc port. Schedule subject to weather conditions.', 1, '2025-11-05 06:19:01'),
(29, 'Ormoc City Plaza to Altos Peak', 37, 11, 'tricycle', 19.00, 60, 40.00, 0.00, '0', 1, '2025-11-05 06:19:01'),
(30, 'Ormoc Port to Sambawan Island Beach', 37, 12, '', 12.30, 45, 150.00, 0.00, 'Island hopping boat tour. Registration required at tourism office.', 1, '2025-11-05 06:19:01'),
(31, 'Lake Danao Natural Park to Tongonan Hot Spring National Park', 8, 9, 'tricycle', 8.70, 25, 30.00, 5.00, 'Short route connecting two natural attractions. Tricycle or motorcycle available.', 1, '2025-11-05 06:19:01'),
(32, 'Lake Danao Natural Park to Altos Peak', 8, 11, 'walking', 2.10, 90, 0.00, 0.00, 'Hiking trail from Lake Danao Park. Guided trek recommended for safety.', 1, '2025-11-05 06:19:01'),
(33, 'Tongonan Hot Spring to Mahagnao Volcano Natural Park', 9, 13, 'van', 6.40, 20, 25.00, 4.00, 'Connecting route between geothermal areas. Van or private vehicle.', 1, '2025-11-05 06:19:01');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `role`, `created_at`) VALUES
(1, 'Admin', '$2y$10$rurfn/OYFQUWIfpyzXxOjOmErlcq/Mw0yVEGD8cTsMAHwpI/yXQGa', 'admin@gmail.com', 'admin', '2025-11-05 00:41:27'),
(2, 'Hans', '$2y$10$/ADtH0gaUpSr8ox4ihu2vOcwwsZWwLg8I5vNh6JJmlJSGzgTpd7x6', 'hansmichael.2005.gabor@gmail.com', 'user', '2025-11-05 00:31:38');

-- --------------------------------------------------------

--
-- Table structure for table `website_feedback`
--

CREATE TABLE `website_feedback` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `rating` int(11) NOT NULL CHECK (`rating` >= 1 and `rating` <= 5),
  `category` enum('usability','features','content','design','general') DEFAULT 'general',
  `feedback` text NOT NULL,
  `is_public` tinyint(1) DEFAULT 1,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `website_feedback`
--

INSERT INTO `website_feedback` (`id`, `user_id`, `user_name`, `email`, `rating`, `category`, `feedback`, `is_public`, `is_read`, `created_at`) VALUES
(2, 1, 'Admin', 'ad@gmail.com', 2, 'features', 'damn', 1, 0, '2025-11-05 08:10:13'),
(3, 1, 'Admin', 'ad@gmail.com', 3, 'features', 'again', 1, 1, '2025-11-05 08:10:31');

-- --------------------------------------------------------

--
-- Structure for view `destination_ratings`
--
DROP TABLE IF EXISTS `destination_ratings`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `destination_ratings`  AS SELECT `d`.`id` AS `id`, `d`.`name` AS `name`, count(`r`.`id`) AS `review_count`, round(avg(`r`.`rating`),1) AS `average_rating`, sum(case when `r`.`rating` = 5 then 1 else 0 end) AS `five_star`, sum(case when `r`.`rating` = 4 then 1 else 0 end) AS `four_star`, sum(case when `r`.`rating` = 3 then 1 else 0 end) AS `three_star`, sum(case when `r`.`rating` = 2 then 1 else 0 end) AS `two_star`, sum(case when `r`.`rating` = 1 then 1 else 0 end) AS `one_star` FROM (`destinations` `d` left join `reviews` `r` on(`d`.`id` = `r`.`destination_id` and `r`.`is_approved` = 1)) GROUP BY `d`.`id`, `d`.`name` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `destinations`
--
ALTER TABLE `destinations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `destination_images`
--
ALTER TABLE `destination_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `destination_id` (`destination_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_reviews_destination` (`destination_id`),
  ADD KEY `idx_reviews_rating` (`rating`);

--
-- Indexes for table `routes`
--
ALTER TABLE `routes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `origin_id` (`origin_id`),
  ADD KEY `destination_id` (`destination_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `website_feedback`
--
ALTER TABLE `website_feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_feedback_rating` (`rating`),
  ADD KEY `idx_feedback_created` (`created_at`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `destinations`
--
ALTER TABLE `destinations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `destination_images`
--
ALTER TABLE `destination_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `routes`
--
ALTER TABLE `routes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `website_feedback`
--
ALTER TABLE `website_feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `destinations`
--
ALTER TABLE `destinations`
  ADD CONSTRAINT `destinations_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `destination_images`
--
ALTER TABLE `destination_images`
  ADD CONSTRAINT `destination_images_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `routes`
--
ALTER TABLE `routes`
  ADD CONSTRAINT `routes_ibfk_1` FOREIGN KEY (`origin_id`) REFERENCES `destinations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `routes_ibfk_2` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `website_feedback`
--
ALTER TABLE `website_feedback`
  ADD CONSTRAINT `website_feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
