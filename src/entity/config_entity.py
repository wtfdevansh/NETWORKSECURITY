from datatime import datetime
import os
from src.constant import training_pipeline



class trainingPipelineConfig:
    def __init__(self , timestamp = datetime.now()):

        self.timestamp = timestamp.strftime("%Y-%m-%d-%H-%M-%S")

        self.pipeline_name = training_pipeline.PIPELINE_NAME

        self.artifact_name = training_pipeline.ARTIFACT_DIR_NAME

        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)

        self.file_name = training_pipeline.FILE_NAME

        self.train_file_name = training_pipeline.TRAIN_FILE_NAME
        
        self.test_file_name = training_pipeline.TEST_FILE_NAME






class dataIngestionConfig:
    def __init__(self , training_pipeline_config: trainingPipelineConfig):

        self.training_pipeline_config = training_pipeline_config

        self.data_ingestion_dir = os.path.join(self.training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)

        self.feature_store_dir = os.path.join(self.training_pipeline_config.artifact_dir,  training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR_NAME)

        self.ingested_dir = os.path.join(self.training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR_NAME)

        self.train_file_path = os.path.join(self.ingested_dir, self.training_pipeline_config.train_file_name)

        self.test_file_path = os.path.join(self.ingested_dir, self.training_pipeline_config.test_file_name)

        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME

        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME

