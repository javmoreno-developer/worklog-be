-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-04-2023 a las 17:15:03
-- Versión del servidor: 10.4.25-MariaDB
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `worklog`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `agreement`
--

CREATE TABLE `agreement` (
  `idAgreement` int(11) NOT NULL,
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `startAt` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `endAt` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `agreementType` enum('fct','dual','fct+dual') NOT NULL,
  `idCompany` int(11) NOT NULL,
  `idTeacher` int(11) NOT NULL,
  `idLabor` int(11) NOT NULL,
  `idAlumn` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `company`
--

CREATE TABLE `company` (
  `idCompany` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `direction` varchar(255) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  `phone` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `company`
--

INSERT INTO `company` (`idCompany`, `name`, `direction`, `latitude`, `longitude`, `phone`) VALUES
(1, 'Accenture', '', '0.000000', '0.000000', ''),
(2, 'ByEvolution', '', '0.000000', '0.000000', ''),
(3, 'Cathedral Software', '', '0.000000', '0.000000', ''),
(4, 'Viewnext', '', '0.000000', '0.000000', ''),
(5, 'Properly', '', '0.000000', '0.000000', ''),
(6, 'Rewe', '', '0.000000', '0.000000', ''),
(7, 'Rocketfy', '', '0.000000', '0.000000', ''),
(8, 'Solbyte', '', '0.000000', '0.000000', ''),
(9, 'Freepik', '', '0.000000', '0.000000', ''),
(10, 'Navicom', '', '0.000000', '0.000000', ''),
(11, 'Dekra', '', '0.000000', '0.000000', ''),
(12, 'Mayoral', '', '0.000000', '0.000000', ''),
(13, 'Rindus', '', '0.000000', '0.000000', ''),
(14, 'Safamotor', '', '0.000000', '0.000000', ''),
(15, 'Vicox', '', '0.000000', '0.000000', ''),
(16, 'Top Digital', '', '0.000000', '0.000000', ''),
(17, 'BIC Euronova', '', '0.000000', '0.000000', ''),
(18, 'Everis', '', '0.000000', '0.000000', ''),
(19, 'InComputer', '', '0.000000', '0.000000', ''),
(20, 'Dworkin', '', '0.000000', '0.000000', ''),
(21, 'SecureKids', '', '0.000000', '0.000000', ''),
(22, 'Click Help Point', '', '0.000000', '0.000000', ''),
(23, 'Institute of Physics of the Czech Academy of Sciences', '', '0.000000', '0.000000', ''),
(24, 'Enreach - Summa', '', '0.000000', '0.000000', ''),
(25, 'TraffGen Global', '', '0.000000', '0.000000', ''),
(26, 'NTT Data - Everis', '', '0.000000', '0.000000', ''),
(27, 'Verisk', '', '0.000000', '0.000000', ''),
(28, 'OP Plus', '', '0.000000', '0.000000', ''),
(29, 'Adivin Beach Flag', '', '0.000000', '0.000000', ''),
(30, 'Babel', '', '0.000000', '0.000000', ''),
(31, 'Hispasec', '', '0.000000', '0.000000', ''),
(32, 'EY', '', '0.000000', '0.000000', ''),
(33, 'ASAC', '', '0.000000', '0.000000', ''),
(34, 'Fantozzi Ufficio', '', '0.000000', '0.000000', ''),
(35, 'Wevoice', '', '0.000000', '0.000000', ''),
(36, 'Aliqindoi', '', '0.000000', '0.000000', ''),
(37, 'DHV Technology', '', '0.000000', '0.000000', ''),
(38, 'Cargestión', '', '0.000000', '0.000000', ''),
(39, 'Cooking & Publishing', '', '0.000000', '0.000000', ''),
(40, 'Under the Bed Games', '', '0.000000', '0.000000', ''),
(41, 'BIM Float', '', '0.000000', '0.000000', ''),
(42, 'Master Crowd Games', '', '0.000000', '0.000000', ''),
(43, 'The Game Kitchen', '', '0.000000', '0.000000', ''),
(44, 'Visitas Virtuales 360', '', '0.000000', '0.000000', ''),
(45, 'OVO', '', '0.000000', '0.000000', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `day`
--

CREATE TABLE `day` (
  `idDay` int(11) NOT NULL,
  `text` varchar(255) NOT NULL,
  `hours` time NOT NULL,
  `observations` varchar(255) DEFAULT NULL,
  `idEntry` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entry`
--

CREATE TABLE `entry` (
  `idEntry` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `idAgreement` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `module`
--

CREATE TABLE `module` (
  `idModule` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `initials` varchar(50) NOT NULL,
  `hours` int(11) DEFAULT NULL,
  `idUnit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `module`
--

INSERT INTO `module` (`idModule`, `name`, `initials`, `hours`, `idUnit`) VALUES
(1, 'Sistemas Informáticos', 'SINF', 6, 1),
(2, 'Programación', 'PROG', 8, 1),
(3, 'Lenguajes de Marcas y Sistemas de Gestión de la Información', 'LMSGI', 4, 1),
(4, 'Entornos de Desarrollo', 'ED', 3, 1),
(5, 'Bases de Datos', 'BDAT', 8, 1),
(7, 'Desarrollo Web en Entorno Servidor', 'DWES', 8, 2),
(8, 'Desarrollo Web en Entorno Cliente', 'DWEC', 8, 2),
(9, 'Diseño de Interfaces', 'DI', 7, 2),
(10, 'Despliegue de Aplicaciones Web', 'DAW', 3, 2),
(12, 'Sistemas Informáticos', 'SINF', 6, 3),
(13, 'Programación', 'PROG', 8, 3),
(14, 'Lenguajes de Marcas y Sistemas de Gestión de la Información', 'LMSGI', 4, 3),
(15, 'Entornos de Desarrollo', 'ED', 3, 3),
(16, 'Bases de Datos', 'BDAT', 8, 3),
(18, 'Acceso a Datos', 'ADAT', 5, 4),
(19, 'Programación Multimedia y de Dispositivos Móviles', 'PMDM', 4, 4),
(20, 'Programación de Servicios y Procesos', 'PSP', 3, 4),
(21, 'Desarrollo de Interfaces', 'DI', 7, 4),
(22, 'Sistemas de Gestión Empresarial', 'SGE', 4, 4),
(23, 'Hacking Ético', 'HE', NULL, 7),
(24, 'Incidentes de Ciberseguridad', 'ICS', NULL, 7),
(25, 'Bastionado de Redes y Sistemas', 'BRS', NULL, 7),
(26, 'Análisis Forense', 'AFOR', NULL, 7),
(27, 'Normativa de Ciberseguridad', 'NOR', NULL, 7),
(28, 'Puesta en Producción Segura', 'PPS', NULL, 7),
(29, 'Modelos de Inteligencia Artificial\r\n', 'MIA', 3, 8),
(30, 'Sistemas de Aprendizaje Automático', 'SAA', 3, 8),
(31, 'Programación de Inteligencia Artificial', 'PIA', 7, 8),
(32, 'Sistemas de Big Data', 'SBD', 3, 8),
(33, 'Bid Data Aplicado', 'BDA', 4, 8),
(34, 'Programación y Motores de Videojuegos', 'PMV', NULL, 9),
(35, 'Diseño Gráfico 2D y 3D', 'DG', NULL, 9),
(36, 'Programación en Red e Inteligencia Artificial', 'PRIA', NULL, 9),
(37, 'Realidad Virtual y Realidad Aumentada', 'RVRA', NULL, 9),
(38, 'Gestión, publicación y Producción', 'GPP', NULL, 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `unit`
--

CREATE TABLE `unit` (
  `idUnit` int(11) NOT NULL,
  `level` tinyint(4) NOT NULL,
  `name` varchar(255) NOT NULL,
  `initials` varchar(10) NOT NULL,
  `character` char(1) DEFAULT NULL,
  `unitType` enum('morning','evening') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `unit`
--

INSERT INTO `unit` (`idUnit`, `level`, `name`, `initials`, `character`, `unitType`) VALUES
(1, 1, 'Desarrollo de Aplicaciones Web', 'DAW', NULL, 'morning'),
(2, 2, 'Desarrollo de Aplicaciones Web', 'DAW', NULL, 'evening'),
(3, 1, 'Desarrollo de Aplicaciones Multiplataforma', 'DAM', NULL, 'morning'),
(4, 2, 'Desarrollo de Aplicaciones Multiplataforma', 'DAM', NULL, 'evening'),
(5, 1, 'Sistemas Microinformáticos y Redes', 'SMR', NULL, 'morning'),
(6, 2, 'Sistemas Microinformáticos y Redes', 'SMR', NULL, 'evening'),
(7, 1, 'Ciberseguridad en Entornos de las Tecnologías de la Información', 'CETI', NULL, 'morning'),
(8, 1, 'Inteligencia Artificial y Big Data', 'IABD', NULL, 'morning'),
(9, 1, 'Desarrollo de Videojuegos y Realidad Virtual', 'DVRV', NULL, 'morning');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `idUser` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `surname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `picture` varchar(255) NOT NULL,
  `linkedin` varchar(255) NOT NULL,
  `github` varchar(255) NOT NULL,
  `twitter` varchar(255) NOT NULL,
  `profile` enum('1','2','3','4') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_has_unit`
--

CREATE TABLE `user_has_unit` (
  `idUser` int(11) NOT NULL,
  `idUnit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `agreement`
--
ALTER TABLE `agreement`
  ADD PRIMARY KEY (`idAgreement`),
  ADD KEY `idCompany` (`idCompany`),
  ADD KEY `idTeacher` (`idTeacher`),
  ADD KEY `idLabor` (`idLabor`),
  ADD KEY `idAlumn` (`idAlumn`);

--
-- Indices de la tabla `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`idCompany`);

--
-- Indices de la tabla `day`
--
ALTER TABLE `day`
  ADD PRIMARY KEY (`idDay`),
  ADD KEY `idEntry` (`idEntry`);

--
-- Indices de la tabla `entry`
--
ALTER TABLE `entry`
  ADD PRIMARY KEY (`idEntry`),
  ADD KEY `idAgreement` (`idAgreement`);

--
-- Indices de la tabla `module`
--
ALTER TABLE `module`
  ADD PRIMARY KEY (`idModule`),
  ADD KEY `idUnit` (`idUnit`);

--
-- Indices de la tabla `unit`
--
ALTER TABLE `unit`
  ADD PRIMARY KEY (`idUnit`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`idUser`),
  ADD UNIQUE KEY `user_index_0` (`email`);

--
-- Indices de la tabla `user_has_unit`
--
ALTER TABLE `user_has_unit`
  ADD PRIMARY KEY (`idUser`,`idUnit`),
  ADD KEY `idUnit` (`idUnit`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `agreement`
--
ALTER TABLE `agreement`
  MODIFY `idAgreement` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `company`
--
ALTER TABLE `company`
  MODIFY `idCompany` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT de la tabla `day`
--
ALTER TABLE `day`
  MODIFY `idDay` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `entry`
--
ALTER TABLE `entry`
  MODIFY `idEntry` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `module`
--
ALTER TABLE `module`
  MODIFY `idModule` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `unit`
--
ALTER TABLE `unit`
  MODIFY `idUnit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `idUser` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `agreement`
--
ALTER TABLE `agreement`
  ADD CONSTRAINT `agreement_ibfk_1` FOREIGN KEY (`idCompany`) REFERENCES `company` (`idCompany`),
  ADD CONSTRAINT `agreement_ibfk_2` FOREIGN KEY (`idTeacher`) REFERENCES `user` (`idUser`),
  ADD CONSTRAINT `agreement_ibfk_3` FOREIGN KEY (`idLabor`) REFERENCES `user` (`idUser`),
  ADD CONSTRAINT `agreement_ibfk_4` FOREIGN KEY (`idAlumn`) REFERENCES `user` (`idUser`);

--
-- Filtros para la tabla `day`
--
ALTER TABLE `day`
  ADD CONSTRAINT `day_ibfk_1` FOREIGN KEY (`idEntry`) REFERENCES `entry` (`idEntry`);

--
-- Filtros para la tabla `entry`
--
ALTER TABLE `entry`
  ADD CONSTRAINT `entry_ibfk_1` FOREIGN KEY (`idAgreement`) REFERENCES `agreement` (`idAgreement`);

--
-- Filtros para la tabla `module`
--
ALTER TABLE `module`
  ADD CONSTRAINT `module_ibfk_1` FOREIGN KEY (`idUnit`) REFERENCES `unit` (`idUnit`);

--
-- Filtros para la tabla `user_has_unit`
--
ALTER TABLE `user_has_unit`
  ADD CONSTRAINT `user_has_unit_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `user` (`idUser`),
  ADD CONSTRAINT `user_has_unit_ibfk_2` FOREIGN KEY (`idUnit`) REFERENCES `unit` (`idUnit`);
COMMIT;


