-- =====================================================================================
-- KPI DASHBOARD - OLYMPIC ANALYTICS
-- Dieses Skript berechnet zentrale KPIs
-- sowohl insgesamt als auch pro Jahr.
-- =====================================================================================



-- =====================================================================================
-- KPI 1: ANZAHL ATHLETEN (GESAMT)
-- Wie viele unterschiedliche Athleten existieren?
-- =====================================================================================

SELECT
    COUNT(DISTINCT athlete_id) AS total_athletes
FROM dim_athletes;



-- =====================================================================================
-- KPI 2: ANZAHL ATHLETEN PRO JAHR
-- Wie viele Athleten nahmen pro Jahr teil?
-- =====================================================================================

SELECT
    d.year,

    COUNT(DISTINCT fp.athlete_id) AS athletes_per_year

FROM fact_participations fp

JOIN dim_date d
    ON fp.date_id = d.date_id

GROUP BY d.year

ORDER BY d.year;



-- =====================================================================================
-- KPI 3: TOTAL MEDALS (GESAMT)
-- Anzahl aller gewonnenen Medaillen
-- "No Medal" wird ausgeschlossen
-- =====================================================================================

SELECT
    COUNT(*) AS total_medals

FROM fact_participations fp

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

WHERE m.medal_type <> 'No Medal';



-- =====================================================================================
-- KPI 4: TOTAL MEDALS PRO JAHR
-- Wie viele Medaillen wurden pro Jahr vergeben?
-- =====================================================================================

SELECT
    d.year,

    COUNT(*) AS medals_per_year

FROM fact_participations fp

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

JOIN dim_date d
    ON fp.date_id = d.date_id

WHERE m.medal_type <> 'No Medal'

GROUP BY d.year

ORDER BY d.year;



-- =====================================================================================
-- KPI 5: TOTAL COUNTRIES (GESAMT)
-- Anzahl aller teilnehmenden Länder
-- =====================================================================================

SELECT
    COUNT(DISTINCT country_id) AS total_countries
FROM dim_countries;



-- =====================================================================================
-- KPI 6: TOTAL COUNTRIES PRO JAHR
-- Wie viele Länder nahmen pro Jahr teil?
-- =====================================================================================

SELECT
    d.year,

    COUNT(DISTINCT fp.country_id) AS countries_per_year

FROM fact_participations fp

JOIN dim_date d
    ON fp.date_id = d.date_id

GROUP BY d.year

ORDER BY d.year;



-- =====================================================================================
-- KPI 7: DURCHSCHNITTSALTER ALLER ATHLETEN
-- =====================================================================================

SELECT
    ROUND(AVG(age), 2) AS average_athlete_age
FROM fact_participations;



-- =====================================================================================
-- KPI 8: DURCHSCHNITTSALTER PRO JAHR
-- =====================================================================================

SELECT
    d.year,

    ROUND(AVG(fp.age), 2) AS average_age_per_year

FROM fact_participations fp

JOIN dim_date d
    ON fp.date_id = d.date_id

GROUP BY d.year

ORDER BY d.year;



-- =====================================================================================
-- KPI 9: GOLD MEDAL RATIO (GESAMT)
-- Anteil der Goldmedaillen an allen Medaillen
-- =====================================================================================

SELECT

    ROUND(
        COUNT(
            CASE
                WHEN m.medal_type = 'Gold'
                THEN 1
            END
        ) * 100.0
        /
        COUNT(
            CASE
                WHEN m.medal_type <> 'No Medal'
                THEN 1
            END
        ),
        2
    ) AS gold_medal_ratio_percent

FROM fact_participations fp

JOIN dim_medals m
    ON fp.medal_id = m.medal_id;



-- =====================================================================================
-- KPI 10: GOLD MEDAL RATIO PRO JAHR
-- =====================================================================================

SELECT
    d.year,

    ROUND(
        COUNT(
            CASE
                WHEN m.medal_type = 'Gold'
                THEN 1
            END
        ) * 100.0
        /
        COUNT(
            CASE
                WHEN m.medal_type <> 'No Medal'
                THEN 1
            END
        ),
        2
    ) AS gold_medal_ratio_percent

FROM fact_participations fp

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

JOIN dim_date d
    ON fp.date_id = d.date_id

GROUP BY d.year

ORDER BY d.year;



-- =====================================================================================
-- KPI 11: PARTICIPATION GROWTH
-- Entwicklung der Teilnahmen über die Jahre
-- =====================================================================================

SELECT
    d.year,

    COUNT(fp.participations_id) AS total_participations

FROM fact_participations fp

JOIN dim_date d
    ON fp.date_id = d.date_id

GROUP BY d.year

ORDER BY d.year;



-- =====================================================================================
-- KPI 12: GESAMTANZAHL TEILNAHMEN
-- =====================================================================================

