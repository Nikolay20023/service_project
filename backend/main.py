import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from api.v1 import users, services
from core.config import app_setting

app = FastAPI(
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse
)

origin = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(
    services.router, prefix="/api/v1", tags=["services"])


if __name__ == '__main__':
    logger.info("Bot starting...")
    uvicorn.run(
        'main:app',
        host=app_setting.project_host,
        port=app_setting.project_port,
    )
