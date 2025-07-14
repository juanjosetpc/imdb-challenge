import os
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "imdb_db"),
            port=int(os.getenv("DB_PORT", 3306)),
            allow_local_infile=True,
            charset='utf8mb4'
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise
