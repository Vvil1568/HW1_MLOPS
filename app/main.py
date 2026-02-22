from threading import Thread

import uvicorn
from fastapi import FastAPI

from app.api.grpc_service import serve_grpc_server
from app.api.rest import router
from app.config import settings
from app.logger import get_logger

logger = get_logger("main")

app = FastAPI(title="MLOps HW1 API", description="REST + gRPC ML Service")
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    t = Thread(target=serve_grpc_server, args=(settings.GRPC_PORT,), daemon=True)
    t.start()
    logger.info("Background gRPC thread started")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)