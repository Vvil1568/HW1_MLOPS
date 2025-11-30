import asyncio
import uvicorn
from fastapi import FastAPI
from app.api import rest, grpc_service
from app.core.config import settings
from app.core.logger import get_logger
from threading import Thread

logger = get_logger("main")

app = FastAPI(title="MLOps HW1 API", description="REST + gRPC ML Service")
app.include_router(rest.router, prefix="/api/v1")

def run_grpc():
    grpc_service.serve(settings.GRPC_PORT)

@app.on_event("startup")
async def startup_event():
    # Run gRPC in a separate thread
    t = Thread(target=run_grpc, daemon=True)
    t.start()
    logger.info("Background gRPC thread started")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)