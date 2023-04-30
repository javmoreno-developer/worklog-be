CREATE TABLE `user` (
  `idUse` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `surname` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `pass` VARCHAR(255) NOT NULL,
  `picture` VARCHAR(255) NOT NULL,
  `linkedin` VARCHAR(255) NOT NULL,
  `github` VARCHAR(255) NOT NULL,
  `twitter` VARCHAR(255) NOT NULL,
  `profile` ENUM ('1', '2', '3', '4') NOT NULL
);

CREATE TABLE `unit` (
  `idUni` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `level` TINYINT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `initials` VARCHAR(10) NOT NULL,
  `character` CHAR(1) DEFAULT NULL,
  `unit_type` ENUM ('morning', 'evening')
);

CREATE TABLE `module` (
  `idMod` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `initials` VARCHAR(50) NOT NULL,
  `hours` INT DEFAULT NULL,
  `idUni` INT NOT NULL
);

CREATE TABLE `company` (
  `idComp` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `direction` VARCHAR(255) NOT NULL,
  `latitude` DECIMAL(9,6) NOT NULL,
  `longitude` DECIMAL(9,6) NOT NULL,
  `phone` VARCHAR(50) NOT NULL
);

CREATE TABLE `user_has_unit` (
  `idUse` INT NOT NULL,
  `idUni` INT NOT NULL,
  PRIMARY KEY (`idUse`, `idUni`)
);

CREATE TABLE `agreement` (
  `idAgr` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `created_at` TIMESTAMP NOT NULL,
  `start_at` TIMESTAMP NOT NULL,
  `end_at` TIMESTAMP NOT NULL,
  `agreement_type` ENUM ('fct', 'dual', 'fct+dual') NOT NULL,
  `idComp` INT NOT NULL,
  `idUse` INT NOT NULL,
  `laboralidUse` INT NOT NULL,
  `alumnoidUse` INT NOT NULL
);

CREATE TABLE `entry` (
  `idEnt` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `date` TIMESTAMP NOT NULL,
  `idAgr` INT NOT NULL
);

CREATE TABLE `day` (
  `idDay` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(255) NOT NULL,
  `hours` TIME NOT NULL,
  `observations` VARCHAR(255) DEFAULT NULL,
  `idEnt` INT NOT NULL
);


CREATE UNIQUE INDEX `user_index_0` ON `user` (`email`);

ALTER TABLE `module` ADD FOREIGN KEY (`idUni`) REFERENCES `unit` (`idUni`);

ALTER TABLE `user_has_unit` ADD FOREIGN KEY (`idUse`) REFERENCES `user` (`idUse`);

ALTER TABLE `user_has_unit` ADD FOREIGN KEY (`idUni`) REFERENCES `unit` (`idUni`);

ALTER TABLE `agreement` ADD FOREIGN KEY (`idComp`) REFERENCES `company` (`idComp`);

ALTER TABLE `agreement` ADD FOREIGN KEY (`idUse`) REFERENCES `user` (`idUse`);

ALTER TABLE `agreement` ADD FOREIGN KEY (`laboralidUse`) REFERENCES `user` (`idUse`);

ALTER TABLE `agreement` ADD FOREIGN KEY (`alumnoidUse`) REFERENCES `user` (`idUse`);

ALTER TABLE `entry` ADD FOREIGN KEY (`idAgr`) REFERENCES `agreement` (`idAgr`);

ALTER TABLE `day` ADD FOREIGN KEY (`idEnt`) REFERENCES `entry` (`idEnt`);
