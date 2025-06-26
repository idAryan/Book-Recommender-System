from book_recommender.exception.exception_handler import AppException
from book_recommender.logger.log import logging
import sys
try:
    3/0
except Exception as e:
    logging.info(e)
    raise AppException(e,sys) from e