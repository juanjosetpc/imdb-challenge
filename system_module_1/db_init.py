import os
import mysql.connector
from mysql.connector import Error
from utils.logger import get_logger

logger = get_logger("db_init")

def create_database_if_not_exists():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            port=int(os.getenv("DB_PORT", 3306)),
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS imdb_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        logger.info("Database 'imdb_db' checked/created.")
    except Error as e:
        logger.error(f"Error creating database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def create_tables():
    from config.db_config import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, "models", "schema.sql")

    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    for stmt in sql.strip().split(";"):
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt + ";")

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Tables created (or already existed).")
    
if __name__ == "__main__":
    create_database_if_not_exists()
    create_tables()
    logger.info("DB initialization finished.")
