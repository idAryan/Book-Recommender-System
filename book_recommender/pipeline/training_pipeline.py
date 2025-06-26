from book_recommender.components.data_ingestion import DataIngestion
import sys
from book_recommender.logger.log import logging
from book_recommender.exception.exception_handler import AppException
from book_recommender.config.configuration import Configuration
from book_recommender.components.data_ingestion import DataIngestion

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
            data_ingestion_config = self.config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise AppException(e, sys)

    def run_pipeline(self):
        """
        The full training pipeline. Add more stages here as needed.
        """
        try:
            logging.info("\n\n========= Training Pipeline Started =========\n")
            
            self.start_data_ingestion()
            # Future steps:
            # self.start_data_validation()
            # self.start_data_transformation()
            # self.start_model_training()
            # self.start_model_evaluation()
            # self.start_model_pusher()

            logging.info("\n\n========= Training Pipeline Completed Successfully =========\n")
        except Exception as e:
            logging.error("Training pipeline failed.")
            raise AppException(e, sys)
