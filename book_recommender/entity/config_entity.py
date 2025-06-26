from collections import namedtuple

# Configuration for data ingestion
DataIngestionConfig = namedtuple("DatasetConfig", [
    "dataset_download_url",
    "raw_data_dir",
    "ingested_dir"
])

# Configuration for data validation
DataValidationConfig = namedtuple("DataValidationConfig", [
    "validation_status_file",
    "required_files"
])
