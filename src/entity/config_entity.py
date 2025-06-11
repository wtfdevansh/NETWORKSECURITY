from datetime import datetime
import os
from src.constant import training_pipeline



class trainingPipelineConfig:
    def __init__(self , timestamp = datetime.now()):

        self.timestamp = timestamp.strftime("%Y-%m-%d-%H-%M-%S")

        self.pipeline_name = training_pipeline.PIPELINE_NAME

        self.artifact_name = training_pipeline.ARTIFACT_DIR_NAME

        self.artifact_dir = os.path.join(self.artifact_name,self.timestamp)

        self.file_name = training_pipeline.FILE_NAME

        self.train_file_name = training_pipeline.TRAIN_FILE_NAME
        
        self.test_file_name = training_pipeline.TEST_FILE_NAME

        self.model_dir=os.path.join("final_model")






class dataIngestionConfig:
    def __init__(self , training_pipeline_config: trainingPipelineConfig):

        self.training_pipeline_config = training_pipeline_config

        self.data_ingestion_dir = os.path.join(self.training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)

        self.feature_store_dir = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR_NAME)

        self.ingested_dir = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR)

        self.train_file_path = os.path.join(self.ingested_dir, self.training_pipeline_config.train_file_name)

        self.test_file_path = os.path.join(self.ingested_dir, self.training_pipeline_config.test_file_name)

        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME

        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME


class dataValidationConfig:
    def __init__(self , training_pipeline_config: trainingPipelineConfig):

        self.training_pipeline_config = training_pipeline_config
        self.data_validation_dir = os.path.join(self.training_pipeline_config.artifact_name ,training_pipeline_config.timestamp ,training_pipeline.DATA_VALIDATION_DIR_NAME )
        self.valid_data_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.train_file_path = os.path.join(self.valid_data_dir, self.training_pipeline_config.train_file_name)
        self.test_file_path = os.path.join(self.valid_data_dir, self.training_pipeline_config.test_file_name)
        self.invalid_train_file_path = os.path.join(self.invalid_data_dir, self.training_pipeline_config.train_file_name)
        self.invalid_test_file_path = os.path.join(self.invalid_data_dir, self.training_pipeline_config.test_file_name)
        self.drift_report_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR , training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)



class DataTransformationConfig:
     def __init__(self,training_pipeline_config:trainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME )
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"), )
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,)
        self.schema_file_path: str = training_pipeline.SCHEMA_FILE_PATH


class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:trainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME
        )

        self.trained_model_dir: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR
        )
        self.trained_model_name: str = training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR , training_pipeline.MODEL_FILE_NAME
        )
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD