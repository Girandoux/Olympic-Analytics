-- =====================================================
-- DATABASE: Olympic Analytics
-- Beschreibung:
-- Dieses Skript erstellt das komplette relationale
-- Datenmodell für die Analyse olympischer Spiele.
--
-- Das Modell basiert auf einem Star Schema mit:
-- - Dimensionstabellen
-- - Faktentabelle
-- - Primär- und Fremdschlüsseln
-- =====================================================


-- =====================================================
-- OPTIONAL:
-- Alte Tabellen löschen
-- Nur verwenden falls Tabellen bereits existieren
-- =====================================================

DROP TABLE IF EXISTS fact_participations CASCADE;
DROP TABLE IF EXISTS dim_events CASCADE;
DROP TABLE IF EXISTS dim_athletes CASCADE;
DROP TABLE IF EXISTS dim_countries CASCADE;
DROP TABLE IF EXISTS dim_sports CASCADE;
DROP TABLE IF EXISTS dim_medals CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;

DROP TYPE IF EXISTS medal_enum;


-- =====================================================
-- ENUM TYPE: MEDAILLEN
-- Erlaubt nur gültige Medaillenwerte
-- =====================================================

CREATE TYPE medal_enum AS ENUM
(
    'Gold',
    'Silver',
    'Bronze',
    'No Medal'
);


-- =====================================================
-- DIMENSION TABLE: ATHLETES
-- Stammdaten der Athleten
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_athletes
(
    athlete_id INT PRIMARY KEY,

    name TEXT NOT NULL,

    sex CHAR(1)
);


-- =====================================================
-- DIMENSION TABLE: COUNTRIES
-- Länderinformationen
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_countries
(
    country_id SERIAL PRIMARY KEY,

    country_name TEXT NOT NULL,

    noc CHAR(3) UNIQUE
);


-- =====================================================
-- DIMENSION TABLE: SPORTS
-- Olympische Sportarten
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_sports
(
    sport_id SERIAL PRIMARY KEY,

    sport_name TEXT UNIQUE NOT NULL
);


-- =====================================================
-- DIMENSION TABLE: MEDALS
-- Medaillenarten
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_medals
(
    medal_id SERIAL PRIMARY KEY,

    medal_type medal_enum UNIQUE NOT NULL
);


-- =====================================================
-- DIMENSION TABLE: DATE
-- Zeitdimension für historische Analysen
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_date
(
    date_id SERIAL PRIMARY KEY,

    date DATE,

    year INT NOT NULL
);


-- =====================================================
-- DIMENSION TABLE: EVENTS
-- Olympische Wettbewerbe
-- Jedes Event gehört zu genau einer Sportart
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_events
(
    event_id SERIAL PRIMARY KEY,

    event_name TEXT UNIQUE NOT NULL,

    sport_id INT NOT NULL,

    -- ================================================
    -- FOREIGN KEY:
    -- Verknüpfung zur Sportart
    -- ================================================

    CONSTRAINT fk_sport
        FOREIGN KEY (sport_id)
        REFERENCES dim_sports(sport_id)
);


-- =====================================================
-- FACT TABLE: PARTICIPATIONS
-- Zentrale Faktentabelle
-- Enthält jede olympische Teilnahme
-- =====================================================

CREATE TABLE IF NOT EXISTS fact_participations
(
    participations_id SERIAL PRIMARY KEY,

    athlete_id INT NOT NULL,

    country_id INT NOT NULL,

    event_id INT NOT NULL,

    medal_id INT NOT NULL,

    date_id INT NOT NULL,

    -- ================================================
    -- Dynamische Athletenwerte
    -- Können sich über die Jahre verändern
    -- ================================================

    age INT,

    height_cm INT,

    weight_kg INT,

    -- ================================================
    -- FOREIGN KEYS
    -- ================================================

    CONSTRAINT fk_athlete
        FOREIGN KEY (athlete_id)
        REFERENCES dim_athletes(athlete_id),

    CONSTRAINT fk_country
        FOREIGN KEY (country_id)
        REFERENCES dim_countries(country_id),

    CONSTRAINT fk_event
        FOREIGN KEY (event_id)
        REFERENCES dim_events(event_id),

    CONSTRAINT fk_medal
        FOREIGN KEY (medal_id)
        REFERENCES dim_medals(medal_id),

    CONSTRAINT fk_date
        FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);