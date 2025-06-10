from src.exception.exception import networkException
from src.logging.logger import logging
from src.entity.config_entity import trainingPipelineConfig, dataIngestionConfig , dataValidationConfig , dataTransformationConfig, modelTrainerConfig
from src.entity.artifacts_entity import ArtifactsEntity , dataValidationArtifact
from src.components.data_ingestion import DataIngestion

from src.components.data_validation import DataValidation

from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


import sys


if __name__ == "__main__":
    try:
        logging.info("Starting the Network Security Pipeline")
        
        # Initialize the training pipeline configuration
        training_pipeline_config = trainingPipelineConfig()
        logging.info(f"Training Pipeline Config: {training_pipeline_config}")
        
        # Initialize data ingestion configuration
        data_ingestion_config = dataIngestionConfig(training_pipeline_config)
        logging.info(f"Data Ingestion Config: {data_ingestion_config}")
        
        # Create an instance of DataIngestion
        data_ingestion = DataIngestion()

        artifacts = data_ingestion.initiate_data_ingestion()

        print(artifacts)

        DataValidation = DataValidation(
            data_validation_config=data_ingestion_config,
            data_ingestion_artifact=artifacts
        )

        

        data_validation_artifact = DataValidation.initiate_data_validation()

        print(data_validation_artifact)

        logging.info("model transformation started....")
        data_transformation = DataTransformation(data_transformation_config=dataTransformationConfig(training_pipeline_config),
                                                  data_validation_artifact=data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("model transformation completed....")


        logging.info("model trainer started....")
        model_trainer = ModelTrainer(model_trainer_config=modelTrainerConfig(training_pipeline_config),
                                     data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("model trainer completed....")

    except Exception as e:
        raise networkException(e, sys)