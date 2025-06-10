from src.exception.exception import networkException
from src.logging.logger import logging

from src.entity.config_entity import trainingPipelineConfig, dataIngestionConfig , dataValidationConfig , DataTransformationConfig, ModelTrainerConfig


from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.entity.artifacts_entity import ArtifactsEntity, dataValidationArtifact , DataTransformationArtifact, ModelTrainerArtifact

class TrainingPipeline:
    def __init__(self, config: trainingPipelineConfig):
        self.config = config

    def run(self):
        try:
            logging.info("Starting the training pipeline...")

            # Data Ingestion
            data_ingestion_config = dataIngestionConfig(self.config)
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifacts:ArtifactsEntity = data_ingestion.initiate_data_ingestion()

            # Data Validation
            data_validation_config = dataValidationConfig(self.config)
            data_validation = DataValidation(data_validation_config , data_ingestion_artifacts)
            data_validation_artifact: dataValidationArtifact = data_validation.initiate_data_validation()

            # Data Transformation
            transformation_config = DataTransformationConfig(self.config)  
            data_transformation = DataTransformation(transformation_config , data_validation_artifact)
            data_transformation_artifact: DataTransformationArtifact = data_transformation.initiate_data_transformation()

            # Model Trainer
            model_trainer_config = ModelTrainerConfig(self.config)
            model_trainer_artifact = ModelTrainer(model_trainer_config , data_transformation_artifact)
            
            logging.info("Training pipeline completed successfully.")   
        except Exception as e:
            logging.error(f"An error occurred in the training pipeline: {e}")
            raise networkException(e)
    