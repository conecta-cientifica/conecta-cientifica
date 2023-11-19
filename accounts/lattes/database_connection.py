# import mysql.connector
import psycopg2
import os
from accounts.lattes.queryerror import QueryException

class DataBaseConn():
    def __init__(self):
        database_url = os.getenv('DATABASE_URL', 'postgres://conecta_cientifica_db_user:NCOexua0Ys81F4z6h9CaX4BKeR69Aw9V@dpg-clbqjcmg1b2c73eovte0-a.ohio-postgres.render.com/conecta_cientifica_db')
        self.conn = psycopg2.connect(database_url)
    def __del__(self):
        self.conn.close()
    
    def execute_query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except:
            raise(QueryException)
