-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Czas generowania: 12 Gru 2020, 15:47
-- Wersja serwera: 8.0.22
-- Wersja PHP: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `museum`
--

CREATE USER 'admin'@'%' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION; 


DELIMITER $$
--
-- Procedury
--
CREATE DEFINER=`admin`@`%` PROCEDURE `podsumowanie_zwiedzania` (IN `dzien` DATE, IN `oddzial` VARCHAR(100))  BEGIN
SELECT j.godzina_rozpoczecia, p.imie, p.nazwisko, j.liczba_uczestnikow FROM
   (SELECT h.godzina_rozpoczecia, h.pracownik_pesel, COUNT(b.id) AS liczba_uczestnikow FROM
    bilet b RIGHT JOIN harmonogram_zwiedzania h ON (b.harmonogram_zwiedzania_godzina_rozpoczecia=h.godzina_rozpoczecia AND b.harmonogram_zwiedzania_data=h.data)
	WHERE h.data=dzien
    GROUP BY h.godzina_rozpoczecia, h.pracownik_pesel) j LEFT JOIN pracownik p ON j.pracownik_pesel=p.pesel
    WHERE p.oddzial_nazwa=oddzial;
END$$

--
-- Funkcje
--
CREATE DEFINER=`admin`@`%` FUNCTION `policz_dochod` (`typ_biletu` VARCHAR(100)) RETURNS FLOAT DETERMINISTIC BEGIN
	DECLARE suma FLOAT DEFAULT 0; 
	SELECT SUM(r.cena) INTO suma FROM bilet b LEFT JOIN rodzaj_biletu r ON (b.rodzaj_biletu_typ=r.typ AND b.rodzaj_biletu_oddzial_nazwa=r.oddzial_nazwa AND b.rodzaj_biletu_czy_z_przewodnikiem=r.czy_z_przewodnikiem)
    WHERE b.rodzaj_biletu_typ=typ_biletu; 
    RETURN suma;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `artysta`
--

