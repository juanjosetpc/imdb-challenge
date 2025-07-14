import pandas as pd
from utils.logger import get_logger
from datetime import datetime

logger = get_logger("transform")

def read_tsv_gz(filepath: str) -> pd.DataFrame:
    logger.info(f"Reading file: {filepath}")
    try:
        df = pd.read_csv(filepath, sep='\t', compression='gzip', na_values='\\N', low_memory=False)
        logger.info(f"File loaded: {filepath} with {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
        return pd.DataFrame()
    
def save_discarded(df_discarded: pd.DataFrame, base_filepath: str):
    if not df_discarded.empty:
        df_discarded = df_discarded.copy()
        df_discarded['discarded_at'] = datetime.now().isoformat()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = base_filepath.replace(".csv", f"_{timestamp}.csv")
        df_discarded.to_csv(filepath, index=False)
        logger.info(f"Saved {len(df_discarded)} discarded rows with timestamp to {filepath}")


def transform_films(df: pd.DataFrame, discard_path="discarded_films.csv") -> pd.DataFrame:
    logger.info("Transforming films data")
    logger.debug(f"DataFrame columns: {df.columns.tolist()}")

    required_cols = ["tconst", "primaryTitle", "titleType", "originalTitle"]
    mask = df[required_cols].notnull().all(axis=1)

    discarded = df.loc[~mask].copy()
    save_discarded(discarded, discard_path)

    df = df.loc[mask, :].copy()  

    df['runtimeMinutes'] = pd.to_numeric(df['runtimeMinutes'], errors='coerce')

    # Sanitize isAdult
    df['isAdult'] = pd.to_numeric(df['isAdult'], errors='coerce')
    df.loc[~df['isAdult'].isin([0, 1]), 'isAdult'] = pd.NA
    
    return df

def transform_people(df: pd.DataFrame, discard_path="discarded_people.csv") -> pd.DataFrame:
    logger.info("Transforming people data")

    required_cols = ["nconst", "primaryName", "primaryProfession", "birthYear"]
    mask = df[required_cols].notnull().all(axis=1)

    discarded = df.loc[~mask].copy()
    save_discarded(discarded, discard_path)

    df_filtered = df.loc[mask, :]
    cols_needed = [
        "nconst", "primaryName", "birthYear", "deathYear",
        "primaryProfession", "knownForTitles"
    ]
    existing_cols = [col for col in cols_needed if col in df_filtered.columns]
    df_filtered = df_filtered[existing_cols]

    return df_filtered

def transform_people_films(df: pd.DataFrame, discard_path="discarded_people_films.csv") -> pd.DataFrame:
    logger.info("Transforming people-films relation data")

    required_cols = ["nconst", "tconst"]
    mask = df[required_cols].notnull().all(axis=1)

    discarded = df.loc[~mask].copy()
    save_discarded(discarded, discard_path)

    df_filtered = df.loc[mask, :]
    cols_needed = ["nconst", "tconst", "category", "job", "characters"]
    existing_cols = [col for col in cols_needed if col in df_filtered.columns]
    df_filtered = df_filtered[existing_cols]

    return df_filtered