SELECT
    COUNT(*) AS total_participations
FROM fact_participations;



-- =====================================================================================
-- KPI 13: ALTER DER GEWINNER (GESAMT)
-- Durchschnittsalter aller Medaillengewinner
-- =====================================================================================

SELECT

    ROUND(AVG(fp.age), 2) AS average_winner_age

FROM fact_participations fp

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

WHERE m.medal_type <> 'No Medal';



-- =====================================================================================
-- KPI 14: ALTER DER GEWINNER PRO JAHR
-- =====================================================================================

SELECT
    d.year,

    ROUND(AVG(fp.age), 2) AS average_winner_age

FROM fact_participations fp

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

JOIN dim_date d
    ON fp.date_id = d.date_id

WHERE m.medal_type <> 'No Medal'

GROUP BY d.year

ORDER BY d.year;



-- =====================================================================================
-- KPI SUMMARY TABLE
-- Alle wichtigsten KPIs in EINER Tabelle
-- Sehr gut für Dashboard / Power BI
-- =====================================================================================

SELECT

    d.year,

    -- =================================================
    -- Anzahl Athleten
    -- =================================================

    COUNT(DISTINCT fp.athlete_id) AS total_athletes,

    -- =================================================
    -- Anzahl Länder
    -- =================================================

    COUNT(DISTINCT fp.country_id) AS total_countries,

    -- =================================================
    -- Anzahl Teilnahmen
    -- =================================================

    COUNT(fp.participations_id) AS total_participations,

    -- =================================================
    -- Anzahl Medaillen
    -- =================================================

    COUNT(
        CASE
            WHEN m.medal_type <> 'No Medal'
            THEN 1
        END
    ) AS total_medals,

    -- =================================================
    -- Durchschnittsalter
    -- =================================================

    ROUND(AVG(fp.age), 2) AS average_athlete_age,

    -- =================================================
    -- Durchschnittsalter Gewinner
    -- =================================================

    ROUND(
        AVG(
            CASE
                WHEN m.medal_type <> 'No Medal'
                THEN fp.age
            END
        ),
        2
    ) AS average_winner_age,

    -- =================================================
    -- Gold Medal Ratio
    -- =================================================

    ROUND(
        COUNT(
            CASE
                WHEN m.medal_type = 'Gold'
                THEN 1
            END
        ) * 100.0
        /
        NULLIF(
            COUNT(
                CASE
                    WHEN m.medal_type <> 'No Medal'
                    THEN 1
                END
            ),
            0
        ),
        2
    ) AS gold_medal_ratio_percent

FROM fact_participations fp

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

JOIN dim_date d
    ON fp.date_id = d.date_id

GROUP BY d.year

ORDER BY d.year;


--------------------------------------------------------------------------------------------------------

-- =====================================================================================
-- FRAGESTELLUNG 1:
-- Leistungsdominanz von Ländern
-- Welche Länder dominieren bestimmte Sportarten über die Jahre?
-- =====================================================================================

SELECT
    c.country_name,
    s.sport_name,
    d.year,
    
    -- Anzahl gewonnener Medaillen
    COUNT(*) AS medal_count

FROM fact_participations fp

-- =========================================================
-- JOINS ZU DIMENSIONSTABELLEN
-- =========================================================

JOIN dim_countries c
    ON fp.country_id = c.country_id

JOIN dim_events e
    ON fp.event_id = e.event_id

JOIN dim_sports s
    ON e.sport_id = s.sport_id

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

JOIN dim_date d
    ON fp.date_id = d.date_id

-- =========================================================
-- Nur echte Medaillen zählen
-- "No Medal" ausschließen
-- =========================================================

WHERE m.medal_type <> 'No Medal'

-- =========================================================
-- Gruppierung
-- =========================================================

GROUP BY
    c.country_name,
    s.sport_name,
    d.year

-- =========================================================
-- Sortierung nach meisten Medaillen
-- =========================================================
ORDER BY year DESC, medal_count DESC, sport_name ASC;
-- ORDER BY medal_count DESC;


-- =====================================================================================
-- FRAGESTELLUNG 2:
-- Alters- und Körperprofil erfolgreicher Athleten
-- Gibt es typische Körperprofile pro Sportart?
-- =====================================================================================

SELECT
    s.sport_name,

    -- Durchschnittsalter erfolgreicher Athleten
    ROUND(AVG(fp.age), 2) AS avg_age_medalists,

    -- Durchschnittliche Körpergröße
    ROUND(AVG(fp.height_cm), 2) AS avg_height_cm,

    -- Durchschnittliches Gewicht
    ROUND(AVG(fp.weight_kg), 2) AS avg_weight_kg

FROM fact_participations fp

-- =========================================================
-- JOINS
-- =========================================================

