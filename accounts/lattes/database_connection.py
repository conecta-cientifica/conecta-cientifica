# import mysql.connector
import psycopg2
import os
from accounts.lattes.queryerror import QueryException

class DataBaseConn():
    def __init__(self):
        database_url = os.environ.get("DATABASE_URL")
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
