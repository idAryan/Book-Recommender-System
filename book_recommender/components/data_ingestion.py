import os
import zipfile
from book_recommender.logger.log import logging
from book_recommender.exception.exception_handler import AppException

import os
import sys
import shutil
import requests
import zipfile
from book_recommender.logger.log import logging
from book_recommender.exception.exception_handler import AppException
from book_recommender.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        try:
            self.config = config
        except Exception as e:
            raise AppException(e, sys)

    def download_data(self) -> str:
        """
        Downloads the dataset from the URL to the raw_data_dir.
        Returns the path to the downloaded file.
        """
        try:
            if not self.config.dataset_download_url:
                raise ValueError("Dataset URL is empty in the configuration.")

            os.makedirs(self.config.raw_data_dir, exist_ok=True)
            file_name = "dataset.zip" if self.config.dataset_download_url.endswith(".zip") else "dataset.csv"
            file_path = os.path.join(self.config.raw_data_dir, file_name)

            response = requests.get(self.config.dataset_download_url, timeout=30)
            response.raise_for_status()

            with open(file_path, "wb") as f:
                f.write(response.content)

            logging.info(f"Dataset downloaded at: {file_path}")
            return file_path

        except Exception as e:
            raise AppException(e, sys)

    def extract_zip_file(self, zip_file_path: str, extract_to_dir: str):
        """
        Extracts the contents of a zip file to the given directory.
        """
        try:
            os.makedirs(extract_to_dir, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_dir)
            logging.info(f"Extracted zip file: {zip_file_path} to: {extract_to_dir}")
        except Exception as e:
            raise AppException(e, sys)

    def copy_to_ingested(self, source_dir: str):
        """
        Copies all files from the raw_data_dir to the ingested_dir.
        """
        try:
            os.makedirs(self.config.ingested_dir, exist_ok=True)

            for file_name in os.listdir(source_dir):
                full_file_name = os.path.join(source_dir, file_name)
                if os.path.isfile(full_file_name):
                    shutil.copy(full_file_name, self.config.ingested_dir)
                    logging.info(f"Copied {file_name} to ingested directory")

        except Exception as e:
            raise AppException(e, sys)

    def initiate_data_ingestion(self):
        """
        Executes the full data ingestion workflow:
        - Downloads data
        - Extracts if ZIP
        - Copies to ingested_dir
        """
        try:
            logging.info("Data ingestion started.")

            downloaded_file_path = self.download_data()

            # If zip file, extract it
            if downloaded_file_path.endswith(".zip"):
                self.extract_zip_file(downloaded_file_path, self.config.raw_data_dir)

            self.copy_to_ingested(self.config.raw_data_dir)

            logging.info("Data ingestion completed successfully.")

        except Exception as e:
            raise AppException(e, sys)

