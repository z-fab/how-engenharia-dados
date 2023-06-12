from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine('postgresql+psycopg2://root:root@localhost:5432/test_db')

sql = '''
    SELECT * FROM vw_artist;
'''

df = pd.read_sql(sql, engine)

df2 = pd.read_sql('SELECT * FROM vw_song', engine)

sql_insert = '''
INSERT INTO tb_artist (
	SELECT
		t1."date",
		t1."rank",
		t1.artist,
		t1.song
	FROM
		public."Billboard" AS t1
	WHERE
		t1.artist like 'Beyonce'
	ORDER BY t1."date"
);
'''

with engine.connect() as con:
    con.execute(text(sql_insert))
    con.commit()