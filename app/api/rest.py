from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List
from app.ml.models import MODEL_REGISTRY
from app.services.dvc_manager import DVCManager
from app.ml.trainer import MLTrainer
from app.config import settings
import os
import shutil
import joblib
from clearml import Task

router = APIRouter()
dvc = DVCManager()
trainer = MLTrainer()


class TrainPayload(BaseModel):
    model_type: str
    dataset_name: str
    hyperparameters: Dict[str, Any]


class PredictPayload(BaseModel):
    model_id: str
    features: List[List[float]]


@router.get("/health")
def health_check():
    """Checks service health."""
    return {"status": "ok"}


@router.get("/models/list")
def list_model_classes():
    """Returns available model classes for training."""
    return {"models": list(MODEL_REGISTRY.keys())}


@router.get("/datasets/list")
def list_datasets():
    """Returns list of datasets tracked by DVC."""
    return {"datasets": dvc.list_files()}


@router.post("/datasets/upload")
def upload_dataset(file: UploadFile = File(...)):
    """Uploads a dataset (CSV/JSON) and tracks it with DVC."""
    file_location = os.path.join(settings.DATA_DIR, file.filename)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    dvc.add_and_push(file.filename)
    return {"filename": file.filename, "status": "uploaded and tracked"}


@router.post("/train")
def train_model(payload: TrainPayload):
    """Starts a training job logged in ClearML."""
    if payload.model_type not in MODEL_REGISTRY:
        raise HTTPException(status_code=400, detail="Model type not supported")

    try:
        task_id = trainer.train(payload.model_type, payload.dataset_name, payload.hyperparameters)
        return {"task_id": task_id, "status": "training_completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict")
def predict(payload: PredictPayload):
    """Predicts using a model downloaded from ClearML."""
    try:
        # Retrieve task and model
        task = Task.get_task(task_id=payload.model_id)
        model_artifact = task.artifacts['model'].get_local_copy()

        loaded_model = joblib.load(model_artifact)
        predictions = loaded_model.predict(payload.features)
        return {"predictions": predictions.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))