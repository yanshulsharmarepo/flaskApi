CREATE DATABASE Records;
use Records;
CREATE TABLE users(
  `id` int(10) UNSIGNED NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `city`varchar(255) DEFAULT NULL,
  `state`varchar(255) DEFAULT NULL,
  `zip`varchar(255) DEFAULT NULL,
  `web`varchar(255) DEFAULT NULL,
  `age` int(10) UNSIGNED NOT NULL
  );

ALTER TABLE `users` ADD PRIMARY KEY(`id`);
ALTER TABLE `users` CHANGE `id` `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT;



