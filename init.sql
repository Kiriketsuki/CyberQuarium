-- GRANT ALL PRIVILEGES ON cyberquarium_db.* TO 'kiri'@'172.27.0.4' IDENTIFIED BY 'rootpassword';
-- FLUSH PRIVILEGES;
-- ALTER USER 'kiri'@'localhost' IDENTIFIED WITH mysql_native_password BY 'rootpassword';

ALTER TABLE Animal MODIFY COLUMN image_url VARCHAR(500);
SET @@global.sql_mode= '';