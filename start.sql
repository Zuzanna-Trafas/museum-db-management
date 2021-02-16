-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Czas generowania: 14 Gru 2020, 12:38
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
CREATE DEFINER=`admin`@`%` PROCEDURE `podsumowanie_zwiedzania` ()  BEGIN
SELECT j.data, j.godzina_rozpoczecia, p.imie, p.nazwisko, j.liczba_uczestnikow FROM
   (SELECT h.data, h.godzina_rozpoczecia, h.pracownik_pesel_id, COUNT(b.id) AS liczba_uczestnikow FROM
    museum_app_bilet b RIGHT JOIN museum_app_harmonogram_zwiedzania h ON (b.harmonogram_zwiedzania_id_id=h.id)
    GROUP BY h.data, h.godzina_rozpoczecia, h.pracownik_pesel_id) j LEFT JOIN museum_app_pracownik p ON j.pracownik_pesel_id=p.pesel;
END$$

--
-- Funkcje
--
CREATE DEFINER=`admin`@`%` FUNCTION `policz_dochod` (`typ_biletu` VARCHAR(100), `czy_z_przewodnikiem` TINYINT(1), `oddzial` VARCHAR(100)) RETURNS FLOAT DETERMINISTIC BEGIN
	DECLARE suma FLOAT DEFAULT 0;
	SELECT SUM(r.cena) INTO suma FROM museum_app_bilet b LEFT JOIN museum_app_rodzaj_biletu r ON (b.rodzaj_biletu_typ_id=r.typ AND b.rodzaj_biletu_oddzial_nazwa_id=r.oddzial_nazwa_id AND b.rodzaj_biletu_czy_z_przewodnikiem_id=r.czy_z_przewodnikiem)
    WHERE b.rodzaj_biletu_typ_id=typ_biletu AND b.rodzaj_biletu_czy_z_przewodnikiem_id=czy_z_przewodnikiem AND b.rodzaj_biletu_oddzial_nazwa_id=oddzial;
    RETURN suma;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `museum_app_artysta`
--

