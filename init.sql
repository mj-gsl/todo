DROP DATABASE IF EXISTS todo_app;
CREATE DATABASE todo_app;
USE todo_app;

CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    status ENUM('open', 'in_progress', 'finished') NOT NULL DEFAULT 'open'
);
