import grpc
import json
from concurrent import futures
from proto import service_pb2, service_pb2_grpc
from app.ml.service import MLServiceLogic
from app.services.dvc_manager import DVCManager
from app.logger import get_logger

logger = get_logger(__name__)

class MLGrpcServicer(service_pb2_grpc.MLServiceServicer):
    def __init__(self):
        self.ml_logic = MLServiceLogic()
        self.dvc = DVCManager()

    def HealthCheck(self, request, context):
        return service_pb2.HealthResponse(status="ok")

    def GetAvailableModels(self, request, context):
        models = self.ml_logic.get_available_models()
        return service_pb2.ModelList(models=models)

    def ListDatasets(self, request, context):
        datasets = self.dvc.list_files()
        return service_pb2.DatasetList(datasets=datasets)

    def UploadDataset(self, request, context):
        try:
            self.dvc.add_and_push(request.filename, request.content)
            return service_pb2.UploadResponse(filename=request.filename, status="uploaded and tracked")
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.UploadResponse()

    def TrainModel(self, request, context):
        try:
            params = json.loads(request.hyperparameters_json)
            task_id = self.ml_logic.train(request.model_type, request.dataset_path, params)
            return service_pb2.TrainResponse(model_id=task_id, status="success")
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return service_pb2.TrainResponse()
        except FileNotFoundError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return service_pb2.TrainResponse()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.TrainResponse()

    def Predict(self, request, context):
        try:
            predictions = self.ml_logic.predict(request.model_id, [list(request.features)])
            return service_pb2.PredictResponse(predictions=predictions)
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return service_pb2.PredictResponse()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.PredictResponse()

    def DeleteModel(self, request, context):
        try:
            self.ml_logic.delete_model(request.model_id)
            return service_pb2.DeleteResponse(status="deleted")
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return service_pb2.DeleteResponse()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.DeleteResponse()


def serve_grpc_server(port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MLServiceServicer_to_server(MLGrpcServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info(f"gRPC server started on port {port}")
    server.wait_for_termination()