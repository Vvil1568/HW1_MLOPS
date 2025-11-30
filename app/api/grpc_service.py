import grpc
import json
from concurrent import futures
from proto import service_pb2, service_pb2_grpc
from app.ml.models import MODEL_REGISTRY
from app.ml.trainer import MLTrainer
from app.core.logger import get_logger
import joblib
from clearml import Task

logger = get_logger(__name__)


class MLService(service_pb2_grpc.MLServiceServicer):
    def GetAvailableModels(self, request, context):
        return service_pb2.ModelList(models=list(MODEL_REGISTRY.keys()))

    def TrainModel(self, request, context):
        trainer = MLTrainer()
        try:
            params = json.loads(request.hyperparameters_json)
            task_id = trainer.train(request.model_type, request.dataset_path, params)
            return service_pb2.TrainResponse(model_id=task_id, status="success")
        except Exception as e:
            logger.error(f"gRPC Train Error: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.TrainResponse()

    def Predict(self, request, context):
        try:
            task = Task.get_task(task_id=request.model_id)
            model_path = task.artifacts['model'].get_local_copy()
            model = joblib.load(model_path)

            # Reshape for single sample prediction
            prediction = model.predict([list(request.features)])[0]
            return service_pb2.PredictResponse(prediction=prediction)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.PredictResponse()


def serve(port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MLServiceServicer_to_server(MLService(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info(f"gRPC server started on port {port}")
    server.wait_for_termination()