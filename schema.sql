CREATE DATABASE IF NOT EXISTS divyadarshan_db;
USE divyadarshan_db;

-- Users Table for Authentication & Registration
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bookings Table for Darshan Reservations
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ref_no VARCHAR(50) UNIQUE NOT NULL,
    temple_name VARCHAR(150) NOT NULL,
    devotee_name VARCHAR(100) NOT NULL,
    aadhaar VARCHAR(50) NOT NULL,
    darshan_type VARCHAR(100) NOT NULL,
    slot VARCHAR(100) NOT NULL,
    breakdown VARCHAR(150) NOT NULL,
    total_amount INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
