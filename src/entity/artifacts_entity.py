from src.constant import training_pipeline
import os
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ArtifactsEntity:
   train_file_path: str
   test_file_path: str


@dataclass
class dataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str