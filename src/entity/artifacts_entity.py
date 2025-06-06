from src.constant import training_pipeline
import os
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ArtifactsEntity:
   train_file_path: str
   test_file_path: str