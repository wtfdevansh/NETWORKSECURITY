from src.exception.exception import networkException as CustomException
import os
import sys
from src.utils.main_utils.utils import read_yaml_file, write_yaml_file, save_numpy_array_data, save_object
from src.entity.config_entity import trainingPipelineConfig, dataTransformationConfig
from src.logging.logger import logging
import pandas as pd
from src.entity.artifacts_entity import dataValidationArtifact, dataTransformationArtifact

from src.constant.training_pipeline import TARGET_COLUMN , DATA_TRANSFORMATION_IMPUTER_PARAMS
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer



class DataTransformation:
    def __init__(slef , data_transformation_config: dataTransformationConfig,
                 data_validation_artifact: dataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(self.data_transformation_config.schema_file_path)
        except Exception as e:
            raise CustomException(e, sys)
        

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(f"Error reading data from {file_path}: {e}", sys) from e 
        
    def get_data_transformation_object(cls) -> Pipeline:

        logging.info("Entered the get_data_transformation_object method of DataTransformation class")
        
        try:

            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise CustomException(f"Error creating data transformation object: {e}", sys) from e
        

    def initiate_data_transformation(self)-> dataTransformationArtifact:
        try:
            logging.info("Entered the initiate_data_transformation method of DataTransformation class")
            logging.info("Loading train and test data")
            train_df = self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = self.read_data(self.data_validation_artifact.valid_test_file_path)

            ##training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)


            ##test dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformation_object()

            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train_arr = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)


            train_arr = np.c_[transformed_input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_feature_test_arr, np.array(target_feature_test_df)]


            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_train_file_path,
                array=train_arr
            )
            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_test_file_path,
                array=test_arr
            )

            save_object(
                file_path=self.data_transformation_config.transformed_object_file_path,
                obj=preprocessor_obj
            )

            ##preparing the artifact
            data_transformation_artifact = dataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )

            return data_transformation_artifact
        except Exception as e:
            raise CustomException(f"Error in initiate_data_transformation: {e}", sys) from e