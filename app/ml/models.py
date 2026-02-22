from abc import ABC, abstractmethod
from typing import Dict, Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

MODEL_REGISTRY = {}

class BaseModel(ABC):
    @abstractmethod
    def train(self, X, y, hyperparams: Dict[str, Any]):
        pass

    @abstractmethod
    def predict(self, X):
        pass


class RandomForestModel(BaseModel):
    def __init__(self):
        self.model = None
        self.le = LabelEncoder()

    def train(self, X, y, hyperparams: Dict[str, Any]):
        n_estimators = int(hyperparams.get("n_estimators", 100))
        max_depth = hyperparams.get("max_depth", None)
        if max_depth: max_depth = int(max_depth)

        y_encoded = self.le.fit_transform(y)

        self.model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
        self.model.fit(X, y_encoded)
        return self

    def predict(self, X):
        return self.model.predict(X)


class LogisticRegressionModel(BaseModel):
    def __init__(self):
        self.model = None
        self.le = LabelEncoder()

    def train(self, X, y, hyperparams: Dict[str, Any]):
        C = float(hyperparams.get("C", 1.0))

        y_encoded = self.le.fit_transform(y)

        self.model = LogisticRegression(C=C, max_iter=200)
        self.model.fit(X, y_encoded)
        return self

    def predict(self, X):
        return self.model.predict(X)

MODEL_REGISTRY["RandomForest"] = RandomForestModel
MODEL_REGISTRY["LogisticRegression"] = LogisticRegressionModel