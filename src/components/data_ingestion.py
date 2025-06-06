import pymongo
import sys
import os
import pandas as pd
import numpy as np

from src.exception.exception import networkException
from src.logging.logger import logging
from src.entity.config_entity import dataIngestionConfig

data_ingestion_config_obj = dataIngestionConfig()

from dotenv import load_dotenv
load_dotenv()

from sklearn.model_selection import train_test_split
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

class  DataIngestion:
    def __init__(self):
        try:
            self.data_ingestion_config = dataIngestionConfig()
            logging.info(f"Data Ingestion Config: {self.data_ingestion_config}")
        except Exception as e:
            raise networkException(e, sys)

    def get_raw_data(self):
        try:
            client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            db = client[self.data_ingestion_config.database_name]
            collection = db.get_collection(self.data_ingestion_config.collection_name)
            cursor = collection.find()
            documents = list(cursor)
            df = pd.DataFrame(documents)
            logging.info(f"Raw data fetched from MongoDB: {df.shape}")

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True, axis=1)
                logging.info("Dropped '_id' column from DataFrame")

            df.replace({"na":np.nan}, inplace=True)

            return df
        except Exception as e:
            raise networkException(e , sys)
        
    

    def export_raw_data(self , df: pd.DataFrame):
      try:
        FILE_PATH = self.data_ingestion_config.feature_store_dir
        FILE_PATH = os.path.join(FILE_PATH, self.data_ingestion_config.file_name)
        os.makedirs(FILE_PATH , exist_ok=True)
        df.to_csv(FILE_PATH , index=False)
        logging.info(f"Raw data exported to {FILE_PATH}")
      except Exception as e:
          raise networkException(e , sys)
      

      

    def train_test_split_and_save(self, df: pd.DataFrame):
        try:
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            logging.info(f"Train DataFrame Shape: {train_df.shape}")
            logging.info(f"Test DataFrame Shape: {test_df.shape}")
            train_file_path = self.data_ingestion_config.train_file_path
            test_file_path = self.data_ingestion_config.test_file_path
            logging.info(f"Train File Path: {train_file_path}")
            logging.info(f"Test File Path: {test_file_path}")
            os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
            train_df.to_csv(train_file_path, index=False)
            test_df.to_csv(test_file_path, index=False)
            logging.info(f"Train and test datasets created: {train_file_path}, {test_file_path}")

        except Exception as e:
            raise networkException(e, sys)
        


    def initiate_data_ingestion(self):
        try:
            dataframe = self.get_raw_data()
            self.export_raw_data(dataframe)
            self.train_test_split_and_save(dataframe)
        except Exception as e:
            raise networkException(e, sys)

