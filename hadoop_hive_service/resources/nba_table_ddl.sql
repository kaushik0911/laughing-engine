CREATE TABLE game_events (
    EVENTID INT,
    EVENTNUM INT,
    GAME_ID INT,
    HOMEDESCRIPTION STRING,
    PCTIMESTRING STRING,
    PERIOD INT,
    PLAYER1_ID INT,
    PLAYER1_NAME STRING,
    PLAYER1_TEAM_ABBREVIATION STRING,
    PLAYER1_TEAM_CITY STRING,
    PLAYER1_TEAM_ID FLOAT,
    PLAYER1_TEAM_NICKNAME STRING,
    PLAYER2_ID INT,
    PLAYER2_NAME STRING,
    PLAYER2_TEAM_ABBREVIATION STRING,
    PLAYER2_TEAM_CITY STRING,
    PLAYER2_TEAM_ID FLOAT,
    PLAYER2_TEAM_NICKNAME STRING,
    PLAYER3_ID INT,
    PLAYER3_NAME STRING,
    PLAYER3_TEAM_ABBREVIATION STRING,
    PLAYER3_TEAM_CITY STRING,
    PLAYER3_TEAM_ID FLOAT,
    PLAYER3_TEAM_NICKNAME STRING,
    SCORE STRING,
    SCOREMARGIN STRING,
    VISITORDESCRIPTION STRING
) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE 
LOCATION 'hdfs://hive-namenode:8020/user/hive/warehouse/nba.db' 
TBLPROPERTIES ('skip.header.line.count'='1');


WITH game_scores AS (
SELECT
    GAME_ID,
    PLAYER1_TEAM_ABBREVIATION AS TEAM_ABBREVIATION,
    SPLIT(SCORE, ' - ')[0] AS SCORE_1,
    SPLIT(SCORE, ' - ')[1] AS SCORE_2,
FROM game_events
WHERE
    SCORE IS NOT NULL AND
    PLAYER1_TEAM_ABBREVIATION IS NOT NULL AND
    SCORE != '' AND
    PLAYER1_TEAM_ABBREVIATION != ''
GROUP BY GAME_ID, PLAYER1_TEAM_ABBREVIATION
)
SELECT
    GAME_ID,
    TEAM_ABBREVIATION,
    MAX(SCORE_1),
    MAX(SCORE_2)
FROM game_scores
GROUP BY GAME_ID, TEAM_ABBREVIATION



WITH
    game_scores AS (
        SELECT
            GAME_ID,
            PLAYER1_TEAM_ABBREVIATION AS TEAM_ABBREVIATION,
            CAST(SPLIT(SCORE, ' - ')[0] AS INT) AS VISITOR_SCORE,
            CAST(SPLIT(SCORE, ' - ')[1] AS INT) AS HOME_SCORE,
            CASE
                WHEN HOMEDESCRIPTION IS NOT NULL AND HOMEDESCRIPTION != '' THEN
                    CAST(SPLIT(SCORE, ' - ')[1] AS INT)
                WHEN VISITORDESCRIPTION IS NOT NULL AND VISITORDESCRIPTION != '' THEN
                    CAST(SPLIT(SCORE, ' - ')[0] AS INT)
                ELSE 0
            END AS TEAM_SCORE
        FROM game_events
        WHERE
            SCORE IS NOT NULL AND
            SCORE != '' AND
            PLAYER1_TEAM_ABBREVIATION IS NOT NULL AND
            PLAYER1_TEAM_ABBREVIATION != ''
    ),
    final_scores AS (
        SELECT GAME_ID, TEAM_ABBREVIATION, MAX(TEAM_SCORE) AS FINAL_SCORE
        FROM game_scores
        WHERE TEAM_SCORE > 0
        GROUP BY GAME_ID, TEAM_ABBREVIATION
    )
SELECT TEAM_ABBREVIATION, SUM(FINAL_SCORE) AS SCORE_SUM
FROM final_scores
GROUP BY TEAM_ABBREVIATION
ORDER BY SCORE_SUM DESC
LIMIT 5;


WITH game_scores AS (
    SELECT
        GAME_ID,
        PERIOD,
        CAST(SPLIT(SCORE, ' - ')[0] AS INT) AS VISITOR_SCORE,
        CAST(SPLIT(SCORE, ' - ')[1] AS INT) AS HOME_SCORE
    FROM 
        game_events
    WHERE
        SCORE IS NOT NULL AND
        SCORE != '' AND
        PLAYER1_TEAM_ABBREVIATION IS NOT NULL AND
        PLAYER1_TEAM_ABBREVIATION != '' AND
        GAME_ID = 20001116 AND
        PERIOD = 1
)
SELECT
    PERIOD,
    MAX(VISITOR_SCORE) AS MAX_VISITOR_SCORE,
    CASE
        WHEN PERIOD = 1 THEN 0
        ELSE MIN(VISITOR_SCORE)
    END AS MIN_VISITOR_SCORE,
    MAX(HOME_SCORE) AS MAX_HOME_SCORE,
    CASE
        WHEN PERIOD = 1 THEN 0
        ELSE MIN(HOME_SCORE)
    END AS MIN_HOME_SCORE
FROM game_scores
GROUP BY GAME_ID, PERIOD
















WITH game_scores AS (
    SELECT
        GAME_ID,
        PERIOD,
        CAST(SPLIT(SCORE, ' - ')[0] AS INT) AS VISITOR_SCORE,
        CAST(SPLIT(SCORE, ' - ')[1] AS INT) AS HOME_SCORE
    FROM 
        game_events
    WHERE
        SCORE IS NOT NULL AND
        SCORE != '' AND
        PLAYER1_TEAM_ABBREVIATION IS NOT NULL AND
        PLAYER1_TEAM_ABBREVIATION != '' AND
        PERIOD >= 4
),
adjusted_scores AS (
    SELECT
        GAME_ID,
        PERIOD,
        VISITOR_SCORE,
        HOME_SCORE,
        CASE
            WHEN PERIOD = 1 THEN 0
            ELSE VISITOR_SCORE
        END AS ADJUSTED_VISITOR_SCORE,
        CASE
            WHEN PERIOD = 1 THEN 0
            ELSE HOME_SCORE
        END AS ADJUSTED_HOME_SCORE
    FROM game_scores
),
period_min_max AS (
    SELECT
        GAME_ID,
        PERIOD,
        MAX(VISITOR_SCORE) AS MAX_VISITOR_SCORE,
        MIN(ADJUSTED_VISITOR_SCORE) AS MIN_VISITOR_SCORE,
        MAX(HOME_SCORE) AS MAX_HOME_SCORE,
        MIN(ADJUSTED_HOME_SCORE) AS MIN_HOME_SCORE
    FROM adjusted_scores
    GROUP BY GAME_ID, PERIOD
),
period_total AS (
    SELECT
        PERIOD,
        ((MAX_VISITOR_SCORE - MIN_VISITOR_SCORE) + (MAX_HOME_SCORE - MIN_HOME_SCORE)) AS TEAM_POINTS
    FROM period_min_max
)
SELECT PERIOD, ROUND(AVG(TEAM_POINTS)) AS AVG_POINTS
FROM period_total
GROUP BY PERIOD