JOIN dim_events e
    ON fp.event_id = e.event_id

JOIN dim_sports s
    ON e.sport_id = s.sport_id

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

-- =========================================================
-- Nur Medaillengewinner analysieren
-- =========================================================

WHERE m.medal_type <> 'No Medal'

-- =========================================================
-- Gruppierung nach Sportart
-- =========================================================

GROUP BY s.sport_name

ORDER BY avg_age_medalists;


-- =====================================================================================
-- FRAGESTELLUNG 3:
-- Geschlechteranalyse
-- Unterschiede zwischen Männern und Frauen
-- =====================================================================================

SELECT
    a.sex,

    -- Anzahl gewonnener Medaillen
    COUNT(
        CASE
            WHEN m.medal_type <> 'No Medal'
            THEN 1
        END
    ) AS medal_count,

    -- Gesamtanzahl Teilnahmen
    COUNT(fp.participations_id) AS total_participations,

    -- Erfolgsquote
    ROUND(
        COUNT(
            CASE
                WHEN m.medal_type <> 'No Medal'
                THEN 1
            END
        ) * 1.0
        /
        COUNT(fp.participations_id),
        2
    ) AS medal_rate

FROM fact_participations fp

-- =========================================================
-- JOINS
-- =========================================================

JOIN dim_athletes a
    ON fp.athlete_id = a.athlete_id

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

-- =========================================================
-- Gruppierung nach Geschlecht
-- =========================================================

GROUP BY a.sex;


-- =====================================================================================
-- FRAGESTELLUNG 4:
-- Zeitliche Entwicklung
-- Veränderung von Altersprofilen über die Jahre
-- =====================================================================================

SELECT
    d.year,

    -- Durchschnittsalter der Medaillengewinner
    ROUND(AVG(fp.age), 2) AS avg_age_medalists

FROM fact_participations fp

-- =========================================================
-- JOINS
-- =========================================================

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

JOIN dim_date d
    ON fp.date_id = d.date_id

-- =========================================================
-- Nur Medaillengewinner
-- =========================================================

WHERE m.medal_type <> 'No Medal'

-- =========================================================
-- Gruppierung nach Jahr
-- =========================================================

GROUP BY d.year

ORDER BY d.year;


-- =====================================================================================
-- VIEW FÜR PYTHON / PANDAS ANALYSE
-- Vereinfachte Analyse-Tabelle
-- =====================================================================================

CREATE OR REPLACE VIEW olympics_analysis AS

SELECT

    -- =====================================================
    -- Faktentabelle
    -- =====================================================

    fp.participations_id,

    fp.age,

    fp.height_cm,

    fp.weight_kg,

    -- =====================================================
    -- Athleteninformationen
    -- =====================================================

    a.athlete_id,

    a.name,

    a.sex AS gender,

    -- =====================================================
    -- Länderinformationen
    -- =====================================================

    c.noc,

    c.country_name,

    -- =====================================================
    -- Sportinformationen
    -- =====================================================

    s.sport_name,

    e.event_name,

    -- =====================================================
    -- Zeitinformationen
    -- =====================================================

    d.date,

    d.year,

    -- =====================================================
    -- Medailleninformationen
    -- =====================================================

    m.medal_type

FROM fact_participations fp

-- =========================================================
-- JOINS
-- =========================================================

JOIN dim_athletes a
    ON fp.athlete_id = a.athlete_id

JOIN dim_countries c
    ON fp.country_id = c.country_id

JOIN dim_events e
    ON fp.event_id = e.event_id

JOIN dim_sports s
    ON e.sport_id = s.sport_id

JOIN dim_medals m
    ON fp.medal_id = m.medal_id

JOIN dim_date d
    ON fp.date_id = d.date_id

-- =========================================================
-- Sortierung
-- =========================================================

ORDER BY c.country_name DESC;


-- =====================================================================================
-- DATENBEREINIGUNG
-- =====================================================================================


-- =====================================================================================
-- Lösche fehlerhafte Länderwerte:
-- noc = 'UNK'
-- country_name IS NULL
-- =====================================================================================

DELETE FROM dim_countries

WHERE noc = 'UNK'
AND country_name IS NULL;


-- =====================================================================================
-- Fehlende Länderwerte ergänzen:
-- ROT -> Romania Team
-- =====================================================================================

UPDATE dim_countries

SET country_name = 'Romania Team'

WHERE noc = 'ROT'
AND country_name IS NULL;


-- =====================================================================================
-- Fehlende Länderwerte ergänzen:
-- TUV -> Tuvalu
-- =====================================================================================

UPDATE dim_countries

SET country_name = 'Tuvalu'

WHERE noc = 'TUV'
AND country_name IS NULL;



SELECT *
FROM olympics_analysis