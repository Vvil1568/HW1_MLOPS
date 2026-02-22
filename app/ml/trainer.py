import pandas as pd
import joblib
from clearml import Task
from app.ml.models import MODEL_REGISTRY
from app.config import settings
from app.logger import get_logger
import os

logger = get_logger(__name__)


class MLTrainer:
    def train(self, model_type: str, dataset_path: str, hyperparams: dict):
        logger.info(f"Starting training: {model_type} on {dataset_path}")

        clean_endpoint = settings.AWS_ENDPOINT_URL.replace("http://", "").replace("https://", "")
        output_uri = f"s3://{clean_endpoint}/{settings.S3_BUCKET_NAME}/models"

        task = None
        try:
            current_task = Task.current_task()
            if current_task:
                logger.warning(f"Closing lingering task {current_task.id}")
                current_task.close()

            print(f"DEBUG: Init task with URI: {output_uri}")
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

            if dataset_path.endswith(".csv"):
                df = pd.read_csv(full_path)
            else:
                df = pd.read_json(full_path)

            X = df.iloc[:, :-1]
            y = df.iloc[:, -1]

            model_cls = MODEL_REGISTRY.get(model_type)
            if not model_cls:
                raise ValueError(f"Model {model_type} not found")

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