CREATE DATABASE IF NOT EXISTS vnoiwebsite CHARACTER SET utf8;
GRANT ALL PRIVILEGES
    ON vnoiwebsite.*
    TO 'vnoi_admin'@'localhost' IDENTIFIED BY 'vnoi_password';