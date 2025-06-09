from src.entity.artifacts_entity import ArtifactsEntity, dataValidationArtifact
from src.utils.main_utils.utils import read_yaml_file , write_yaml_file
from src.entity.config_entity import dataValidationConfig
from src.constant.training_pipeline import SCHEMA_FILE_PATH
from src.logging.logger import logging
from src.exception.exception import CustomException
from scipy.stats import ks_2samp
import pandas as pd
import os

class DataValidation:
    def __init__(self , data_validation_config: dataValidationConfig , data_ingestion_artifact: ArtifactsEntity):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys)
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(f"Error reading data from {file_path}: {e}", sys) from e
        

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Validate if the number of columns in the dataframe matches the expected number of columns.
        """

        try:
            number_of_coumns = len(self._schema_config['columns'])
            logging.info(f"Expected number of columns: {number_of_coumns}")
            logging.info(f"Actual number of columns: {len(dataframe.columns)}") 

            if len(dataframe.columns) == number_of_coumns:
                return True
            else:
                logging.error(f"Number of columns mismatch: expected {number_of_coumns}, got {len(dataframe.columns)}")
                return False
        except Exception as e:
            raise CustomException(f"Error validating number of columns: {e}", sys) from e
        
    
    def is_numerical_column(self , dataframe: pd.DataFrame ) -> bool :
        """
        Check if the dataframe contains numerical columns.
        """
        try:
            numerical_columns = dataframe.select_dtypes(include=['number']).columns.tolist()
            actual_numerical_columns = self._schema_config.get('numerical_columns', [])

            logging.info(f"Expected numerical columns: {actual_numerical_columns}")
            logging.info(f"Actual numerical columns: {numerical_columns}")


            if set(numerical_columns) == set(actual_numerical_columns):
                logging.info("Numerical columns validation passed.")
                return True
            else:
                logging.error("Numerical columns validation failed.")
                return False
        except Exception as e:
            raise CustomException(f"Error checking for numerical columns: {e}", sys) from e
        
    def detect_data_drift(self, base_df , current_df  , thereshold: float = 0.05)->bool:
        """
        Detect data drift between the training and testing datasets using the Kolmogorov-Smirnov test.
        """
        try:
            status = True
            drift_report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_samp_dist = ks_2samp(d1,d2)
                
                if thereshold <= is_samp_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False

                drift_report[column] = {    
                    "p_value": is_samp_dist.pvalue,
                    "is_found": is_found
                }

            drift_report_file_path = self.data_validation_config.drift_report_dir
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)

            write_yaml_file(drift_report_file_path, drift_report)

            return status

        except Exception as e:
            raise CustomException(f"Error detecting data drift: {e}", sys) from e
        
    
    def initiate_data_validation(self)-> dataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path


            train_dataframe = self.read_data(train_file_path)
            test_dataframe = self.read_data(test_file_path)


            is_train_valid = self.validate_number_of_columns(train_dataframe)
            is_test_valid = self.validate_number_of_columns(test_dataframe)

            if not is_train_valid or not is_test_valid:
                raise CustomException("Data validation failed: Number of columns mismatch", sys)

            status = is_numerical_column(train_dataframe)
            if not status:
                raise CustomException("Data validation failed: Numerical columns mismatch", sys)
            status = is_numerical_column(test_dataframe)
            if not status:
                raise CustomException("Data validation failed: Numerical columns mismatch", sys)
            

            status = self.detect_data_drift(train_dataframe, test_dataframe)

            dir_path = self.data_validation_config.valid_data_dir
            os.makedirs(dir_path, exist_ok=True)

            if status == True:
                logging.info("Data validation passed. Saving valid data files.")
                train_dataframe.to_csv(self.data_validation_config.train_file_path, index=False)
                test_dataframe.to_csv(self.data_validation_config.test_file_path, index=False)
            else:
                logging.warning("Data validation failed. Saving invalid data files.")
                os.makedirs(self.data_validation_config.invalid_data_dir, exist_ok=True)
                train_dataframe.to_csv(self.data_validation_config.invalid_train_file_path, index=False)
                test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path, index=False)

            logging.info("Data validation completed successfully.")

            dataValidationArtifact = dataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.train_file_path,
                valid_test_file_path=self.data_validation_config.test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_dir
            )
            logging.info(f"Data validation artifact: {dataValidationArtifact}")
            return dataValidationArtifact
        except Exception as e:
            raise CustomException(e, sys)


