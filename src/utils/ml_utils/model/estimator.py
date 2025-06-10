from src.constant.training_pipeline import SAVED_MODEL_DIR , MODEL_FILE_NAME

from src.exception.exception import networkException
from src.logging.logger import logging

import os
import sys


class NetworkModel:
    def __init__(self, preprocessor , model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise networkException(e, sys) from e
        
    def predict(self, X):
        try:
            logging.info("Making predictions using the model")
            X_transform = self.preprocessor.transform(X)
            y_hat = self.model.predict(X_transform)
            return y_hat
        except Exception as e:
            raise networkException(f"Error during prediction: {e}", sys) from e
    
