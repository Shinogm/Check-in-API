-- Active: 1715043174887@@127.0.0.1@3306@checkdb_gym
DROP DATABASE IF EXISTS checkdb_gym;

CREATE DATABASE checkdb_gym DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE checkdb_gym;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    perms ENUM('admin', 'client', 'none') DEFAULT 'noneS' NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email)
);

CREATE TABLE fingerprints (
    id INT NOT NULL AUTO_INCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    fingerprint LONGTEXT NOT NULL,
    tmp BLOB NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_fingerprint_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE memberships (
    id INT(6) NOT NULL AUTO_INCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    expiration_date DATE,
    have_membership ENUM('yes', 'no') DEFAULT 'no' NOT NULL,
    fingerprint_id INT,
    PRIMARY KEY (id),
    CONSTRAINT fk_membership_user FOREIGN KEY (user_id)REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_membership_fingerprint FOREIGN KEY (fingerprint_id) REFERENCES fingerprints (id) ON DELETE CASCADE
);

DELIMITER $$
CREATE TRIGGER generate_user_id
BEFORE INSERT ON memberships
FOR EACH ROW
BEGIN
    DECLARE new_id INT(6);
    SET new_id = FLOOR(RAND() * 900000) + 100000;
    WHILE EXISTS (SELECT * FROM memberships WHERE id = new_id) DO
        SET new_id = FLOOR(RAND() * 900000) + 100000;
    END WHILE;
    SET NEW.id = new_id;
END$$
DELIMITER ;

