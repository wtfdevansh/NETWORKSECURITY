import os

DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR_NAME: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
DATA_INGESTION_DATABASE_NAME: str = "devanshAI"
DATA_INGESTION_COLLECTION_NAME: str= "NetworkData"



TARGET_COLUMN = 'Result'
PIPELINE_NAME: str = 'NetworkSecurity'
ARTIFACT_DIR_NAME : str= 'artifacts'
FILE_NAME: str = 'phisingData.csv'
TRAIN_FILE_NAME: str = 'test.csv'
TEST_FILE_NAME: str = 'train.csv'

SCHEMA_FILE_PATH: str = os.path.join('data_schema', 'schema.yaml')


DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = 'validated'
DATA_VALIDATION_INVALID_DIR: str = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'report.yaml'







    