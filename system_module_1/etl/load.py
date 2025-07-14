import time
import os
import tempfile
import pandas as pd
from config.db_config import get_db_connection
from utils.logger import get_logger

logger = get_logger("load")

class DataLoaderStrategy:
    def load(self, df: pd.DataFrame, table_name: str):
        raise NotImplementedError

class BatchLoader(DataLoaderStrategy):
    def __init__(self, batch_size=10000):
        self.batch_size = batch_size

    def load(self, df: pd.DataFrame, table_name: str):
        start_time = time.perf_counter()
        conn = get_db_connection()
        cursor = conn.cursor()

        placeholders = ', '.join(['%s'] * len(df.columns))
        columns = ', '.join(df.columns)
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        def row_generator():
            for row in df.itertuples(index=False, name=None):
                yield tuple(None if pd.isna(v) else v for v in row)

        total_rows = len(df)
        processed = 0
        try:
            batch = []
            for i, row in enumerate(row_generator(), 1):
                batch.append(row)
                if len(batch) >= self.batch_size:
                    cursor.executemany(insert_query, batch)
                    conn.commit()
                    processed += len(batch)
                    logger.info(f"[{processed/total_rows:.1%}] Inserted {processed}/{total_rows} rows")
                    batch = []
            if batch:
                cursor.executemany(insert_query, batch)
                conn.commit()
                processed += len(batch)
                logger.info(f"[{processed/total_rows:.1%}] Inserted {processed}/{total_rows} rows")

            elapsed = time.perf_counter() - start_time
            logger.info(f"Batch loader: Loaded total {processed} rows into `{table_name}` in {elapsed:.2f} seconds")

        except Exception as e:
            logger.error(f"Batch loader error: {e}")
        finally:
            cursor.close()
            conn.close()


class CSVLoader(DataLoaderStrategy):
    def load(self, df: pd.DataFrame, table_name: str):
        start_time = time.perf_counter()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmpfile:
            tmp_csv_path = tmpfile.name
            df.to_csv(tmp_csv_path, index=False, header=False, na_rep='\\N')

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            csv_path = tmp_csv_path.replace("\\", "/")
            cursor.execute(f"""
                LOAD DATA LOCAL INFILE '{csv_path}'
                INTO TABLE {table_name}
                FIELDS TERMINATED BY ',' 
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                ({', '.join(df.columns)})
            """)
            conn.commit()
            elapsed = time.perf_counter() - start_time
            logger.info(f"CSV loader: Loaded total {len(df)} rows into `{table_name}` in {elapsed:.2f} seconds")
        except Exception as e:
            logger.error(f"CSV loader error: {e}")
        finally:
            cursor.close()
            conn.close()
            os.remove(tmp_csv_path)


class UpdateLoader(BatchLoader):
    def update(self, df: pd.DataFrame, table_name: str, key_columns: list):
        """
        Inserta solo filas nuevas (no presentes ya en la tabla)
        usando los valores de las columnas claves (key_columns) para detectar duplicados.
        """
        start_time = time.perf_counter()
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            keys_str = ', '.join(key_columns)
            cursor.execute(f"SELECT {keys_str} FROM {table_name}")
            existing_keys = set(cursor.fetchall())

            def key_tuple(row):
                return tuple(row[col] for col in key_columns)

            df_new = df[~df.apply(key_tuple, axis=1).isin(existing_keys)]

            if df_new.empty:
                logger.info(f"No new rows to update in {table_name}.")
                return

            placeholders = ', '.join(['%s'] * len(df_new.columns))
            columns = ', '.join(df_new.columns)
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            total_rows = len(df_new)
            processed = 0

            def row_generator():
                for row in df_new.itertuples(index=False, name=None):
                    yield tuple(None if pd.isna(v) else v for v in row)

            batch = []
            for i, row in enumerate(row_generator(), 1):
                batch.append(row)
                if len(batch) >= self.batch_size:
                    cursor.executemany(insert_query, batch)
                    conn.commit()
                    processed += len(batch)
                    logger.info(f"[{processed/total_rows:.1%}] Updated {processed}/{total_rows} rows in {table_name}")
                    batch = []
            if batch:
                cursor.executemany(insert_query, batch)
                conn.commit()
                processed += len(batch)
                logger.info(f"[{processed/total_rows:.1%}] Updated {processed}/{total_rows} rows in {table_name}")

            elapsed = time.perf_counter() - start_time
            logger.info(f"Update loader: Updated total {processed} rows into `{table_name}` in {elapsed:.2f} seconds")

        except Exception as e:
            logger.error(f"Update loader error: {e}")
        finally:
            cursor.close()
            conn.close()


class DataLoader:
    def __init__(self, strategy: DataLoaderStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: DataLoaderStrategy):
        self.strategy = strategy

    def load(self, df: pd.DataFrame, table_name: str):
        self.strategy.load(df, table_name)
