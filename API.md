# API Documentation

## REST Endpoints

### Health Check
- **Endpoint**: `GET /health`
- **Description**: Check if the service is running
- **Response**:
  ```json
  {
    "status": "ok"
  }
  ```

### List Available Models
- **Endpoint**: `GET /models/list`
- **Description**: Get list of available model types
- **Response**:
  ```json
  {
    "models": ["knn", "logistic_regression", "random_forest"]
  }
  ```

### Delete Model
- **Endpoint**: `DELETE /models/{model_id}`
- **Description**: Delete a trained model from ClearML
- **Response**:
  ```json
  {
    "status": "deleted",
    "model_id": "<model_id>"
  }
  ```

### List Datasets
- **Endpoint**: `GET /datasets/list`
- **Description**: List available datasets in DVC
- **Response**:
  ```json
  {
    "datasets": ["dataset1.csv", "dataset2.json"]
  }
  ```

### Upload Dataset
- **Endpoint**: `POST /datasets/upload`
- **Description**: Upload a dataset file to DVC
- **Request**: Multipart form with file field
- **Response**:
  ```json
  {
    "filename": "dataset.csv",
    "status": "uploaded and tracked"
  }
  ```

### Train Model
- **Endpoint**: `POST /train`
- **Description**: Train a new model
- **Request Body**:
  ```json
  {
    "model_type": "random_forest",
    "dataset_name": "dataset.csv",
    "hyperparameters": {
      "n_estimators": 100,
      "max_depth": 5
    }
  }
  ```
- **Response**:
  ```json
  {
    "task_id": "<clearml_task_id>",
    "status": "training_completed"
  }
  ```

### Single Prediction
- **Endpoint**: `POST /predict`
- **Description**: Make a single prediction using a trained model
- **Request Body**:
  ```json
  {
    "model_id": "<clearml_task_id>",
    "features": [[0.1, 0.2, 0.3]]
  }
  ```
- **Response**:
  ```json
  {
    "predictions": [0.5]
  }
  ```

### Batch Prediction (NEW)
- **Endpoint**: `POST /predict/batch`
- **Description**: Make predictions on multiple samples from a CSV file
- **Request**: Multipart form with file field (CSV file containing features)
- **Response**:
  ```json
  {
    "predictions": [0.1, 0.2, 0.3]
  }
  ```
- **CSV Format**: CSV file should contain one row per sample, with each column representing a feature. The model will predict for each row.
- **Example CSV**:
  ```
  0.1,0.2,0.3
  0.4,0.5,0.6
  0.7,0.8,0.9
  ```

## gRPC Service

The gRPC service provides the same functionality as REST endpoints via protocol buffers.

### Available Methods
- `HealthCheck`: Check service health
- `GetAvailableModels`: List available model types
- `ListDatasets`: List available datasets
- `UploadDataset`: Upload a dataset
- `TrainModel`: Train a new model
- `Predict`: Make a single prediction
- `PredictBatch`: Make batch predictions (NEW)
- `DeleteModel`: Delete a trained model

### Proto Definition
See `proto/service.proto` for detailed message definitions.

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK`: Success
- `400 Bad Request`: Invalid input data
- `404 Not Found`: Model or dataset not found
- `500 Internal Server Error`: Unexpected server error
