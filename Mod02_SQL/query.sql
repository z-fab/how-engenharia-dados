-- CREATE TABLE BILLBOARD

CREATE TABLE public."Billboard" (
	"date" DATE NULL,
	"rank" INT4 NULL,
	song VARCHAR(300) NULL,
	artist VARCHAR(300) NULL,
	"last-week" INT4 NULL,
	"peak-rank" INT4 NULL,
	"weeks-on-board" INT4 NULLl
);


SELECT
	COUNT(*) AS quantidade
FROM
	public."Billboard";

	
SELECT
	t1."date",
	t1."rank",
	t1.song,
	t1.artist,
	t1."last-week",
	t1."peak-rank",
	t1."weeks-on-board"
FROM
	public."Billboard" AS t1
LIMIT 100;


SELECT
	t1.song,
	t1.artist
FROM
	public."Billboard" AS t1
WHERE 
	t1.artist = 'Adele'
;



SELECT
	t1.artist,
	t1.song,
	COUNT(*) AS "#song"
FROM
	public."Billboard" AS t1
WHERE 
	-- t1.artist = 'Adele' OR t1.artist = 'Lady Gaga'
	t1.artist IN('Adele', 'Lady Gaga', 'Beyonce')
GROUP BY t1.artist, t1.song
ORDER BY "#song" DESC
;

----------------------
--       CTE        --
----------------------

SELECT DISTINCT
	t1.artist,
	t1.song
FROM
	public."Billboard" AS t1
ORDER BY t1.artist, t1.song
;


SELECT
	t1.artist,
	COUNT(*) AS "#artist"
FROM
	public."Billboard" AS t1
GROUP BY t1.artist
ORDER BY t1.artist
;


SELECT
	t1.song,
	COUNT(*) AS "#song"
FROM
	public."Billboard" AS t1
GROUP BY t1.song
ORDER BY t1.song
;



SELECT DISTINCT
	t1.artist,
	t2."#artist",
	t1.song,
	t3."#song"
FROM public."Billboard" AS t1
LEFT JOIN (
	SELECT
		t1.artist,
		COUNT(*) AS "#artist"
	FROM
		public."Billboard" AS t1
	GROUP BY t1.artist
) AS t2 ON t1.artist = t2.artist
LEFT JOIN (
	SELECT
		t1.song,
		COUNT(*) AS "#song"
	FROM
		public."Billboard" AS t1
	GROUP BY t1.song
) AS t3 ON t1.song = t3.song
ORDER BY "#artist" DESC, "#song" DESC
;


WITH cte_artist AS (
	SELECT
		t1.artist,
		COUNT(*) AS "#artist"
	FROM
		public."Billboard" AS t1
	GROUP BY t1.artist
),

cte_song AS (
	SELECT
		t1.song,
		COUNT(*) AS "#song"
	FROM
		public."Billboard" AS t1
	GROUP BY t1.song
)

SELECT DISTINCT
	t1.artist,
	t2."#artist",
	t1.song,
	t3."#song"
FROM public."Billboard" AS t1
LEFT JOIN cte_artist AS t2 ON t1.artist = t2.artist
LEFT JOIN cte_song AS t3 ON t1.song = t3.song
ORDER BY "#artist" DESC, "#song" DESC
;

-----------------------
--  WINDOW FUNCTION  --
-----------------------

WITH cte_billboard AS (
	SELECT DISTINCT
		t1.artist,
		t1.song,
		ROW_NUMBER() OVER(ORDER BY artist, song) AS "row_number",
		ROW_NUMBER() OVER(PARTITION BY artist ORDER BY artist, song) AS "row_number_artist"
	FROM
		public."Billboard" AS t1
	ORDER BY t1.artist, t1.song
)
SELECT *
FROM cte_billboard
WHERE "row_number_artist" = 1
;


WITH cte_billboard AS (
	SELECT DISTINCT
		t1.artist,
		t1.song
	FROM
		public."Billboard" AS t1
	ORDER BY t1.artist, t1.song
)
SELECT *,
	ROW_NUMBER() OVER(ORDER BY artist, song) AS "row_number",
	RANK() OVER(PARTITION BY artist ORDER BY artist, song) AS "rank",
	LAG(song, 1) OVER(PARTITION BY artist ORDER BY artist, song) AS "lag",
	LEAD(song, 1) OVER(PARTITION BY artist ORDER BY artist, song) AS "lead",
	FIRST_VALUE(song) OVER(PARTITION BY artist ORDER BY artist, song) AS "first_value",
	LAST_VALUE(song) OVER(PARTITION BY artist ORDER BY artist, song RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS "last_value"
FROM cte_billboard
;


------------------------
-- DEDUPLICANDO DADOS --
------------------------

CREATE TABLE tb_website AS(
	WITH cte_dedup_artist AS (
		SELECT
			t1."date",
			t1."rank",
			t1.artist,
			ROW_NUMBER() OVER(PARTITION BY t1.artist ORDER BY t1.artist, t1."date") AS dedup
		FROM
			public."Billboard" AS t1
		ORDER BY t1.artist, t1."date"
	)
	SELECT 
		t1."date",
		t1."rank",
		t1.artist
	FROM cte_dedup_artist AS t1
	WHERE t1.dedup = 1
)
;

SELECT * FROM public.tb_website;

CREATE TABLE tb_artist AS (
	SELECT
		t1."date",
		t1."rank",
		t1.artist,
		t1.song
	FROM
		public."Billboard" AS t1
	WHERE
		t1.artist = 'Adele'
	ORDER BY t1."date"
);

SELECT * FROM public.tb_artist;

CREATE VIEW vw_artist AS (
	WITH cte_dedup_artist AS (
		SELECT
			t1."date",
			t1."rank",
			t1.artist,
			ROW_NUMBER() OVER(PARTITION BY t1.artist ORDER BY t1.artist, t1."date") AS dedup
		FROM
			public.tb_artist AS t1
		ORDER BY t1.artist, t1."date"
	)
	SELECT 
		t1."date",
		t1."rank",
		t1.artist
	FROM cte_dedup_artist AS t1
	WHERE t1.dedup = 1
);

SELECT * FROM vw_artist;

INSERT INTO tb_artist (
	SELECT
		t1."date",
		t1."rank",
		t1.artist,
		t1.song
	FROM
		public."Billboard" AS t1
	WHERE
		t1.artist like 'Lady%'
	ORDER BY t1."date"
);

CREATE VIEW vw_song AS (
	WITH cte_dedup_artist AS (
		SELECT
			t1."date",
			t1."rank",
			t1.artist,
			t1.song,
			ROW_NUMBER() OVER(PARTITION BY t1.artist, t1.song ORDER BY t1.artist, t1.song, t1."date") AS dedup
		FROM
			public.tb_artist AS t1
		ORDER BY t1.artist, t1.song, t1."date"
	)
	SELECT 
		t1."date",
		t1."rank",
		t1.artist,
		t1.song
	FROM cte_dedup_artist AS t1
	WHERE t1.dedup = 1
);

SELECT * FROM vw_song;