CREATE TABLE `artysta` (
  `id` int NOT NULL,
  `imie` varchar(50) NOT NULL,
  `nazwisko` varchar(50) NOT NULL,
  `data_urodzenia` date NOT NULL,
  `data_smierci` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `bilet`
--

CREATE TABLE `bilet` (
  `id` int NOT NULL,
  `data_zakupu` date NOT NULL,
  `rodzaj_biletu_typ` varchar(100) NOT NULL,
  `rodzaj_biletu_oddzial_nazwa` varchar(100) NOT NULL,
  `harmonogram_zwiedzania_godzina_rozpoczecia` time DEFAULT NULL,
  `harmonogram_zwiedzania_data` date DEFAULT NULL,
  `rodzaj_biletu_czy_z_przewodnikiem` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Zrzut danych tabeli `bilet`
--

INSERT INTO `bilet` (`id`, `data_zakupu`, `rodzaj_biletu_typ`, `rodzaj_biletu_oddzial_nazwa`, `harmonogram_zwiedzania_godzina_rozpoczecia`, `harmonogram_zwiedzania_data`, `rodzaj_biletu_czy_z_przewodnikiem`) VALUES
(1, '2020-12-08', 'normalny', 'muzeum narodowe w poznaniu', '12:00:00', '2020-12-09', 1),
(2, '2020-12-10', 'ulgowy', 'muzeum narodowe w warszawie', NULL, NULL, 0),
(3, '2020-12-06', 'ulgowy', 'muzeum narodowe w poznaniu', '12:00:00', '2020-12-09', 1),
(4, '2020-12-03', 'normalny', 'muzeum narodowe w warszawie', '12:00:00', '2020-12-09', 1),
(5, '2020-12-12', 'normalny', 'muzeum narodowe w poznaniu', NULL, NULL, 0);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `dzial`
--

CREATE TABLE `dzial` (
  `nazwa` varchar(100) NOT NULL,
  `pietro` int NOT NULL,
  `epoka` varchar(100) DEFAULT NULL,
  `oddzial_nazwa` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `harmonogram_zwiedzania`
--

CREATE TABLE `harmonogram_zwiedzania` (
  `godzina_rozpoczecia` time NOT NULL,
  `data` date NOT NULL,
  `pracownik_pesel` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Zrzut danych tabeli `harmonogram_zwiedzania`
--

INSERT INTO `harmonogram_zwiedzania` (`godzina_rozpoczecia`, `data`, `pracownik_pesel`) VALUES
('12:00:00', '2020-12-09', 65030565926),
('15:00:00', '2020-12-09', 65030565926),
('12:00:00', '2020-12-09', 89123185621);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `obraz`
--

CREATE TABLE `obraz` (
  `id` int NOT NULL,
  `nazwa` varchar(100) DEFAULT NULL,
  `szerokosc` float NOT NULL,
  `wysokosc` float NOT NULL,
  `artysta_id` int NOT NULL,
  `dzial_nazwa` varchar(100) NOT NULL,
  `dzial_oddzial_nazwa` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `oddzial`
--

CREATE TABLE `oddzial` (
  `nazwa` varchar(100) NOT NULL,
  `godzina_otwarcia` time NOT NULL,
  `godzina_zamkniecia` time NOT NULL,
  `adres` varchar(100) NOT NULL,
  `numer_telefonu` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Zrzut danych tabeli `oddzial`
--

INSERT INTO `oddzial` (`nazwa`, `godzina_otwarcia`, `godzina_zamkniecia`, `adres`, `numer_telefonu`) VALUES
('muzeum narodowe w poznaniu', '11:00:00', '18:00:00', 'Aleje Marcinkowskiego 9, 61-745 Poznań', 618568000),
('muzeum narodowe w warszawie', '10:00:00', '19:00:00', 'Al. Jerozolimskie 3, 00-495 Warszawa', 226211031);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `pracownik`
--

CREATE TABLE `pracownik` (
  `pesel` bigint NOT NULL,
  `imie` varchar(50) NOT NULL,
  `nazwisko` varchar(50) NOT NULL,
  `placa` int NOT NULL,
  `etat` varchar(50) NOT NULL,
  `data_zatrudnienia` date NOT NULL,
  `numer_telefonu` int DEFAULT NULL,
  `oddzial_nazwa` varchar(100) NOT NULL
) ;

--
-- Zrzut danych tabeli `pracownik`
--

INSERT INTO `pracownik` (`pesel`, `imie`, `nazwisko`, `placa`, `etat`, `data_zatrudnienia`, `numer_telefonu`, `oddzial_nazwa`) VALUES
(121212345, 'Antoni', 'Nowak', 500, 'stazysta', '2020-11-10', 123123123, 'muzeum narodowe w poznaniu'),
(65030565926, 'Kazimierz', 'Dudziak', 3000, 'pracownik', '2017-12-16', NULL, 'muzeum narodowe w poznaniu'),
(78010145673, 'Anna', 'Kowalska', 10000, 'kierownik', '2002-03-10', 501501501, 'muzeum narodowe w poznaniu'),
(89123185621, 'Nadia', 'Stachowiak', 3500, 'pracownik', '2016-08-11', 802492749, 'muzeum narodowe w warszawie');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `rodzaj_biletu`
--

CREATE TABLE `rodzaj_biletu` (
  `typ` varchar(100) NOT NULL,
  `czy_z_przewodnikiem` tinyint(1) NOT NULL,
  `cena` float NOT NULL,
  `oddzial_nazwa` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Zrzut danych tabeli `rodzaj_biletu`
--

INSERT INTO `rodzaj_biletu` (`typ`, `czy_z_przewodnikiem`, `cena`, `oddzial_nazwa`) VALUES
('normalny', 0, 20, 'muzeum narodowe w poznaniu'),
('normalny', 0, 30, 'muzeum narodowe w warszawie'),
('normalny', 1, 25, 'muzeum narodowe w poznaniu'),
('normalny', 1, 40, 'muzeum narodowe w warszawie'),
('ulgowy', 0, 10, 'muzeum narodowe w poznaniu'),
('ulgowy', 0, 20, 'muzeum narodowe w warszawie'),
('ulgowy', 1, 12.5, 'muzeum narodowe w poznaniu'),
('ulgowy', 1, 30, 'muzeum narodowe w warszawie');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `rzezba`
--

CREATE TABLE `rzezba` (
  `id` int NOT NULL,
  `nazwa` varchar(100) DEFAULT NULL,
  `waga` float NOT NULL,
  `material` varchar(50) NOT NULL,
  `artysta_id` int NOT NULL,
  `dzial_nazwa` varchar(100) NOT NULL,
  `dzial_oddzial_nazwa` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `wydarzenie`
--

CREATE TABLE `wydarzenie` (
  `nazwa` varchar(100) NOT NULL,
  `data_rozpoczecia` date NOT NULL,
  `data_zakonczenia` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `wydarzenie_oddzial`
--

CREATE TABLE `wydarzenie_oddzial` (
  `oddzial_nazwa` varchar(100) NOT NULL,
  `wydarzenie_nazwa` varchar(100) NOT NULL,
  `wydarzenie_data_rozpoczecia` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `artysta`
--
ALTER TABLE `artysta`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `bilet`
--
ALTER TABLE `bilet`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bilet_rodzaj_biletu` (`rodzaj_biletu_typ`,`rodzaj_biletu_czy_z_przewodnikiem`,`rodzaj_biletu_oddzial_nazwa`),
  ADD KEY `bilet_harmonogram_zwiedzania_FK` (`harmonogram_zwiedzania_data`,`harmonogram_zwiedzania_godzina_rozpoczecia`) USING BTREE;

--
-- Indeksy dla tabeli `dzial`
--
ALTER TABLE `dzial`
  ADD PRIMARY KEY (`nazwa`,`oddzial_nazwa`) USING BTREE,
  ADD KEY `dzial_oddzial_fk` (`oddzial_nazwa`);

--
-- Indeksy dla tabeli `harmonogram_zwiedzania`
--
ALTER TABLE `harmonogram_zwiedzania`
  ADD PRIMARY KEY (`data`,`godzina_rozpoczecia`,`pracownik_pesel`),
  ADD KEY `harmonogram_zwiedzania_pracownik_FK` (`pracownik_pesel`);

--
-- Indeksy dla tabeli `obraz`
--
ALTER TABLE `obraz`
  ADD PRIMARY KEY (`id`),
  ADD KEY `obraz_dzial_FK` (`dzial_nazwa`,`dzial_oddzial_nazwa`) USING BTREE,
  ADD KEY `obraz_artysta_FK` (`artysta_id`);

--
-- Indeksy dla tabeli `oddzial`
--
ALTER TABLE `oddzial`
  ADD PRIMARY KEY (`nazwa`);

--
-- Indeksy dla tabeli `pracownik`
--
ALTER TABLE `pracownik`
  ADD PRIMARY KEY (`pesel`),
  ADD KEY `pracownik_oddzial_FK` (`oddzial_nazwa`);

--
-- Indeksy dla tabeli `rodzaj_biletu`
--
ALTER TABLE `rodzaj_biletu`
  ADD PRIMARY KEY (`typ`,`czy_z_przewodnikiem`,`oddzial_nazwa`) USING BTREE,
  ADD KEY `rodzaj_biletu_oddzial_FK` (`oddzial_nazwa`);

--
-- Indeksy dla tabeli `rzezba`
--
ALTER TABLE `rzezba`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rzezba_dzial_FK` (`dzial_nazwa`,`dzial_oddzial_nazwa`),
  ADD KEY `rzezba_artysta_FK` (`artysta_id`);

--
-- Indeksy dla tabeli `wydarzenie`
--
ALTER TABLE `wydarzenie`
  ADD PRIMARY KEY (`nazwa`,`data_rozpoczecia`);

--
-- Indeksy dla tabeli `wydarzenie_oddzial`
--
ALTER TABLE `wydarzenie_oddzial`
  ADD PRIMARY KEY (`oddzial_nazwa`,`wydarzenie_data_rozpoczecia`,`wydarzenie_nazwa`),
  ADD KEY `wydarzenie_FK` (`wydarzenie_nazwa`,`wydarzenie_data_rozpoczecia`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `artysta`
--
ALTER TABLE `artysta`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `bilet`
--
ALTER TABLE `bilet`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT dla tabeli `obraz`
--
ALTER TABLE `obraz`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT dla tabeli `rzezba`
--
ALTER TABLE `rzezba`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `bilet`
--
ALTER TABLE `bilet`
  ADD CONSTRAINT `bilet_harmonogram_zwiedzania_FK` FOREIGN KEY (`harmonogram_zwiedzania_data`,`harmonogram_zwiedzania_godzina_rozpoczecia`) REFERENCES `harmonogram_zwiedzania` (`data`, `godzina_rozpoczecia`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `bilet_rodzaj_biletu` FOREIGN KEY (`rodzaj_biletu_typ`,`rodzaj_biletu_czy_z_przewodnikiem`,`rodzaj_biletu_oddzial_nazwa`) REFERENCES `rodzaj_biletu` (`typ`, `czy_z_przewodnikiem`, `oddzial_nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `dzial`
--
ALTER TABLE `dzial`
  ADD CONSTRAINT `dzial_oddzial_fk` FOREIGN KEY (`oddzial_nazwa`) REFERENCES `oddzial` (`nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `harmonogram_zwiedzania`
--
ALTER TABLE `harmonogram_zwiedzania`
  ADD CONSTRAINT `harmonogram_zwiedzania_pracownik_FK` FOREIGN KEY (`pracownik_pesel`) REFERENCES `pracownik` (`pesel`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `obraz`
--
ALTER TABLE `obraz`
  ADD CONSTRAINT `obraz_artysta_FK` FOREIGN KEY (`artysta_id`) REFERENCES `artysta` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `obraz_oddzial_FK` FOREIGN KEY (`dzial_nazwa`,`dzial_oddzial_nazwa`) REFERENCES `dzial` (`nazwa`, `oddzial_nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `pracownik`
--
ALTER TABLE `pracownik`
  ADD CONSTRAINT `pracownik_oddzial_FK` FOREIGN KEY (`oddzial_nazwa`) REFERENCES `oddzial` (`nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `rodzaj_biletu`
--
ALTER TABLE `rodzaj_biletu`
  ADD CONSTRAINT `rodzaj_biletu_oddzial_FK` FOREIGN KEY (`oddzial_nazwa`) REFERENCES `oddzial` (`nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `rzezba`
--
ALTER TABLE `rzezba`
  ADD CONSTRAINT `rzezba_artysta_FK` FOREIGN KEY (`artysta_id`) REFERENCES `artysta` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `rzezba_dzial_FK` FOREIGN KEY (`dzial_nazwa`,`dzial_oddzial_nazwa`) REFERENCES `dzial` (`nazwa`, `oddzial_nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `wydarzenie_oddzial`
--
ALTER TABLE `wydarzenie_oddzial`
  ADD CONSTRAINT `oddzial_FK` FOREIGN KEY (`oddzial_nazwa`) REFERENCES `oddzial` (`nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `wydarzenie_FK` FOREIGN KEY (`wydarzenie_nazwa`,`wydarzenie_data_rozpoczecia`) REFERENCES `wydarzenie` (`nazwa`, `data_rozpoczecia`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;
 
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
