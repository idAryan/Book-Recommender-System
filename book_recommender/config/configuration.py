import os
import sys
from book_recommender.logger.log import logging
from book_recommender.utils.util import read_yaml_file
from book_recommender.exception.exception_handler import AppException
from book_recommender.entity.config_entity import DataIngestionConfig
from book_recommender.constant import *

class AppConfiguration:
    def __init__(self, config_file_path=CONFIG_FILE_PATH):
        try:
            self.config = read_yaml_file(config_file_path)
            logging.info(f"Loaded configuration from {config_file_path}")
        except Exception as e:
            raise AppException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            # Access sections from YAML
            artifacts_config = self.config.get("artifacts_config", {})
            data_ingestion_config = self.config.get("data_ingestion_config", {})

            artifacts_dir = artifacts_config.get("artifacts_dir", "artifacts")
            dataset_download_url = data_ingestion_config.get("dataset_download_url", "")

            raw_data_dir = os.path.join(artifacts_dir, data_ingestion_config.get("raw_data_dir", "raw_data"))
            ingested_dir = os.path.join(artifacts_dir, data_ingestion_config.get("ingested_dir", "ingested_data"))

            data_ingestion = DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                raw_data_dir=raw_data_dir,
                ingested_dir=ingested_dir
            )

            logging.info(f"Data Ingestion Config: {data_ingestion}")
            return data_ingestion

        except Exception as e:
            raise AppException(e, sys)
