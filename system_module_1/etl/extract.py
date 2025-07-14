import os
import requests
from utils.logger import get_logger

logger = get_logger("extract")

IMDB_DATASETS = [
    "name.basics.tsv.gz",
    "title.basics.tsv.gz",
    "title.principals.tsv.gz",
]


def download_datasets(download_path="data/imdb_downloads"):
    os.makedirs(download_path, exist_ok=True)
    base_url = "https://datasets.imdbws.com/"

    for dataset in IMDB_DATASETS:
        url = base_url + dataset
        output_path = os.path.join(download_path, dataset)
        logger.info(f"Downloading {dataset}...")
        try:
            r = requests.get(url)
            r.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(r.content)
            logger.info(f"Downloaded {dataset}")
        except Exception as e:
            logger.error(f"Failed to download {dataset}: {e}")

    logger.info("All datasets processed.")
