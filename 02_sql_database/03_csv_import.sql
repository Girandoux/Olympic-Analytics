-- =====================================================
-- COPY: DIM_ATHLETES
-- Importiert Athleteninformationen
-- =====================================================

COPY dim_athletes(athlete_id, name, sex)

FROM 'C:\Program Files\PostgreSQL\17\data\import\dim_athletes.csv'

WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ';',
    QUOTE '"'
);


-- =====================================================
-- COPY: DIM_COUNTRIES
-- Importiert Länderinformationen
-- =====================================================

COPY dim_countries(country_id, country_name, noc)

FROM 'C:\Program Files\PostgreSQL\17\data\import\dim_countries.csv'

WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ';',
    QUOTE '"'
);


-- =====================================================
-- COPY: DIM_SPORTS
-- Importiert olympische Sportarten
-- =====================================================

COPY dim_sports(sport_id, sport_name)

FROM 'C:\Program Files\PostgreSQL\17\data\import\dim_sports.csv'

WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ';',
    QUOTE '"'
);


-- =====================================================
-- COPY: DIM_MEDALS
-- Importiert Medaillentypen
-- =====================================================

COPY dim_medals(medal_id, medal_type)

FROM 'C:\Program Files\PostgreSQL\17\data\import\dim_medals.csv'

WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ';',
    QUOTE '"'
);


-- =====================================================
-- COPY: DIM_DATE
-- Importiert Zeitdimension
-- =====================================================

COPY dim_date(date_id, date, year)

FROM 'C:\Program Files\PostgreSQL\17\data\import\dim_date.csv'

WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ';',
    QUOTE '"'
);


-- =====================================================
-- COPY: DIM_EVENTS
-- Importiert olympische Wettbewerbe
-- =====================================================

COPY dim_events(event_id, event_name, sport_id)

FROM 'C:\Program Files\PostgreSQL\17\data\import\dim_events.csv'

WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ';',
    QUOTE '"'
);


-- =====================================================
-- COPY: FACT_PARTICIPATIONS
-- Importiert olympische Teilnahmen
-- =====================================================

COPY fact_participations
(
    participations_id,
    athlete_id,
    country_id,
	medal_id,
    event_id,
    date_id,
    age,
    height_cm,
    weight_kg
)

FROM 'C:\Program Files\PostgreSQL\17\data\import\fact_participations.csv'

WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ';',
    QUOTE '"'
);