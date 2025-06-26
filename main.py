from book_recommender.pipeline.training_pipeline import TrainPipeline
from book_recommender.logger.log import logging

if __name__ == "__main__":
    try:
        logging.info("Main execution started.")
        pipeline = TrainPipeline()
        pipeline.run_pipeline()
        logging.info("Main execution finished.")
    except Exception as e:
        logging.error(f"An error occurred in main: {e}")
        raise e
