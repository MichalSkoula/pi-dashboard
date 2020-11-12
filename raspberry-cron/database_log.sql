-- Adminer 4.7.7 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `log`;
CREATE TABLE `log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inserted_at` datetime NOT NULL DEFAULT current_timestamp(),
  `indoor_temp` float NOT NULL DEFAULT 0,
  `indoor_pressure` float NOT NULL DEFAULT 0,
  `indoor_humidity` float NOT NULL DEFAULT 0,
  `indoor_moisture` float NOT NULL DEFAULT 0,
  `indoor_light` float NOT NULL DEFAULT 0,
  `outdoor_temp` float NOT NULL DEFAULT 0,
  `outdoor_pressure` float NOT NULL DEFAULT 0,
  `outdoor_humidity` float NOT NULL DEFAULT 0,
  `outdoor_rain` float NOT NULL DEFAULT 0,
  `cpu_temp` float NOT NULL DEFAULT 0,
  `cpu_load` float NOT NULL DEFAULT 0,
  `memory` float NOT NULL DEFAULT 0,
  `hdd` float NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- 2020-06-18 11:38:38
