import os
import sys
import json


from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from src.logging.logger import logging
from src.exception.exception import networkException


class networkDataExtract():
    def __init__(self, database , collection):
        try:
            self.database = database
            self.collection = collection
        except Exception as e:
            raise networkException(e, sys)
        
    def cv_to_json(self, file_path: str):
        try:
            data =pd.read_csv(file_path)
            data = data.drop(columns=['Unnamed: 0'], axis=1, errors='ignore')
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise networkException(e, sys)
        
    def insert_data(self, records: list):
        try:
            self.records = records
            client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            db = client[self.database]
            collection = db[self.collection]
            collection.insert_many(self.records)
            logging.info("Data inserted successfully into MongoDB")
            return len(self.records)
        except Exception as e:
            raise networkException(e, sys)




if __name__ == '__main__':
    FILE_PATH = 'Network_Data/phisingData.csv'
    obj = networkDataExtract("devanshAI" , "NetworkData")
    records = obj.cv_to_json(FILE_PATH)
    no_of_records = obj.insert_data(records)
    print(no_of_records)

