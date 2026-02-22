from typing import Dict, Any, List

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel

from app.ml.service import MLServiceLogic
from app.services.dvc_manager import DVCManager

router = APIRouter()

class TrainPayload(BaseModel):
    model_type: str
    dataset_name: str
    hyperparameters: Dict[str, Any]

class PredictPayload(BaseModel):
    model_id: str
    features: List[List[float]]

def get_ml_service() -> MLServiceLogic:
    return MLServiceLogic()

def get_dvc_manager() -> DVCManager:
    return DVCManager()


@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/models/list")
def list_model_classes(ml_service: MLServiceLogic = Depends(get_ml_service)):
    return {"models": ml_service.get_available_models()}

@router.delete("/models/{model_id}")
def delete_model(model_id: str, ml_service: MLServiceLogic = Depends(get_ml_service)):
    try:
        ml_service.delete_model(model_id)
        return {"status": "deleted", "model_id": model_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/datasets/list")
def list_datasets(dvc: DVCManager = Depends(get_dvc_manager)):
    return {"datasets": dvc.list_files()}

@router.post("/datasets/upload")
async def upload_dataset(file: UploadFile = File(...), dvc: DVCManager = Depends(get_dvc_manager)):
    try:
        content = await file.read()
        dvc.add_and_push(file.filename, content)
        return {"filename": file.filename, "status": "uploaded and tracked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/train")
def train_model(payload: TrainPayload, ml_service: MLServiceLogic = Depends(get_ml_service)):
    try:
        task_id = ml_service.train(payload.model_type, payload.dataset_name, payload.hyperparameters)
        return {"task_id": task_id, "status": "training_completed"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict")
def predict(payload: PredictPayload, ml_service: MLServiceLogic = Depends(get_ml_service)):
    try:
        predictions = ml_service.predict(payload.model_id, payload.features)
        return {"predictions": predictions}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))