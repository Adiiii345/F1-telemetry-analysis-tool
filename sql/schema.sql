CREATE DATABASE F1_DB;
USE F1_DB;
CREATE TABLE Sessions (
	Session_id INT AUTO_INCREMENT PRIMARY KEY,
    Year INT NOT NULL,
    Race_name VARCHAR(100),
    Circuit_name VARCHAR(100),
    Session_type VARCHAR(20),
    Race_date date
);
CREATE TABLE Drivers (
	Driver_id INT AUTO_INCREMENT PRIMARY KEY,
    Driver_Code VARCHAR(5) UNIQUE,
    Driver_name VARCHAR(100),
    Team VARCHAR(100)
);
CREATE TABLE Laps (
	Lap_id INT auto_increment PRIMARY KEY,
    Session_id INT,
    Driver_id INT,
    Lap_number INT,
    Lap_time_sec FLOAT,
    Sector1_time FLOAT,
    Sector2_time FLOAT,
    Sector3_time FLOAT,
    Tyre_Compound VARCHAR(20),
    Tyre_life INT,
    is_pit_out BOOLEAN,
    FOREIGN KEY (Session_id) REFERENCES Sessions(Session_id),
    FOREIGN KEY (Driver_id) REFERENCES Drivers(Driver_id) 
);
CREATE TABLE pitstops (
	pit_id INT AUTO_INCREMENT PRIMARY KEY,
    Session_id INT,
    Driver_id INT,
    Lap_number INT,
    Pit_duration FLOAT
);
CREATE TABLE weather (
  weather_id INT AUTO_INCREMENT PRIMARY KEY,
  session_id INT,
  time_elapsed FLOAT,
  air_temp FLOAT,
  track_temp FLOAT,
  rainfall BOOLEAN,
  wind_speed FLOAT
);