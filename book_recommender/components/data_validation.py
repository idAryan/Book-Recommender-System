import os
import sys
import yaml
import pandas as pd
from book_recommender.logger.log import logging
from book_recommender.exception.exception_handler import AppException
from book_recommender.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig, raw_data_dir: str):
        self.config = config
        self.raw_data_dir = raw_data_dir

    def validate_required_files(self) -> bool:
        try:
            missing_files = []
            for file in self.config.required_files:
                if not os.path.exists(os.path.join(self.raw_data_dir, file)):
                    missing_files.append(file)

            result = {
                "validation_status": "SUCCESS" if not missing_files else "FAILED",
                "missing_files": missing_files
            }

            os.makedirs(os.path.dirname(self.config.validation_status_file), exist_ok=True)
            with open(self.config.validation_status_file, "w") as report_file:
                yaml.dump(result, report_file)

            if missing_files:
                logging.warning(f"Missing files: {missing_files}")
                return False

            logging.info("All required files found.")
            return True

        except Exception as e:
            raise AppException(e, sys)

    def preprocess_data(self):
        try:
            logging.info("Starting data preprocessing...")

            books_path = os.path.join(self.raw_data_dir, "books.csv")
            users_path = os.path.join(self.raw_data_dir, "users.csv")
            ratings_path = os.path.join(self.raw_data_dir, "ratings.csv")

            books = pd.read_csv(books_path, sep=";", encoding='ISO-8859-1', on_bad_lines='skip')
            users = pd.read_csv(users_path, sep=";", encoding='ISO-8859-1', on_bad_lines='skip')
            ratings = pd.read_csv(ratings_path, sep=";", encoding='ISO-8859-1', on_bad_lines='skip')

            # Column renaming
            books.rename(columns={
                "Book-Title": "title",
                "Book-Author": "author",
                "Year-Of-Publication": "year",
                "Publisher": "publisher",
                "Image-URL-L": "image_url"
            }, inplace=True)

            users.rename(columns={
                "User-ID": "user_id",
                "Location": "location",
                "Age": "age"
            }, inplace=True)

            ratings.rename(columns={
                "User-ID": "user_id",
                "Book-Rating": "book_rating"
            }, inplace=True)

            # Logging shape and preview
            logging.info(f"Books shape: {books.shape}")
            logging.info(f"Users shape: {users.shape}")
            logging.info(f"Ratings shape: {ratings.shape}")
            logging.info(f"Books sample:\n{books.head(2)}")
            logging.info(f"Users sample:\n{users.head(2)}")
            logging.info(f"Ratings sample:\n{ratings.head(2)}")

            # Merge sanity check
            ratings_with_books = ratings.merge(books, on="ISBN", how="inner")
            logging.info(f"Merged ratings_with_books shape: {ratings_with_books.shape}")

        except Exception as e:
            raise AppException(e, sys)

    def initiate_data_validation(self) -> bool:
        try:
            logging.info("Initiating full data validation process...")
            files_ok = self.validate_required_files()

            if not files_ok:
                logging.error("Data validation failed due to missing files.")
                return False

            self.preprocess_data()
            logging.info("Data validation completed successfully.")
            return True
        except Exception as e:
            raise AppException(e, sys)
