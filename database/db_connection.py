import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "123@123",
            database = "carem_db"
        )
        return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None 