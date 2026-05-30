CREATE DATABASE railway_db;

USE railway_db;

CREATE TABLE trains (
    train_no INT PRIMARY KEY,
    train_name VARCHAR(100),
    source_station VARCHAR(100),
    destination_station VARCHAR(100),
    seats_available INT,
    ticket_price INT
);

INSERT INTO trains VALUES
(101, 'Rajdhani Express', 'Delhi', 'Mumbai', 50, 1200),
(102, 'Shatabdi Express', 'Chennai', 'Bangalore', 40, 800),
(103, 'Duronto Express', 'Kolkata', 'Delhi', 60, 1500),
(104, 'Intercity Express', 'Kerala', 'Goa', 30, 900),
(105, 'Vande Bharat', 'Mumbai', 'Ahmedabad', 45, 2000);

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_name VARCHAR(100),
    train_no INT,
    seats_booked INT,
    total_price INT
);