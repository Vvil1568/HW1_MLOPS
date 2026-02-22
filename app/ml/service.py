import pandas as pd
import joblib
import os
from clearml import Task
from app.ml.models import MODEL_REGISTRY
from app.config import settings
from app.logger import get_logger

logger = get_logger(__name__)


class MLServiceLogic:
    def get_available_models(self):
        return list(MODEL_REGISTRY.keys())

    def train(self, model_type: str, dataset_path: str, hyperparams: dict) -> str:
        logger.info(f"Starting training: {model_type} on {dataset_path}")
        clean_endpoint = settings.AWS_ENDPOINT_URL.replace("http://", "").replace("https://", "")
        output_uri = f"s3://{clean_endpoint}/{settings.S3_BUCKET_NAME}/models"

        task = None
        try:
            current_task = Task.current_task()
            if current_task:
                current_task.close()

            task = Task.init(
                project_name="Homework1_MLOps",
                task_name=f"Train_{model_type}",
                task_type=Task.TaskTypes.training,
                output_uri=output_uri,
                reuse_last_task_id=False
            )
            task.connect(hyperparams)

            full_path = os.path.join(settings.DATA_DIR, dataset_path)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Dataset {dataset_path} not found")

            df = pd.read_csv(full_path) if dataset_path.endswith(".csv") else pd.read_json(full_path)
            X, y = df.iloc[:, :-1], df.iloc[:, -1]

            model_cls = MODEL_REGISTRY.get(model_type)
            if not model_cls:
                raise ValueError(f"Model type {model_type} not supported")

            clf = model_cls()
            trained_model = clf.train(X, y, hyperparams)

            model_filename = "model.pkl"
            joblib.dump(trained_model, model_filename)
            task.upload_artifact("model", artifact_object=model_filename)
            logger.info("Training completed")
            return task.id

        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise e
        finally:
            if task:
                task.close()

    def predict(self, model_id: str, features: list) -> list:
        task = Task.get_task(task_id=model_id)
        if not task:
            raise ValueError(f"Task/Model {model_id} not found in ClearML")

        model_artifact = task.artifacts['model'].get_local_copy()
        loaded_model = joblib.load(model_artifact)
        predictions = loaded_model.predict(features)
        return predictions.tolist()

    def delete_model(self, model_id: str):
        task = Task.get_task(task_id=model_id)
        if not task:
            raise ValueError(f"Task/Model {model_id} not found")
        task.delete()
        logger.info(f"Model {model_id} deleted successfully")