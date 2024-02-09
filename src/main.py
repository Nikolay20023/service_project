import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.logger import LOGGING
from api.v1 import users, services
from core.config import app_setting

app = FastAPI(
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse
)

app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(
    services.router, prefix="/api/v1", tags=["services"])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_setting.project_host,
        port=app_setting.project_port,
    )
