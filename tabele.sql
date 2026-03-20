/* Tabela 1a */
CREATE TABLE IF NOT EXISTS panstwa( 
    id_panstwa INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    panstwo VARCHAR(40)
)

/* Tabela 1b */
CREATE TABLE IF NOT EXISTS miasta( 
    id_miasta INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    miasto VARCHAR(40),
    kod_pocztowy VARCHAR(10),
    id_panstwa INT UNSIGNED,
    FOREIGN KEY odw_panstwo (id_panstwa) REFERENCES panstwa(id_panstwa) ON UPDATE CASCADE
)

/* Tabela 1c */
CREATE TABLE IF NOT EXISTS pracownicy( 
    id_pracownika INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    imie VARCHAR(40) NOT NULL,
    nazwisko VARCHAR(40) NOT NULL,
    nr_telefonu VARCHAR(30),
    ulica VARCHAR(30),
    nr_domu VARCHAR(10),
    nr_mieszkania INT UNSIGNED,
    id_miasta INT UNSIGNED NOT NULL,
    data_zatrudnienia DATE NOT NULL,
    data_zwolnienia DATE DEFAULT NULL,
    wynagrodzenie INT UNSIGNED,
    FOREIGN KEY odw_miasto (id_miasta) REFERENCES miasta(id_miasta) ON UPDATE CASCADE
)

/* Tabela 2 */
CREATE TABLE IF NOT EXISTS sponsorzy( 
    id_sponsora INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nazwa_firmy VARCHAR(40) NOT NULL,
    oferta TEXT,
    data_podpisania_umowy DATE,
    data_zakonczenia_umowy DATE,
    nr_tel_reprezentanta INT UNSIGNED
)

/* Tabela 3 */
CREATE TABLE IF NOT EXISTS finansowanie(
    id_transakcji INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_sponsora INT UNSIGNED COMMENT "jeżeli inne źródło, to wartość NULL",
    zrodlo VARCHAR(40),
    data_transakcji DATE,
    kwota INT UNSIGNED,
    id_pracownika INT UNSIGNED,
    FOREIGN KEY odw_sponsor (id_sponsora) REFERENCES sponsorzy(id_sponsora) ON UPDATE CASCADE,
    FOREIGN KEY odw_pracownik (id_pracownika) REFERENCES pracownicy(id_pracownika) ON UPDATE CASCADE
)

/* Tabela 4a */
CREATE TABLE IF NOT EXISTS sportowcy(
    id_uczestnika INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_wlasciciela INT UNSIGNED,
    charakterystyka TEXT,
    data_urodzenia DATE,
    wartosc_wyposazenia INT DEFAULT 0 COMMENT "Cena sprzętu"
    aktywny BOOLEAN,
    FOREIGN KEY odw_wlasciciel (id_wlasciciela) REFERENCES sportowcy_wlasciciele(id_wlasciciela) ON UPDATE CASCADE
)

/* Tabela 4b */
CREATE TABLE IF NOT EXISTS sportowcy_wlasciciele(
    id_wlasciciela INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    imie VARCHAR(40),
    nazwisko VARCHAR(40),
)

/* Tabela 4c */
CREATE TABLE IF NOT EXISTS sportowcy_sponsorzy(
    id_uczestnika INT UNSIGNED,
    id_sponsora INT UNSIGNED,
    kwota INT UNSIGNED,
    data_transakcji DATE,
    PRIMARY KEY id_sportowiec_sponsor (id_uczestnika, id_sponsora, data_transakcji),
    FOREIGN KEY odw_uczestnik (id_uczestnika) REFERENCES sportowcy(id_uczestnika) ON UPDATE CASCADE,
    FOREIGN KEY odw_sponsor (id_sponsora) REFERENCES sponsorzy(id_sponsora) ON UPDATE CASCADE
)

/* Tabela 5a */
CREATE TABLE IF NOT EXISTS zawody( 
    id_zawodow INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_miasta INT UNSIGNED NOT NULL,
    data_zawodow DATE,
    liczba_widzow INT UNSIGNED DEFAULT 0,
    przychod INT DEFAULT 0,
    koszt_organizacji INT DEFAULT 0,
    FOREIGN KEY odw_miasto (id_miasta) REFERENCES miasta(id_miasta) ON UPDATE CASCADE
)

