from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql+psycopg2://root:root@localhost:5432/test_db')

sql = '''
    SELECT * FROM vw_artist;
'''

