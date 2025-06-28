import pyodbc
from util.DBPropertyUtil import DBPropertyUtil

class DBConnUtil:
    @staticmethod
    def get_connection(file_name='db.properties'):
        try:
            conn_str = DBPropertyUtil.get_connection_string(file_name)
            if conn_str:
                conn = pyodbc.connect(conn_str)
                return conn
            else:
                raise Exception("Connection string not found.")
        except Exception as e:
            print("Database connection error:", e)
            return None
