from src.exception.exception import networkException
from src.logging.logger import logging

from src.entity.config_entity import trainingPipelineConfig, dataIngestionConfig , dataValidationConfig , DataTransformationConfig, ModelTrainerConfig


from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.constant.training_pipeline import TRAINING_BUCKET_NAME

from src.entity.artifacts_entity import ArtifactsEntity, dataValidationArtifact , DataTransformationArtifact, ModelTrainerArtifact

from src.cloud.s3_syncer import S3Sync

class TrainingPipeline:
    def __init__(self, config: trainingPipelineConfig):
        self.config = config
        self.s3_sync = S3Sync()

    def run(self):
        try:
            logging.info("Starting the training pipeline...")

            # Data Ingestion
            data_ingestion_config = dataIngestionConfig(self.config)
            data_ingestion = DataIngestion()
            data_ingestion.initiate_data_ingestion()
            data_ingestion_artifacts:ArtifactsEntity = data_ingestion.initiate_data_ingestion()

            # Data Validation
            data_validation_config = dataValidationConfig(self.config)
            data_validation = DataValidation(data_validation_config , data_ingestion_artifacts)
            data_validation.initiate_data_validation()
            data_validation_artifact: dataValidationArtifact = data_validation.initiate_data_validation()

            # Data Transformation
            transformation_config = DataTransformationConfig(self.config)  
            data_transformation = DataTransformation(transformation_config , data_validation_artifact)
            data_transformation.initiate_data_transformation()
            data_transformation_artifact: DataTransformationArtifact = data_transformation.initiate_data_transformation()

            # Model Trainer
            model_trainer_config = ModelTrainerConfig(self.config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer.initiate_model_trainer()
            model_trainer_artifact = ModelTrainer(model_trainer_config , data_transformation_artifact)
            
            logging.info("Training pipeline completed successfully.")   

            #sync save mode dir to s3

            aws_bucket_url  = f"s3://{TRAINING_BUCKET_NAME}/artifacts/{self.config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.config.artifact_dir, aws_bucket_url=aws_bucket_url)
            logging.info(f"Artifacts synced to S3 bucket: {aws_bucket_url}")

            aws_bucket_url  = f"s3://{TRAINING_BUCKET_NAME}/model/{self.config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.config.model_dir, aws_bucket_url=aws_bucket_url)
            logging.info(f"Model synced to S3 bucket: {aws_bucket_url}")


        except Exception as e:
            logging.error(f"An error occurred in the training pipeline: {e}")
            raise networkException(e)
    