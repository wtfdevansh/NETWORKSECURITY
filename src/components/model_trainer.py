import os
import sys

from src.exception.exception import networkException as CustomException
from src.logging.logger import logging

from src.utils.main_utils.utils import read_yaml_file, write_yaml_file, save_numpy_array_data, save_object

from src.entity.config_entity import trainingPipelineConfig, modelTrainerConfig
from src.entity.artifacts_entity import ModelTrainerArtifact, ClassificationMetricArtifact , DataTransformationArtifact

from src.utils.main_utils.utils import save_object , load_object , evaluate_model
from src.utils.main_utils.metrics import load_numpy_array_data
from src.utils.ml_utils.metric.classification_metric import get_classification_score
from src.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier



class ModelTrainer:
    def __init__(self , model_trainer_config: modelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
        

    def train_model(self, x_train, y_train , x_test, y_test):
        models = {
            "Logistic Regression": LogisticRegression(verbose = 1),
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "AdaBoost": AdaBoostClassifier()
        }
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }

        model_report:dict = evaluate_model(
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
            models=models,
            params=params
        )

        best_model_score = max(model_report.values())
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

        best_model = models[best_model_name]
        logging.info(f"Best model found: {best_model_name} with score: {best_model_score}")

        y_train_pred = best_model.predict(x_train)
        y_test_pred = best_model.predict(x_test)

        classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred, dataset="train")
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred, dataset="test")

        ## track the mlflow

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path = os.path.join(
            self.model_trainer_config.trained_model_dir,
            self.model_trainer_config.trained_model_name
        )
        os.makedirs(model_dir_path, exist_ok=True)

        Network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path , obj = Network_model)

        
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                                                    train_metric_artifact=ClassificationMetricArtifact(**classification_train_metric),
                                                    test_metric_artifact=ClassificationMetricArtifact(**classification_test_metric))
        

        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact
         

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(file_path=train_file_path, array_name="train")
            test_arr = load_numpy_array_data(file_path=test_file_path, array_name="test")

            x_train = train_arr[:, :-1]
            y_train = train_arr[:, -1]
            x_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]

            model = self.train_model(x_train, y_train , x_test, y_test)

            return model
           
        except Exception as e:
            raise CustomException(e, sys) from e


