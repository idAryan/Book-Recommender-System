import sys
from book_recommender.logger.log import logging
from book_recommender.exception.exception_handler import AppException
from book_recommender.configuration.configuration import Configuration
from book_recommender.components.data_ingestion import DataIngestion
from book_recommender.components.data_validation import DataValidation

class TrainPipeline:
    def __init__(self):
        try:
            self.config = Configuration()
        except Exception as e:
            raise AppException(e, sys)

    def start_data_ingestion(self):
        """
        Run data ingestion process using configuration.
        """
        try:
            logging.info("🚚 Starting Data Ingestion...")
            data_ingestion_config = self.config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.initiate_data_ingestion()
            logging.info("✅ Data Ingestion completed.")
        except Exception as e:
            raise AppException(e, sys)

    def start_data_validation(self):
        """
        Run data validation process using configuration.
        """
        try:
            logging.info("🔍 Starting Data Validation...")
            data_ingestion_config = self.config.get_data_ingestion_config()
            data_validation_config = self.config.get_data_validation_config()

            data_validation = DataValidation(
                config=data_validation_config,
                raw_data_dir=data_ingestion_config.raw_data_dir
            )
            validation_successful = data_validation.initiate_data_validation()

            if not validation_successful:
                raise Exception("❌ Data validation failed.")

            logging.info("✅ Data Validation completed.")
        except Exception as e:
            raise AppException(e, sys)

    def run_pipeline(self):
        """
        Run the entire training pipeline.
        """
        try:
            logging.info("\n\n🚀 ========= Training Pipeline Started =========\n")

            self.start_data_ingestion()
            self.start_data_validation()

            # TODO: Add further stages below
            # self.start_data_transformation()
            # self.start_model_training()
            # self.start_model_evaluation()
            # self.start_model_pusher()

            logging.info("\n✅ ========= Training Pipeline Completed Successfully =========\n")
        except Exception as e:
            logging.error("❌ Training pipeline failed.")
            raise AppException(e, sys)
