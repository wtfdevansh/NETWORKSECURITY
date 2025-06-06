from src.exception import networkException
from src.logging import logging
from src.entity.config_entity import trainingPipelineConfig, dataIngestionConfig
from src.entity.artifacts_entity import ArtifactsEntity
from src.components.data_ingestion import DataIngestion


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
        data_ingestion = DataIngestion(data_ingestion_config)

        artifacts = data_ingestion.initiate_data_ingestion()

        print(artifacts)



    except Exception as e:
        raise networkException(e, sys)