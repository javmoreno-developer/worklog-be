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
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp(),
  `dualStartAt` date NULL,
  `dualEndAt` date NULL,
  `fctStartAt` date NULL,
  `fctEndAt` date NULL,
  `agreementType` enum('fct','dual','fct+dual') NOT NULL,
  `idCompany` int(11) NULL,
  `idTeacher` int(11) NULL,
  `idLabor` int(11) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `company`
--

CREATE TABLE `company` (
  `idCompany` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  `phone` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `company`
--

INSERT INTO `company` (`idCompany`, `name`, `address`, `latitude`, `longitude`, `phone`) VALUES
(1, 'Accenture', 'Edificio I+D6, C. Severo Ochoa, 21, Edificio I+D 6, 29590 Campanillas, Málaga', '36.734565', '-4.557203', '952 04 57 50'),
(2, 'ByEvolution', 'C. de Marie Curie, 9, bloque 4, 29590 Málaga', '36.737480', '-4.549195', '951 17 32 82'),
(3, 'Cathedral Software', 'C. de Marie Curie, 12, Oficina A2, 29590 Málaga', '36.736287', '-4.549213', ''),
(4, 'Viewnext', '', '0.000000', '0.000000', ''),
(5, 'Properly', 'C. Graham Bell, 6, Planta 1, Oficina 9, 29590 Málaga', '36.733033', '-4.547617', '952 02 02 00'),
(6, 'Rewe', '', '0.000000', '0.000000', ''),
(7, 'Rocketfy', 'C. de Marie Curie, nº 4, 1º Planta, 29590 Málaga', '36.736861', '-4.550804', '951 04 37 74'),
(8, 'Solbyte', '', '0.000000', '0.000000', ''),
(9, 'Freepik', '', '0.000000', '0.000000', ''),
(10, 'Navicom', '', '0.000000', '0.000000', ''),
(11, 'Dekra', 'Pq Tecnológico, C. Severo Ochoa, 6, 29590 Maqueda, Málaga', '36.735143', '-4.554254', '952 61 91 00'),
(12, 'Mayoral', '', '0.000000', '0.000000', ''),
(13, 'Rindus', 'C. Severo Ochoa, 29, 29590 Málaga', '36.73628', '-4.556896', '951 12 00 35'),
(14, 'Safamotor', '', '0.000000', '0.000000', ''),
(15, 'Vicox', '', '0.000000', '0.000000', ''),
(16, 'Top Digital', '', '0.000000', '0.000000', ''),
(17, 'BIC Euronova', 'Av. Juan López de Peñalver, 21, 29590 Málaga', '36.737598', '-4.553678', '951 01 05 04'),
(18, 'Everis', '', '0.000000', '0.000000', ''),
(19, 'InComputer', '', '0.000000', '0.000000', ''),
(20, 'Dworkin', '', '0.000000', '0.000000', ''),
(21, 'SecureKids', 'C. Pierre Laffitte, Nº 6, 29590 Málaga', '36.746748', '-4.551930', ''),
(22, 'Click Help Point', '', '0.000000', '0.000000', ''),
(23, 'Institute of Physics of the Czech Academy of Sciences', '', '0.000000', '0.000000', ''),
(24, 'Enreach - Summa', 'Av. Juan López de Peñalver, NUM. 21, 29590 Málaga', '36.737544', '-4.554182', '951 12 09 52'),
(25, 'TraffGen Global', '', '0.000000', '0.000000', ''),
(26, 'NTT Data - Everis', '', '0.000000', '0.000000', ''),
(27, 'Verisk', '', '0.000000', '0.000000', ''),
(28, 'OP Plus', 'Edificio Alei Center, C. Severo Ochoa, 51, 29590 Málaga', '36.738872', '-4.554614', '952 57 92 81'),
(29, 'Adivin Beach Flag', '', '0.000000', '0.000000', ''),
(30, 'Babel', '', '0.000000', '0.000000', ''),
(31, 'Hispasec', 'C. Severo Ochoa, 10, 29590 Málaga', '36.734174', '-4.555841', '952 02 04 94'),
(32, 'EY', 'C. Severo Ochoa, 29590 Málaga', '36.734865', '-4.557289', ''),
(33, 'ASAC', '', '0.000000', '0.000000', ''),
(34, 'Fantozzi Ufficio', '', '0.000000', '0.000000', ''),
(35, 'Wevoice', '', '0.000000', '0.000000', ''),
(36, 'Aliqindoi', '', '0.000000', '0.000000', ''),
(37, 'DHV Technology', 'Av. Juan López de Peñalver, 21, 29590 Málaga', '36.737256', '-4.554010', '951 95 68 37'),
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
-- Estructura de tabla para la tabla `comment`
--

CREATE TABLE `comment` (
  `idComment` int(11) NOT NULL,
  `text` varchar(255) NOT NULL,
  `hours` time NULL,
  `observations` varchar(255) DEFAULT NULL,
  `idEntry` int(11) NOT NULL,
  `idModule` int(11) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entry`
--

CREATE TABLE `entry` (
  `idEntry` int(11) NOT NULL,
  `startWeek` date NOT NULL,
  `endWeek` date NOT NULL,
  `idAgreement` int(11) NULL
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
  `description` varchar(255) NOT NULL,
  `idUnit` int(11) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `module`
--

INSERT INTO `module` (`idModule`, `name`, `initials`, `hours`, `description`, `idUnit`) VALUES
(1, 'Sistemas Informáticos', 'SINF', 6, '', 1),
(2, 'Programación', 'PROG', 8, '', 1),
(3, 'Lenguajes de Marcas y Sistemas de Gestión de la Información', 'LMSGI', 4, '', 1),
(4, 'Entornos de Desarrollo', 'ED', 3, '', 1),
(5, 'Bases de Datos', 'BDAT', 8, '', 1),
(7, 'Desarrollo Web en Entorno Servidor', 'DWES', 8, '', 2),
(8, 'Desarrollo Web en Entorno Cliente', 'DWEC', 8, '', 2),
(9, 'Diseño de Interfaces', 'DI', 7, '', 2),
(10, 'Despliegue de Aplicaciones Web', 'DAW', 3, '', 2),
(12, 'Sistemas Informáticos', 'SINF', 6, '', 3),
(13, 'Programación', 'PROG', 8, '', 3),
(14, 'Lenguajes de Marcas y Sistemas de Gestión de la Información', 'LMSGI', 4, '', 3),
(15, 'Entornos de Desarrollo', 'ED', 3, '', 3),
(16, 'Bases de Datos', 'BDAT', 8, '', 3),
(18, 'Acceso a Datos', 'ADAT', 5, '', 4),
(19, 'Programación Multimedia y de Dispositivos Móviles', 'PMDM', 4, '', 4),
(20, 'Programación de Servicios y Procesos', 'PSP', 3, '', 4),
(21, 'Desarrollo de Interfaces', 'DI', 7, '', 4),
(22, 'Sistemas de Gestión Empresarial', 'SGE', 4, '', 4),
(23, 'Hacking Ético', 'HE', NULL, '', 7),
(24, 'Incidentes de Ciberseguridad', 'ICS', NULL, '', 7),
(25, 'Bastionado de Redes y Sistemas', 'BRS', NULL, '', 7),
(26, 'Análisis Forense', 'AFOR', NULL, '', 7),
(27, 'Normativa de Ciberseguridad', 'NOR', NULL, '', 7),
(28, 'Puesta en Producción Segura', 'PPS', NULL, '', 7),
(29, 'Modelos de Inteligencia Artificial', 'MIA', 3, '', 8),
(30, 'Sistemas de Aprendizaje Automático', 'SAA', 3, '', 8),
(31, 'Programación de Inteligencia Artificial', 'PIA', 7, '', 8),
(32, 'Sistemas de Big Data', 'SBD', 3, '', 8),
(33, 'Bid Data Aplicado', 'BDA', 4, '', 8),
(34, 'Programación y Motores de Videojuegos', 'PMV', NULL, '', 9),
(35, 'Diseño Gráfico 2D y 3D', 'DG', NULL, '', 9),
(36, 'Programación en Red e Inteligencia Artificial', 'PRIA', NULL, '', 9),
(37, 'Realidad Virtual y Realidad Aumentada', 'RVRA', NULL, '', 9),
(38, 'Gestión, publicación y Producción', 'GPP', NULL, '', 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `unit`
--

CREATE TABLE `unit` (
  `idUnit` int(11) NOT NULL,
  `level` tinyint(4) NOT NULL,
  `name` varchar(255) NOT NULL,
  `initials` varchar(10) NOT NULL,
  `charUnit` char(1) DEFAULT NULL,
  `unitType` enum('morning','evening') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `unit`
--

INSERT INTO `unit` (`idUnit`, `level`, `name`, `initials`, `charUnit`, `unitType`) VALUES
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
  `profile` enum('1','2','3','4') NOT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `student_scholar_year`
--

CREATE TABLE `student_scholar_year` (
  `idStudentYear` int(11) NOT NULL,
  `idStudent` int(11) NOT NULL,
  `idScholarYear` int(11) NOT NULL,
  `idUnit` int(11) NOT NULL,
  `idAgreement` int(11) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `scholarYear`
--

CREATE TABLE `scholarYear` (
  `idScholarYear` int(11) NOT NULL,
  `startDate` date NOT NULL DEFAULT '0000-00-00',
  `endDate` date NOT NULL DEFAULT '0000-00-00',
  `year` varchar(9) NOT NULL DEFAULT '0000-0000',
  `aptitudesPonderation` int(3) NOT NULL DEFAULT 10,
  `subjectsPonderation` int(3) NOT NULL DEFAULT 90,
  `holidays` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `scholarYear` (`idScholarYear`, `startDate`, `endDate`, `year`, `aptitudesPonderation`, `subjectsPonderation`, `holidays`) VALUES
(1, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT);

--
-- Estructura de tabla para la tabla `report`
--

CREATE TABLE `report` (
  `idReport` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `idAgreement` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Estructura de tabla para la tabla `item`
--

CREATE TABLE `item` (
  `idItem` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `item` (`idItem`, `name`) VALUES
(1, 'Puntualidad'),
(2, 'Habilidades y destrezas'),
(3, 'Ténicas y procedimientos'),
(4, 'Competencias profesionales'),
(5, 'Relaciones con el equipo de trabajo');

--
-- Estructura de tabla para la tabla `report_item`
--

CREATE TABLE `report_item` (
  `idReport` int(11) NOT NULL,
  `idItem` int(11) NOT NULL,
  `grade` int(1) NULL DEFAULT NULL,
  `observation` text NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Estructura de tabla para la tabla `report_module`
--

CREATE TABLE `report_module` (
  `idReport` int(11) NOT NULL,
  `idModule` int(11) NOT NULL,
  `grade` int(1) NULL DEFAULT NULL,
  `observation` text NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------

ALTER TABLE `report_item`
ADD CONSTRAINT `check_item_grade`
CHECK (`grade` IN (1, 2, 3, 4, 5));

ALTER TABLE `report_module`
ADD CONSTRAINT `check_module_grade`
CHECK (`grade` IN (1, 2, 3, 4, 5));

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `scholarYear`
--
ALTER TABLE `scholarYear`
  ADD PRIMARY KEY (`idScholarYear`),
  ADD UNIQUE KEY `unique_year` (`year`);;

--
-- Indices de la tabla `report`
--
ALTER TABLE `report`
  ADD PRIMARY KEY (`idReport`);

--
-- Indices de la tabla `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`idItem`);

--
-- Indices de la tabla `report_item`
--
ALTER TABLE `report_item`
  ADD PRIMARY KEY (`idReport`, `idItem`);

--
-- Indices de la tabla `report_module`
--
ALTER TABLE `report_module`
  ADD PRIMARY KEY (`idReport`, `idModule`);

--
-- Indices de la tabla `agreement`
--
ALTER TABLE `agreement`
  ADD PRIMARY KEY (`idAgreement`),
  ADD KEY `idCompany` (`idCompany`),
  ADD KEY `idTeacher` (`idTeacher`),
  ADD KEY `idLabor` (`idLabor`);

--
-- Indices de la tabla `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`idCompany`);

--
-- Indices de la tabla `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`idComment`),
  ADD KEY `idEntry` (`idEntry`),
  ADD KEY `idModule` (`idModule`);

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
  ADD PRIMARY KEY (`idModule`);

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
-- Indices de la tabla `student_scholar_year`
--
ALTER TABLE `student_scholar_year`
  ADD PRIMARY KEY (`idStudentYear`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `scholarYear`
--
ALTER TABLE `scholarYear`
  MODIFY `idScholarYear` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `report`
--
ALTER TABLE `report`
  MODIFY `idReport` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `item`
--
ALTER TABLE `item`
  MODIFY `idItem` int(11) NOT NULL AUTO_INCREMENT;

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
-- AUTO_INCREMENT de la tabla `comment`
--
ALTER TABLE `comment`
  MODIFY `idComment` int(11) NOT NULL AUTO_INCREMENT;

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
-- AUTO_INCREMENT de la tabla `student_scholar_year`
--
ALTER TABLE `student_scholar_year`
  MODIFY `idStudentYear` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `agreement`
--
ALTER TABLE `agreement`
  ADD CONSTRAINT `agreement_ibfk_1` FOREIGN KEY (`idCompany`) REFERENCES `company` (`idCompany`) ON DELETE SET NULL,
  ADD CONSTRAINT `agreement_ibfk_2` FOREIGN KEY (`idTeacher`) REFERENCES `user` (`idUser`) ON DELETE SET NULL,
  ADD CONSTRAINT `agreement_ibfk_3` FOREIGN KEY (`idLabor`) REFERENCES `user` (`idUser`) ON DELETE SET NULL;

--
-- Filtros para la tabla `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`idEntry`) REFERENCES `entry` (`idEntry`) ON DELETE CASCADE,
  ADD CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`idModule`) REFERENCES `module` (`idModule`) ON DELETE SET NULL;

--
-- Filtros para la tabla `entry`
--
ALTER TABLE `entry`
  ADD CONSTRAINT `entry_ibfk_1` FOREIGN KEY (`idAgreement`) REFERENCES `agreement` (`idAgreement`) ON DELETE CASCADE;

--
-- Filtros para la tabla `module`
--
ALTER TABLE `module`
  ADD CONSTRAINT `module_ibfk_1` FOREIGN KEY (`idUnit`) REFERENCES `unit` (`idUnit`) ON DELETE CASCADE;

--
-- Filtros para la tabla `student_scholar_year`
--
ALTER TABLE `student_scholar_year`
  ADD CONSTRAINT `student_scholar_year_ibfk_1` FOREIGN KEY (`idStudent`) REFERENCES `user` (`idUser`) ON DELETE CASCADE,
  ADD CONSTRAINT `student_scholar_year_ibfk_2` FOREIGN KEY (`idScholarYear`) REFERENCES `scholarYear` (`idScholarYear`) ON DELETE CASCADE,
  ADD CONSTRAINT `student_scholar_year_ibfk_3` FOREIGN KEY (`idUnit`) REFERENCES `unit` (`idUnit`) ON DELETE CASCADE,
  ADD CONSTRAINT `student_scholar_year_ibfk_4` FOREIGN KEY (`idAgreement`) REFERENCES `agreement` (`idAgreement`) ON DELETE SET NULL;

--
-- Filtros para la tabla `report`
--
ALTER TABLE `report`
  ADD CONSTRAINT `report_ibfk_1` FOREIGN KEY (`idAgreement`) REFERENCES `agreement` (`idAgreement`) ON DELETE CASCADE;

--
-- Filtros para la tabla `report_item`
--
ALTER TABLE `report_item`
  ADD CONSTRAINT `report_item_ibfk_1` FOREIGN KEY (`idReport`) REFERENCES `report` (`idReport`) ON DELETE CASCADE,
  ADD CONSTRAINT `report_item_ibfk_2` FOREIGN KEY (`idItem`) REFERENCES `item` (`idItem`) ON DELETE CASCADE;

--
-- Filtros para la tabla `report_module`
--
ALTER TABLE `report_module`
  ADD CONSTRAINT `report_module_ibfk_1` FOREIGN KEY (`idReport`) REFERENCES `report` (`idReport`) ON DELETE CASCADE,
  ADD CONSTRAINT `report_module_ibfk_2` FOREIGN KEY (`idModule`) REFERENCES `module` (`idModule`) ON DELETE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
