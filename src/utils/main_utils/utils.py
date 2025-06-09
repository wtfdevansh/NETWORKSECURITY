import yaml
import os , sys
from src.exception.exception import CustomException
from src.logging.logger import logging
import numpy as np
import dill
import pickle


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    
    :param file_path: Path to the YAML file.
    :return: Dictionary containing the YAML file content.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomException(f"Error reading YAML file at {file_path}: {e}", sys) from e
    

def write_yaml_file(file_path: str, data: dict):
    """
    Writes a dictionary to a YAML file.
    
    :param file_path: Path to the YAML file.
    :param data: Dictionary to write to the file.
    """
    try:
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
    except Exception as e:
        raise CustomException(f"Error writing YAML file at {file_path}: {e}", sys) from e