CREATE TABLE `museum_app_artysta` (
  `id` int NOT NULL,
  `imie` varchar(50) NOT NULL,
  `nazwisko` varchar(50) NOT NULL,
  `data_urodzenia` date NOT NULL,
  `data_smierci` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_artysta`
--

INSERT INTO `museum_app_artysta` (`id`, `imie`, `nazwisko`, `data_urodzenia`, `data_smierci`) VALUES
(1, 'Jacek', 'Malczewski', '1854-07-14', '1929-10-08'),
(2, 'Claude', 'Monet', '1840-11-14', '1926-12-05'),
(3, 'Kazimierz', 'Adamski', '1964-07-20', NULL);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `museum_app_bilet`
--

CREATE TABLE `museum_app_bilet` (
  `id` int NOT NULL,
  `data_zakupu` date NOT NULL,
  `rodzaj_biletu_typ_id` varchar(100) NOT NULL,
  `rodzaj_biletu_oddzial_nazwa_id` varchar(100) NOT NULL,
  `harmonogram_zwiedzania_id_id` int DEFAULT NULL,
  `rodzaj_biletu_czy_z_przewodnikiem_id` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_bilet`
--

INSERT INTO `museum_app_bilet` (`id`, `data_zakupu`, `rodzaj_biletu_typ_id`, `rodzaj_biletu_oddzial_nazwa_id`, `harmonogram_zwiedzania_id_id`, `rodzaj_biletu_czy_z_przewodnikiem_id`) VALUES
(1, '2020-12-08', 'normalny', 'muzeum narodowe w poznaniu', 1, 1),
(2, '2020-12-10', 'ulgowy', 'muzeum narodowe w warszawie', NULL, 0),
(3, '2020-12-06', 'ulgowy', 'muzeum narodowe w poznaniu', 3, 1),
(4, '2020-12-03', 'normalny', 'muzeum narodowe w warszawie', 2, 1),
(5, '2020-12-12', 'normalny', 'muzeum narodowe w poznaniu', NULL, 0);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `museum_app_dzial`
--

CREATE TABLE `museum_app_dzial` (
  `nazwa` varchar(100) NOT NULL,
  `pietro` int NOT NULL,
  `epoka` varchar(100) DEFAULT NULL,
  `oddzial_nazwa_id` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_dzial`
--

INSERT INTO `museum_app_dzial` (`nazwa`, `pietro`, `epoka`, `oddzial_nazwa_id`) VALUES
('sztuka europejska XIV-XIX wieku', 1, NULL, 'muzeum narodowe w poznaniu'),
('sztuka nowoczesna', 2, 'wspolczesnosc', 'muzeum narodowe w warszawie'),
('sztuka polska I pol. XX wieku', 1, 'mloda polska', 'muzeum narodowe w poznaniu'),
('sztuka sredniowieczna', 1, 'sredniowiecze', 'muzeum narodowe w poznaniu'),
('sztuka sredniowieczna', 0, 'sredniowiecze', 'muzeum narodowe w warszawie');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `museum_app_harmonogram_zwiedzania`
--

CREATE TABLE `museum_app_harmonogram_zwiedzania` (
  `id` int NOT NULL,
  `godzina_rozpoczecia` time NOT NULL,
  `data` date NOT NULL,
  `pracownik_pesel_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_harmonogram_zwiedzania`
--

INSERT INTO `museum_app_harmonogram_zwiedzania` (`id`, `godzina_rozpoczecia`, `data`, `pracownik_pesel_id`) VALUES
(1, '12:00:00', '2020-12-09', 65030565926),
(2, '15:00:00', '2020-12-09', 65030565926),
(3, '12:00:00', '2020-12-09', 89123185621);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `museum_app_obraz`
--

CREATE TABLE `museum_app_obraz` (
  `id` int NOT NULL,
  `nazwa` varchar(100) DEFAULT NULL,
  `szerokosc` float NOT NULL,
  `wysokosc` float NOT NULL,
  `artysta_id_id` int DEFAULT NULL,
  `dzial_nazwa_id` varchar(100) NOT NULL,
  `dzial_oddzial_nazwa_id` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_obraz`
--

INSERT INTO `museum_app_obraz` (`id`, `nazwa`, `szerokosc`, `wysokosc`, `artysta_id_id`, `dzial_nazwa_id`, `dzial_oddzial_nazwa_id`) VALUES
(1, 'drzewo nad stawem', 41, 33, 1, 'sztuka polska I pol. XX wieku', 'muzeum narodowe w poznaniu'),
(2, 'bledne kolo', 240, 174, 1, 'sztuka polska I pol. XX wieku', 'muzeum narodowe w poznaniu'),
(3, 'melancholia', 240, 139, 1, 'sztuka polska I pol. XX wieku', 'muzeum narodowe w poznaniu'),
(4, 'plaza w pourville', 60, 73, 2, 'sztuka europejska XIV-XIX wieku', 'muzeum narodowe w poznaniu'),
(5, 'nawiedzenie', 40, 100, NULL, 'sztuka sredniowieczna', 'muzeum narodowe w poznaniu');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `museum_app_oddzial`
--

CREATE TABLE `museum_app_oddzial` (
  `nazwa` varchar(100) NOT NULL,
  `godzina_otwarcia` time NOT NULL,
  `godzina_zamkniecia` time NOT NULL,
  `adres` varchar(100) NOT NULL,
  `numer_telefonu` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_oddzial`
--

INSERT INTO `museum_app_oddzial` (`nazwa`, `godzina_otwarcia`, `godzina_zamkniecia`, `adres`, `numer_telefonu`) VALUES
('muzeum narodowe w poznaniu', '11:00:00', '18:00:00', 'Aleje Marcinkowskiego 9, 61-745 Poznań', 618568000),
('muzeum narodowe w warszawie', '10:00:00', '19:00:00', 'Al. Jerozolimskie 3, 00-495 Warszawa', 226211031);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `museum_app_pracownik`
--

CREATE TABLE `museum_app_pracownik` (
  `pesel` bigint NOT NULL,
  `imie` varchar(50) NOT NULL,
  `nazwisko` varchar(50) NOT NULL,
  `placa` int NOT NULL,
  `etat` varchar(50) NOT NULL,
  `data_zatrudnienia` date NOT NULL,
  `numer_telefonu` varchar(20) DEFAULT NULL,
  `oddzial_nazwa_id` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_pracownik`
--

INSERT INTO `museum_app_pracownik` (`pesel`, `imie`, `nazwisko`, `placa`, `etat`, `data_zatrudnienia`, `numer_telefonu`, `oddzial_nazwa_id`) VALUES
(121212345, 'Antoni', 'Nowak', 500, 'stazysta', '2020-11-10', 123123123, 'muzeum narodowe w poznaniu'),
(65030565926, 'Kazimierz', 'Dudziak', 3000, 'pracownik', '2017-12-16', NULL, 'muzeum narodowe w poznaniu'),
(78010145673, 'Anna', 'Kowalska', 10000, 'kierownik', '2002-03-10', 501501501, 'muzeum narodowe w poznaniu'),
(89123185621, 'Nadia', 'Stachowiak', 3500, 'pracownik', '2016-08-11', 802492749, 'muzeum narodowe w warszawie');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `museum_app_rodzaj_biletu`
--

CREATE TABLE `museum_app_rodzaj_biletu` (
  `typ` varchar(100) NOT NULL,
  `czy_z_przewodnikiem` tinyint(1) NOT NULL,
  `cena` float NOT NULL,
  `oddzial_nazwa_id` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_rodzaj_biletu`
--

INSERT INTO `museum_app_rodzaj_biletu` (`typ`, `czy_z_przewodnikiem`, `cena`, `oddzial_nazwa_id`) VALUES
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

CREATE TABLE `museum_app_rzezba` (
  `id` int NOT NULL,
  `nazwa` varchar(100) DEFAULT NULL,
  `waga` float NOT NULL,
  `material` varchar(50) NOT NULL,
  `artysta_id_id` int DEFAULT NULL,
  `dzial_nazwa_id` varchar(100) NOT NULL,
  `dzial_oddzial_nazwa_id` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_rzezba`
--

INSERT INTO `museum_app_rzezba` (`id`, `nazwa`, `waga`, `material`, `artysta_id_id`, `dzial_nazwa_id`, `dzial_oddzial_nazwa_id`) VALUES
(1, 'popiersie adama loreta', 48, 'braz', 3, 'sztuka nowoczesna', 'muzeum narodowe w warszawie'),
(2, 'pieta z lubiaza', 30, 'drewno lipowe', NULL, 'sztuka sredniowieczna', 'muzeum narodowe w warszawie');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `museum_app_wydarzenie`
--

CREATE TABLE `museum_app_wydarzenie` (
  `nazwa` varchar(100) NOT NULL,
  `data_rozpoczecia` date NOT NULL,
  `data_zakonczenia` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_wydarzenie`
--

INSERT INTO `museum_app_wydarzenie` (`nazwa`, `data_rozpoczecia`, `data_zakonczenia`) VALUES
('dzien seniora', '2021-01-30', '2021-01-30'),
('noc w muzeum', '2021-02-19', '2021-02-19'),
('wystawa prac studentow', '2021-06-01', '2021-06-30');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `museum_app_wydarzenie_oddzial`
--

CREATE TABLE `museum_app_wydarzenie_oddzial` (
  `oddzial_nazwa_id` varchar(100) NOT NULL,
  `wydarzenie_nazwa_id` varchar(100) NOT NULL,
  `wydarzenie_data_rozpoczecia_id` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;;

--
-- Zrzut danych tabeli `museum_app_wydarzenie_oddzial`
--

INSERT INTO `museum_app_wydarzenie_oddzial` (`oddzial_nazwa_id`, `wydarzenie_nazwa_id`, `wydarzenie_data_rozpoczecia_id`) VALUES
('muzeum narodowe w poznaniu', 'dzien seniora', '2021-01-30'),
('muzeum narodowe w warszawie', 'dzien seniora', '2021-01-30'),
('muzeum narodowe w poznaniu', 'noc w muzeum', '2021-02-19'),
('muzeum narodowe w warszawie', 'wystawa prac studentow', '2021-06-01');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `museum_app_artysta`
--
ALTER TABLE `museum_app_artysta`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `museum_app_bilet`
--
ALTER TABLE `museum_app_bilet`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bilet_rodzaj_biletu` (`rodzaj_biletu_typ_id`,`rodzaj_biletu_czy_z_przewodnikiem_id`,`rodzaj_biletu_oddzial_nazwa_id`),
  ADD KEY `bilet_harmonogram_zwiedzania_FK` (`harmonogram_zwiedzania_id_id`) USING BTREE;

--
-- Indeksy dla tabeli `museum_app_dzial`
--
ALTER TABLE `museum_app_dzial`
  ADD PRIMARY KEY (`nazwa`,`oddzial_nazwa_id`) USING BTREE,
  ADD KEY `dzial_oddzial_fk` (`oddzial_nazwa_id`);

--
-- Indeksy dla tabeli `museum_app_harmonogram_zwiedzania`
--
ALTER TABLE `museum_app_harmonogram_zwiedzania`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY (`data`,`godzina_rozpoczecia`,`pracownik_pesel_id`),
  ADD KEY `harmonogram_zwiedzania_pracownik_FK` (`pracownik_pesel_id`);

--
-- Indeksy dla tabeli `museum_app_obraz`
--
ALTER TABLE `museum_app_obraz`
  ADD PRIMARY KEY (`id`),
  ADD KEY `obraz_dzial_FK` (`dzial_nazwa_id`,`dzial_oddzial_nazwa_id`) USING BTREE,
  ADD KEY `obraz_artysta_FK` (`artysta_id_id`);

--
-- Indeksy dla tabeli `museum_app_oddzial`
--
ALTER TABLE `museum_app_oddzial`
  ADD PRIMARY KEY (`nazwa`);

--
-- Indeksy dla tabeli `museum_app_pracownik`
--
ALTER TABLE `museum_app_pracownik`
  ADD PRIMARY KEY (`pesel`),
  ADD KEY `pracownik_oddzial_FK` (`oddzial_nazwa_id`);

--
-- Indeksy dla tabeli `museum_app_rodzaj_biletu`
--
ALTER TABLE `museum_app_rodzaj_biletu`
  ADD PRIMARY KEY (`typ`,`czy_z_przewodnikiem`,`oddzial_nazwa_id`) USING BTREE,
  ADD KEY `rodzaj_biletu_oddzial_FK` (`oddzial_nazwa_id`);

--
-- Indeksy dla tabeli `museum_app_rzezba`
--
ALTER TABLE `museum_app_rzezba`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rzezba_dzial_FK` (`dzial_nazwa_id`,`dzial_oddzial_nazwa_id`),
  ADD KEY `rzezba_artysta_FK` (`artysta_id_id`);

--
-- Indeksy dla tabeli `museum_app_wydarzenie`
--
ALTER TABLE `museum_app_wydarzenie`
  ADD PRIMARY KEY (`nazwa`,`data_rozpoczecia`);

--
-- Indeksy dla tabeli `museum_app_wydarzenie_oddzial`
--
ALTER TABLE `museum_app_wydarzenie_oddzial`
  ADD PRIMARY KEY (`oddzial_nazwa_id`,`wydarzenie_data_rozpoczecia_id`,`wydarzenie_nazwa_id`),
  ADD KEY `wydarzenie_FK` (`wydarzenie_nazwa_id`,`wydarzenie_data_rozpoczecia_id`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `museum_app_artysta`
--
ALTER TABLE `museum_app_artysta`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT dla tabeli `museum_app_bilet`
--
ALTER TABLE `museum_app_bilet`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT dla tabeli `museum_app_obraz`
--
ALTER TABLE `museum_app_obraz`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT dla tabeli `museum_app_rzezba`
--
ALTER TABLE `museum_app_rzezba`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `museum_app_bilet`
--
ALTER TABLE `museum_app_bilet`
  ADD CONSTRAINT `bilet_harmonogram_zwiedzania_FK` FOREIGN KEY (`harmonogram_zwiedzania_id_id`) REFERENCES `museum_app_harmonogram_zwiedzania` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `bilet_rodzaj_biletu` FOREIGN KEY (`rodzaj_biletu_typ_id`,`rodzaj_biletu_czy_z_przewodnikiem_id`,`rodzaj_biletu_oddzial_nazwa_id`) REFERENCES `museum_app_rodzaj_biletu` (`typ`, `czy_z_przewodnikiem`, `oddzial_nazwa_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `museum_app_dzial`
--
ALTER TABLE `museum_app_dzial`
  ADD CONSTRAINT `dzial_oddzial_fk` FOREIGN KEY (`oddzial_nazwa_id`) REFERENCES `museum_app_oddzial` (`nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `museum_app_harmonogram_zwiedzania`
--
ALTER TABLE `museum_app_harmonogram_zwiedzania`
  ADD CONSTRAINT `harmonogram_zwiedzania_pracownik_FK` FOREIGN KEY (`pracownik_pesel_id`) REFERENCES `museum_app_pracownik` (`pesel`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `museum_app_obraz`
--
ALTER TABLE `museum_app_obraz`
  ADD CONSTRAINT `obraz_artysta_FK` FOREIGN KEY (`artysta_id_id`) REFERENCES `museum_app_artysta` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `obraz_oddzial_FK` FOREIGN KEY (`dzial_nazwa_id`,`dzial_oddzial_nazwa_id`) REFERENCES `museum_app_dzial` (`nazwa`, `oddzial_nazwa_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `museum_app_pracownik`
--
ALTER TABLE `museum_app_pracownik`
  ADD CONSTRAINT `pracownik_oddzial_FK` FOREIGN KEY (`oddzial_nazwa_id`) REFERENCES `museum_app_oddzial` (`nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `museum_app_rodzaj_biletu`
--
ALTER TABLE `museum_app_rodzaj_biletu`
  ADD CONSTRAINT `rodzaj_biletu_oddzial_FK` FOREIGN KEY (`oddzial_nazwa_id`) REFERENCES `museum_app_oddzial` (`nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `museum_app_rzezba`
--
ALTER TABLE `museum_app_rzezba`
  ADD CONSTRAINT `rzezba_artysta_FK` FOREIGN KEY (`artysta_id_id`) REFERENCES `museum_app_artysta` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `rzezba_dzial_FK` FOREIGN KEY (`dzial_nazwa_id`,`dzial_oddzial_nazwa_id`) REFERENCES `museum_app_dzial` (`nazwa`, `oddzial_nazwa_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Ograniczenia dla tabeli `museum_app_wydarzenie_oddzial`
--
ALTER TABLE `museum_app_wydarzenie_oddzial`
  ADD CONSTRAINT `oddzial_FK` FOREIGN KEY (`oddzial_nazwa_id`) REFERENCES `museum_app_oddzial` (`nazwa`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `wydarzenie_FK` FOREIGN KEY (`wydarzenie_nazwa_id`,`wydarzenie_data_rozpoczecia_id`) REFERENCES `museum_app_wydarzenie` (`nazwa`, `data_rozpoczecia`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
