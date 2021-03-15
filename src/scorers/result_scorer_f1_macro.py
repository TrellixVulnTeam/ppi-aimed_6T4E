
from scorers.base_classification_scorer import BaseClassificationScorer


class ResultScorerF1Macro(BaseClassificationScorer):
    """

    Calculate the score F1 Macro
    """
    def __init__(self):
        pass

    def __call__(self, y_actual, y_pred, pos_label):
        from sklearn.metrics import f1_score

        f1 = f1_score(y_actual, y_pred, pos_label=pos_label, average='macro')

        return f1
