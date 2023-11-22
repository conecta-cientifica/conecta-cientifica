import mysql.connector
from accounts.lattes.queryerror import QueryException

class DataBaseConn():
    def __init__(self):
        self.conn = mysql.connector.connect(
               host='18.188.240.61',
                database='myslqserver_secundario',
                user='admin',
                password='12345678',
                port=3306
            )
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