/* Tabela 5b */
CREATE TABLE IF NOT EXISTS zawody_uczestnicy(
    id_uczestnika INT UNSIGNED NOT NULL,
    id_zawodow INT UNSIGNED NOT NULL,
    PRIMARY KEY id_uczestnik_zawody (id_uczestnika, id_zawodow),
    FOREIGN KEY odw_uczestnik (id_uczestnika) REFERENCES sportowcy(id_uczestnika) ON UPDATE CASCADE,
    FOREIGN KEY odw_zawody (id_zawodow) REFERENCES zawody(id_zawodow) ON UPDATE CASCADE
)

/* Tabela 6a */
CREATE TABLE IF NOT EXISTS kontrole_antydopingowe(
    id_kontroli INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    data_kontroli DATE,
    wynik_kontroli VARCHAR(10) COMMENT "ogólny wynik kontroli, tzn. 'pozytywny'/'negatywny'"
)

/* Tabela 6b */
CREATE TABLE IF NOT EXISTS zdyskwalifikowani(
    id_uczestnika INT UNSIGNED NOT NULL,
    id_kontroli INT UNSIGNED NOT NULL,
    substancja VARCHAR(40),
    PRIMARY KEY id_uczestnik_kontrola (id_uczestnika, id_kontroli),
    FOREIGN KEY odw_uczestnik (id_uczestnika) REFERENCES sportowcy(id_uczestnika) ON UPDATE CASCADE,
    FOREIGN KEY odw_kontrola (id_kontroli) REFERENCES kontrole_antydopingowe(id_kontroli) ON UPDATE CASCADE
)

/* Tabela 7a */
CREATE TABLE IF NOT EXISTS konkurencje(
    id_konkurencji INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nazwa_konkurencji VARCHAR(100) NOT NULL,
    id_kategorii INT UNSIGNED NOT NULL,
    opis TEXT,
    FOREIGN KEY odw_kategoria (id_kategorii) REFERENCES kategorie(id_kategorii) ON UPDATE CASCADE
)

/* Tabela 7b */
CREATE TABLE IF NOT EXISTS konkurencje_zawody(
    id_konkurencji INT UNSIGNED NOT NULL,
    id_zawodow INT UNSIGNED NOT NULL,
    zwyciezca_konkurencji INT UNSIGNED COMMENT "id_uczestnika dla zwycięzcy",
    PRIMARY KEY id_konkurencja_zawody (id_konkurencji, id_zawodow),
    FOREIGN KEY odw_konkurencja (id_konkurencji) REFERENCES konkurencje(id_konkurencji) ON UPDATE CASCADE,
    FOREIGN KEY odw_zawody (id_zawodow) REFERENCES zawody(id_zawodow) ON UPDATE CASCADE,
    FOREIGN KEY odw_uczestnik (zwyciezca_konkurencji) REFERENCES sportowcy(id_uczestnika) ON UPDATE CASCADE
)

/* Tabela 7c */
CREATE TABLE IF NOT EXISTS konkurencje_uczestnicy(
    id_konkurencji INT UNSIGNED NOT NULL,
    id_uczestnika INT UNSIGNED NOT NULL,
    wynik_uczestnika INT UNSIGNED,
    PRIMARY KEY id_uczestnik_konkurencja (id_uczestnika, id_konkurencji),
    FOREIGN KEY odw_konkurencja (id_konkurencji) REFERENCES konkurencje(id_konkurencji) ON UPDATE CASCADE,
    FOREIGN KEY odw_uczestnik (id_uczestnika) REFERENCES sportowcy(id_uczestnika) ON UPDATE CASCADE
)

/* Tabela 8 */
CREATE TABLE IF NOT EXISTS kategorie (
    id_kategorii INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nazwa_kategorii VARCHAR(50) NOT NULL COMMENT "Naturalna lub formuła Ch",
    czy_wymaga_sprzetu BOOLEAN NOT NULL DEFAULT 0 COMMENT "0 - Naturalna, 1 - formuła Ch "
)

