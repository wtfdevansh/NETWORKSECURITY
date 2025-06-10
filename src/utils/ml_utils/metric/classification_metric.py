from src.exception.exception import networkException
from src.logging.logger import logging
from sklearn.metrics import f1_score, precision_score, recall_score
from src.entity.artifacts_entity import ClassificationMetricArtifact



def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    """
    Calculate classification metrics: F1 score, precision score, and recall score.

    :param y_true: True labels.
    :param y_pred: Predicted labels.
    :return: ClassificationMetricArtifact containing the calculated metrics.
    """
    try:
        logging.info("Calculating classification metrics")
        f1 = f1_score(y_true, y_pred, average='weighted')
        precision = precision_score(y_true, y_pred, average='weighted')
        recall = recall_score(y_true, y_pred, average='weighted')

        return ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
    except Exception as e:
        raise networkException(f"Error calculating classification metrics: {e}") from e  