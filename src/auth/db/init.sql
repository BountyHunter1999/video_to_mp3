-- USER FOR OUR DB, to access mysql database
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123';

CREATE DATABASE auth;

-- Give the user created in line 1 access to this database
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

-- We will use the auth db to create a table(inside that db)
USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- This user will haave access to our auth service gateway api
INSERT INTO user (email, password) VALUES ('mikeyy@tokyo.com', 'Admin123');
