import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from etl.extract import download_datasets
from etl.transform import read_tsv_gz, transform_films, transform_people
from config.db_config import get_db_connection
from db_init import create_database_if_not_exists, create_tables
from utils.logger import get_logger
from etl.load import DataLoader, BatchLoader, CSVLoader, UpdateLoader

logger = get_logger("main")
DATA_DIR = "data/imdb_downloads"

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)


def clean_tables():
    logger.info("Cleaning tables data")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute("TRUNCATE TABLE people_films;")
        cursor.execute("TRUNCATE TABLE people;")
        cursor.execute("TRUNCATE TABLE films;")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()
        logger.info("Tables cleaned")
    except Exception as e:
        logger.error(f"Error cleaning tables: {e}")
    finally:
        cursor.close()
        conn.close()


def main(action="reload", mode="batch"):
    create_database_if_not_exists()
    create_tables()

    if mode == "csv":
        loader = DataLoader(CSVLoader())
        logger.info("Using CSV load strategy")
    else:
        loader = DataLoader(BatchLoader(batch_size=15000)) 
        logger.info("Using Batch load strategy")

    if action == "clean":
        clean_tables()
        return

    if action == "reload":
        clean_tables()
        download_datasets(DATA_DIR)

        path_films = os.path.join(DATA_DIR, "title.basics.tsv.gz")
        df_films_raw = read_tsv_gz(path_films)
        df_films = transform_films(df_films_raw)
        loader.load(df_films, "films")

        path_people = os.path.join(DATA_DIR, "name.basics.tsv.gz")
        df_people_raw = read_tsv_gz(path_people)
        df_people = transform_people(df_people_raw)
        loader.load(df_people, "people")

        logger.info("ETL reload completed.")

    elif action == "update":
        update_loader = UpdateLoader(batch_size=10000)
        path_films = os.path.join(DATA_DIR, "title.basics.tsv.gz")
        logger.info(f"updating {path_films}")

        df_films_raw = read_tsv_gz(path_films)
        df_films = transform_films(df_films_raw)
        update_loader.update(df_films, "films", key_columns=["tconst"])

        path_people = os.path.join(DATA_DIR, "name.basics.tsv.gz")
        df_people_raw = read_tsv_gz(path_people)
        df_people = transform_people(df_people_raw)
        update_loader.update(df_people, "people", key_columns=["nconst"])

        logger.info("ETL update completed.")
    else:
        logger.error(f"Unknown action: '{action}'. Valid options are: 'clean', 'reload', or 'update'.")


if __name__ == "__main__":
    action = sys.argv[1].lower() if len(sys.argv) > 1 else "reload"
    mode = sys.argv[2].lower() if len(sys.argv) > 2 else "batch"
    main(action, mode)
