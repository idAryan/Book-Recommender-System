import os
import sys
from book_recommender.logger.log import logging
from book_recommender.utils.util import read_yaml_file
from book_recommender.exception.exception_handler import AppException
from book_recommender.entity.config_entity import DataIngestionConfig, DataValidationConfig
from book_recommender.constant import CONFIG_FILE_PATH


class Configuration:
    def __init__(self, config_file_path=CONFIG_FILE_PATH):
        try:
            self.config = read_yaml_file(config_file_path)
            logging.info(f"Loaded configuration from {config_file_path}")
        except Exception as e:
            raise AppException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            artifacts_config = self.config.get("artifacts_config", {})
            data_ingestion_config = self.config.get("data_ingestion_config", {})

            artifacts_dir = artifacts_config.get("artifacts_dir", "artifacts")
            raw_data_dir = os.path.join(artifacts_dir, data_ingestion_config.get("raw_data_dir", "raw_data"))
            ingested_dir = os.path.join(artifacts_dir, data_ingestion_config.get("ingested_dir", "ingested_data"))
            dataset_download_url = data_ingestion_config.get("dataset_download_url", "")

            return DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                raw_data_dir=raw_data_dir,
                ingested_dir=ingested_dir
            )
        except Exception as e:
            raise AppException(e, sys)

    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            artifacts_config = self.config.get("artifacts_config", {})
            data_validation_config = self.config.get("data_validation_config", {})

            artifacts_dir = artifacts_config.get("artifacts_dir", "artifacts")
            validation_status_file = os.path.join(
                artifacts_dir,
                data_validation_config.get("validation_status_file", "validation_report.yaml")
            )
            required_files = data_validation_config.get("required_files", [])

            return DataValidationConfig(
                validation_status_file=validation_status_file,
                required_files=required_files
            )
        except Exception as e:
            raise AppException(e, sys)
