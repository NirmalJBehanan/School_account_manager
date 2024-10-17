-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 15, 2024 at 03:27 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `school`
--

-- --------------------------------------------------------

--
-- Table structure for table `academic_year`
--

CREATE TABLE `academic_year` (
  `ay_id` int(11) NOT NULL,
  `academic_year` varchar(15) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `academic_year`
--

INSERT INTO `academic_year` (`ay_id`, `academic_year`, `status`) VALUES
(1, '2023-2024', 1);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add academic_year', 7, 'add_academic_year'),
(26, 'Can change academic_year', 7, 'change_academic_year'),
(27, 'Can delete academic_year', 7, 'delete_academic_year'),
(28, 'Can view academic_year', 7, 'view_academic_year'),
(29, 'Can add designation', 8, 'add_designation'),
(30, 'Can change designation', 8, 'change_designation'),
(31, 'Can delete designation', 8, 'delete_designation'),
(32, 'Can view designation', 8, 'view_designation'),
(33, 'Can add educational_level', 9, 'add_educational_level'),
(34, 'Can change educational_level', 9, 'change_educational_level'),
(35, 'Can delete educational_level', 9, 'delete_educational_level'),
(36, 'Can view educational_level', 9, 'view_educational_level'),
(37, 'Can add leave_type', 10, 'add_leave_type'),
(38, 'Can change leave_type', 10, 'change_leave_type'),
(39, 'Can delete leave_type', 10, 'delete_leave_type'),
(40, 'Can view leave_type', 10, 'view_leave_type'),
(41, 'Can add login', 11, 'add_login'),
(42, 'Can change login', 11, 'change_login'),
(43, 'Can delete login', 11, 'delete_login'),
(44, 'Can view login', 11, 'view_login'),
(45, 'Can add salary_table', 12, 'add_salary_table'),
(46, 'Can change salary_table', 12, 'change_salary_table'),
(47, 'Can delete salary_table', 12, 'delete_salary_table'),
(48, 'Can view salary_table', 12, 'view_salary_table'),
(49, 'Can add school_finance', 13, 'add_school_finance'),
(50, 'Can change school_finance', 13, 'change_school_finance'),
(51, 'Can delete school_finance', 13, 'delete_school_finance'),
(52, 'Can view school_finance', 13, 'view_school_finance'),
(53, 'Can add standard', 14, 'add_standard'),
(54, 'Can change standard', 14, 'change_standard'),
(55, 'Can delete standard', 14, 'delete_standard'),
(56, 'Can view standard', 14, 'view_standard'),
(57, 'Can add student_fee', 15, 'add_student_fee'),
(58, 'Can change student_fee', 15, 'change_student_fee'),
(59, 'Can delete student_fee', 15, 'delete_student_fee'),
(60, 'Can view student_fee', 15, 'view_student_fee'),
(61, 'Can add student_register', 16, 'add_student_register'),
(62, 'Can change student_register', 16, 'change_student_register'),
(63, 'Can delete student_register', 16, 'delete_student_register'),
(64, 'Can view student_register', 16, 'view_student_register'),
(65, 'Can add student_fee_transaction', 17, 'add_student_fee_transaction'),
(66, 'Can change student_fee_transaction', 17, 'change_student_fee_transaction'),
(67, 'Can delete student_fee_transaction', 17, 'delete_student_fee_transaction'),
(68, 'Can view student_fee_transaction', 17, 'view_student_fee_transaction'),
(69, 'Can add staff_register', 18, 'add_staff_register'),
(70, 'Can change staff_register', 18, 'change_staff_register'),
(71, 'Can delete staff_register', 18, 'delete_staff_register'),
(72, 'Can view staff_register', 18, 'view_staff_register'),
(73, 'Can add staff_leave', 19, 'add_staff_leave'),
(74, 'Can change staff_leave', 19, 'change_staff_leave'),
(75, 'Can delete staff_leave', 19, 'delete_staff_leave'),
(76, 'Can view staff_leave', 19, 'view_staff_leave'),
(77, 'Can add school_finance_transaction', 20, 'add_school_finance_transaction'),
(78, 'Can change school_finance_transaction', 20, 'change_school_finance_transaction'),
(79, 'Can delete school_finance_transaction', 20, 'delete_school_finance_transaction'),
(80, 'Can view school_finance_transaction', 20, 'view_school_finance_transaction'),
(81, 'Can add salary_transaction', 21, 'add_salary_transaction'),
(82, 'Can change salary_transaction', 21, 'change_salary_transaction'),
(83, 'Can delete salary_transaction', 21, 'delete_salary_transaction'),
(84, 'Can view salary_transaction', 21, 'view_salary_transaction');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `designation`
--

CREATE TABLE `designation` (
  `d_id` int(11) NOT NULL,
  `designation_name` varchar(40) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `designation`
--

INSERT INTO `designation` (`d_id`, `designation_name`, `status`) VALUES
(1, 'Account head', 1),
(2, 'office staff', 1),
(3, 'Faculty LP', 1),
(4, 'Faculty UP', 1),
(5, 'Faculty High school', 1),
(6, 'Faculty Higher secondary', 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'schoolapp', 'academic_year'),
(8, 'schoolapp', 'designation'),
(9, 'schoolapp', 'educational_level'),
(10, 'schoolapp', 'leave_type'),
(11, 'schoolapp', 'login'),
(12, 'schoolapp', 'salary_table'),
(21, 'schoolapp', 'salary_transaction'),
(13, 'schoolapp', 'school_finance'),
(20, 'schoolapp', 'school_finance_transaction'),
(19, 'schoolapp', 'staff_leave'),
(18, 'schoolapp', 'staff_register'),
(14, 'schoolapp', 'standard'),
(15, 'schoolapp', 'student_fee'),
(17, 'schoolapp', 'student_fee_transaction'),
(16, 'schoolapp', 'student_register'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-10-14 16:58:01.573649'),
(2, 'auth', '0001_initial', '2024-10-14 16:58:14.468049'),
(3, 'admin', '0001_initial', '2024-10-14 16:58:16.881480'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-10-14 16:58:16.945642'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-10-14 16:58:17.003795'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-10-14 16:58:18.243273'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-10-14 16:58:19.313123'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-10-14 16:58:19.473550'),
(9, 'auth', '0004_alter_user_username_opts', '2024-10-14 16:58:19.534714'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-10-14 16:58:20.124314'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-10-14 16:58:20.184445'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-10-14 16:58:20.299747'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-10-14 16:58:20.473248'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-10-14 16:58:20.613584'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-10-14 16:58:21.014645'),
(16, 'auth', '0011_update_proxy_permissions', '2024-10-14 16:58:21.074809'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-10-14 16:58:21.598196'),
(18, 'schoolapp', '0001_initial', '2024-10-14 16:58:51.781761'),
(19, 'sessions', '0001_initial', '2024-10-14 16:58:52.782379');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('ejet822edy6bwf0w3796v1q3vbcf56bv', 'eyJsb2dpbl9pZCI6MSwibWFzdGVyIjoxfQ:1t0WHJ:ywp4Ip-dUdAeEnKxTVfKOP_tdyA5PG3225Ofc4U0wlA', '2024-10-29 01:23:13.675123');

-- --------------------------------------------------------

--
-- Table structure for table `educational_level`
--

CREATE TABLE `educational_level` (
  `el_id` int(11) NOT NULL,
  `level` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `educational_level`
--

INSERT INTO `educational_level` (`el_id`, `level`) VALUES
(1, 'LP'),
(2, 'UP'),
(3, 'High school'),
(4, 'Higher secondary');

-- --------------------------------------------------------

--
-- Table structure for table `leave_type`
--

CREATE TABLE `leave_type` (
  `lt_id` int(11) NOT NULL,
  `leave_type` varchar(60) NOT NULL,
  `days` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `leave_type`
--

INSERT INTO `leave_type` (`lt_id`, `leave_type`, `days`, `status`) VALUES
(1, 'Sick', 4, 1),
(2, 'Casual', 2, 1),
(3, 'Vacation', 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` longtext NOT NULL,
  `user_type` varchar(15) NOT NULL,
  `status` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`login_id`, `username`, `password`, `user_type`, `status`) VALUES
(1, 'admin', 'admin', 'admin', NULL),
(2, 'ram@gmail.com', 'LHbh67At', 'Account head', NULL),
(3, 'sam@gmail.com', 'EasWC8Mp', 'Office staff', NULL),
(4, 'ajith@gmail.com', 'D@huSdr6', 'Faculty', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `salary_table`
--

CREATE TABLE `salary_table` (
  `st_id` int(11) NOT NULL,
  `account_category` varchar(20) NOT NULL,
  `basic_pay` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `designation_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `salary_table`
--

INSERT INTO `salary_table` (`st_id`, `account_category`, `basic_pay`, `status`, `designation_id`) VALUES
(1, 'Expense', 30000, 1, 1),
(2, 'Expense', 25000, 1, 2),
(3, 'Expense', 30000, 1, 3),
(4, 'Expense', 35000, 1, 4),
(5, 'Expense', 40000, 1, 5),
(6, 'Expense', 45000, 1, 6);

-- --------------------------------------------------------

--
-- Table structure for table `salary_transaction`
--

CREATE TABLE `salary_transaction` (
  `st_id` int(11) NOT NULL,
  `bonus` double DEFAULT NULL,
  `deductions` double DEFAULT NULL,
  `arrear` double DEFAULT NULL,
  `advance` double DEFAULT NULL,
  `da` double DEFAULT NULL,
  `hra` double DEFAULT NULL,
  `ta` double DEFAULT NULL,
  `agp` double DEFAULT NULL,
  `basic_pay` double NOT NULL,
  `salary_date` date NOT NULL,
  `approval_status` varchar(20) DEFAULT NULL,
  `academic_year_id` int(11) DEFAULT NULL,
  `salary_table_id` int(11) DEFAULT NULL,
  `staff_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `school_finance`
--

CREATE TABLE `school_finance` (
  `sf_id` int(11) NOT NULL,
  `account_category` varchar(20) NOT NULL,
  `finance_type` varchar(40) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `school_finance`
--

INSERT INTO `school_finance` (`sf_id`, `account_category`, `finance_type`, `status`) VALUES
(1, 'Income', 'School maintanance', 1);

-- --------------------------------------------------------

--
-- Table structure for table `school_finance_transaction`
--

CREATE TABLE `school_finance_transaction` (
  `sft_id` int(11) NOT NULL,
  `description` longtext NOT NULL,
  `total_amount` double NOT NULL,
  `entry_date` date NOT NULL,
  `approval_status` varchar(20) DEFAULT NULL,
  `academic_year_id` int(11) DEFAULT NULL,
  `school_finance_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `staff_leave`
--

CREATE TABLE `staff_leave` (
  `sl_id` int(11) NOT NULL,
  `reason` longtext NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `no_of_days` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `leave_type_id` int(11) DEFAULT NULL,
  `staff_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `staff_register`
--

CREATE TABLE `staff_register` (
  `sr_id` int(11) NOT NULL,
  `name` varchar(80) DEFAULT NULL,
  `contact_number` bigint(20) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `image` longtext DEFAULT NULL,
  `designation_id` int(11) DEFAULT NULL,
  `login_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff_register`
--

INSERT INTO `staff_register` (`sr_id`, `name`, `contact_number`, `address`, `image`, `designation_id`, `login_id`) VALUES
(1, 'Ram', NULL, NULL, '/media/team-4.jpg', 2, 2),
(2, 'Sam', NULL, NULL, '/media/testimonial-3.jpg', 3, 3),
(3, 'Ajith', NULL, NULL, '/media/testimonial-2.jpg', 4, 4);

-- --------------------------------------------------------

--
-- Table structure for table `standard`
--

CREATE TABLE `standard` (
  `s_id` int(11) NOT NULL,
  `standard` int(11) NOT NULL,
  `educational_level_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `standard`
--

INSERT INTO `standard` (`s_id`, `standard`, `educational_level_id`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 1),
(5, 5, 2),
(6, 6, 2),
(7, 7, 2),
(8, 8, 3),
(9, 9, 3),
(10, 10, 3),
(11, 11, 4),
(12, 12, 4);

-- --------------------------------------------------------

--
-- Table structure for table `student_fee`
--

CREATE TABLE `student_fee` (
  `sf_id` int(11) NOT NULL,
  `account_category` varchar(20) NOT NULL,
  `fee_type` varchar(150) NOT NULL,
  `amount` double NOT NULL,
  `status` tinyint(1) NOT NULL,
  `educational_level_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_fee`
--

INSERT INTO `student_fee` (`sf_id`, `account_category`, `fee_type`, `amount`, `status`, `educational_level_id`) VALUES
(1, 'Income', 'Tusion fee', 1000, 1, 1),
(2, 'Income', 'Tusion fee', 1200, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `student_fee_transaction`
--

CREATE TABLE `student_fee_transaction` (
  `sft_id` int(11) NOT NULL,
  `total_amount` double NOT NULL,
  `payment_date` date NOT NULL,
  `academic_year_id` int(11) DEFAULT NULL,
  `student_id` int(11) NOT NULL,
  `student_fee_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `student_register`
--

CREATE TABLE `student_register` (
  `sr_id` int(11) NOT NULL,
  `name` varchar(80) DEFAULT NULL,
  `email` varchar(40) NOT NULL,
  `contact_number` bigint(20) NOT NULL,
  `address` longtext NOT NULL,
  `image` longtext NOT NULL,
  `gender` varchar(10) NOT NULL,
  `login_id` int(11) NOT NULL,
  `standard_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academic_year`
--
ALTER TABLE `academic_year`
  ADD PRIMARY KEY (`ay_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `designation`
--
ALTER TABLE `designation`
  ADD PRIMARY KEY (`d_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `educational_level`
--
ALTER TABLE `educational_level`
  ADD PRIMARY KEY (`el_id`);

--
-- Indexes for table `leave_type`
--
ALTER TABLE `leave_type`
  ADD PRIMARY KEY (`lt_id`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`login_id`);

--
-- Indexes for table `salary_table`
--
ALTER TABLE `salary_table`
  ADD PRIMARY KEY (`st_id`),
  ADD KEY `Salary_table_designation_id_ea71ddcc_fk_Designation_d_id` (`designation_id`);

--
-- Indexes for table `salary_transaction`
--
ALTER TABLE `salary_transaction`
  ADD PRIMARY KEY (`st_id`),
  ADD KEY `Salary_transaction_academic_year_id_9d72e39f_fk_Academic_` (`academic_year_id`),
  ADD KEY `Salary_transaction_salary_table_id_aa029d26_fk_Salary_ta` (`salary_table_id`),
  ADD KEY `Salary_transaction_staff_id_83842894_fk_Staff_register_sr_id` (`staff_id`);

--
-- Indexes for table `school_finance`
--
ALTER TABLE `school_finance`
  ADD PRIMARY KEY (`sf_id`);

--
-- Indexes for table `school_finance_transaction`
--
ALTER TABLE `school_finance_transaction`
  ADD PRIMARY KEY (`sft_id`),
  ADD KEY `School_finance_trans_academic_year_id_a72f6aa0_fk_Academic_` (`academic_year_id`),
  ADD KEY `School_finance_trans_school_finance_id_f4a9add5_fk_School_fi` (`school_finance_id`);

--
-- Indexes for table `staff_leave`
--
ALTER TABLE `staff_leave`
  ADD PRIMARY KEY (`sl_id`),
  ADD KEY `Staff_leave_leave_type_id_8149ef8b_fk_Leave_type_lt_id` (`leave_type_id`),
  ADD KEY `Staff_leave_staff_id_781ddaf8_fk_Staff_register_sr_id` (`staff_id`);

--
-- Indexes for table `staff_register`
--
ALTER TABLE `staff_register`
  ADD PRIMARY KEY (`sr_id`),
  ADD KEY `Staff_register_designation_id_3d551c4b_fk_Designation_d_id` (`designation_id`),
  ADD KEY `Staff_register_login_id_4d9879f7_fk_Login_login_id` (`login_id`);

--
-- Indexes for table `standard`
--
ALTER TABLE `standard`
  ADD PRIMARY KEY (`s_id`),
  ADD KEY `Standard_educational_level_id_b839b621_fk_Education` (`educational_level_id`);

--
-- Indexes for table `student_fee`
--
ALTER TABLE `student_fee`
  ADD PRIMARY KEY (`sf_id`),
  ADD KEY `Student_fee_educational_level_id_ad4516d9_fk_Education` (`educational_level_id`);

--
-- Indexes for table `student_fee_transaction`
--
ALTER TABLE `student_fee_transaction`
  ADD PRIMARY KEY (`sft_id`),
  ADD KEY `Student_fee_transact_academic_year_id_f1318ded_fk_Academic_` (`academic_year_id`),
  ADD KEY `Student_fee_transact_student_id_124803d0_fk_Student_r` (`student_id`),
  ADD KEY `Student_fee_transact_student_fee_id_92b9a862_fk_Student_f` (`student_fee_id`);

--
-- Indexes for table `student_register`
--
ALTER TABLE `student_register`
  ADD PRIMARY KEY (`sr_id`),
  ADD KEY `Student_register_login_id_9437b190_fk_Login_login_id` (`login_id`),
  ADD KEY `Student_register_standard_id_8941b1f7_fk_Standard_s_id` (`standard_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `academic_year`
--
ALTER TABLE `academic_year`
  MODIFY `ay_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `designation`
--
ALTER TABLE `designation`
  MODIFY `d_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `educational_level`
--
ALTER TABLE `educational_level`
  MODIFY `el_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `leave_type`
--
ALTER TABLE `leave_type`
  MODIFY `lt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `login_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `salary_table`
--
ALTER TABLE `salary_table`
  MODIFY `st_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `salary_transaction`
--
ALTER TABLE `salary_transaction`
  MODIFY `st_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `school_finance`
--
ALTER TABLE `school_finance`
  MODIFY `sf_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `school_finance_transaction`
--
ALTER TABLE `school_finance_transaction`
  MODIFY `sft_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `staff_leave`
--
ALTER TABLE `staff_leave`
  MODIFY `sl_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `staff_register`
--
ALTER TABLE `staff_register`
  MODIFY `sr_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `standard`
--
ALTER TABLE `standard`
  MODIFY `s_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `student_fee`
--
ALTER TABLE `student_fee`
  MODIFY `sf_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `student_fee_transaction`
--
ALTER TABLE `student_fee_transaction`
  MODIFY `sft_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `student_register`
--
ALTER TABLE `student_register`
  MODIFY `sr_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `salary_table`
--
ALTER TABLE `salary_table`
  ADD CONSTRAINT `Salary_table_designation_id_ea71ddcc_fk_Designation_d_id` FOREIGN KEY (`designation_id`) REFERENCES `designation` (`d_id`);

--
-- Constraints for table `salary_transaction`
--
ALTER TABLE `salary_transaction`
  ADD CONSTRAINT `Salary_transaction_academic_year_id_9d72e39f_fk_Academic_` FOREIGN KEY (`academic_year_id`) REFERENCES `academic_year` (`ay_id`),
  ADD CONSTRAINT `Salary_transaction_salary_table_id_aa029d26_fk_Salary_ta` FOREIGN KEY (`salary_table_id`) REFERENCES `salary_table` (`st_id`),
  ADD CONSTRAINT `Salary_transaction_staff_id_83842894_fk_Staff_register_sr_id` FOREIGN KEY (`staff_id`) REFERENCES `staff_register` (`sr_id`);

--
-- Constraints for table `school_finance_transaction`
--
ALTER TABLE `school_finance_transaction`
  ADD CONSTRAINT `School_finance_trans_academic_year_id_a72f6aa0_fk_Academic_` FOREIGN KEY (`academic_year_id`) REFERENCES `academic_year` (`ay_id`),
  ADD CONSTRAINT `School_finance_trans_school_finance_id_f4a9add5_fk_School_fi` FOREIGN KEY (`school_finance_id`) REFERENCES `school_finance` (`sf_id`);

--
-- Constraints for table `staff_leave`
--
ALTER TABLE `staff_leave`
  ADD CONSTRAINT `Staff_leave_leave_type_id_8149ef8b_fk_Leave_type_lt_id` FOREIGN KEY (`leave_type_id`) REFERENCES `leave_type` (`lt_id`),
  ADD CONSTRAINT `Staff_leave_staff_id_781ddaf8_fk_Staff_register_sr_id` FOREIGN KEY (`staff_id`) REFERENCES `staff_register` (`sr_id`);

--
-- Constraints for table `staff_register`
--
ALTER TABLE `staff_register`
  ADD CONSTRAINT `Staff_register_designation_id_3d551c4b_fk_Designation_d_id` FOREIGN KEY (`designation_id`) REFERENCES `designation` (`d_id`),
  ADD CONSTRAINT `Staff_register_login_id_4d9879f7_fk_Login_login_id` FOREIGN KEY (`login_id`) REFERENCES `login` (`login_id`);

--
-- Constraints for table `standard`
--
ALTER TABLE `standard`
  ADD CONSTRAINT `Standard_educational_level_id_b839b621_fk_Education` FOREIGN KEY (`educational_level_id`) REFERENCES `educational_level` (`el_id`);

--
-- Constraints for table `student_fee`
--
ALTER TABLE `student_fee`
  ADD CONSTRAINT `Student_fee_educational_level_id_ad4516d9_fk_Education` FOREIGN KEY (`educational_level_id`) REFERENCES `educational_level` (`el_id`);

--
-- Constraints for table `student_fee_transaction`
--
ALTER TABLE `student_fee_transaction`
  ADD CONSTRAINT `Student_fee_transact_academic_year_id_f1318ded_fk_Academic_` FOREIGN KEY (`academic_year_id`) REFERENCES `academic_year` (`ay_id`),
  ADD CONSTRAINT `Student_fee_transact_student_fee_id_92b9a862_fk_Student_f` FOREIGN KEY (`student_fee_id`) REFERENCES `student_fee` (`sf_id`),
  ADD CONSTRAINT `Student_fee_transact_student_id_124803d0_fk_Student_r` FOREIGN KEY (`student_id`) REFERENCES `student_register` (`sr_id`);

--
-- Constraints for table `student_register`
--
ALTER TABLE `student_register`
  ADD CONSTRAINT `Student_register_login_id_9437b190_fk_Login_login_id` FOREIGN KEY (`login_id`) REFERENCES `login` (`login_id`),
  ADD CONSTRAINT `Student_register_standard_id_8941b1f7_fk_Standard_s_id` FOREIGN KEY (`standard_id`) REFERENCES `standard` (`s_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
