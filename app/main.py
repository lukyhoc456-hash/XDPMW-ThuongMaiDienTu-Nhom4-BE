import logging

import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.api_router import router
from app.models import Base
from app.db.base import engine
from app.core.config import settings
from app.helpers.exception_handler import CustomException, http_exception_handler

# # logging.config.fileConfig(settings.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, docs_url="/docs", redoc_url='/re-docs',
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        description='''
        Base frame with FastAPI micro framework + Postgresql
            - Login/Register with JWT
            - Permission
            - CRUD User
            - Unit testing with Pytest
            - Dockerize
        '''
    )
    cors_origins = settings.BACKEND_CORS_ORIGINS
    if isinstance(cors_origins, str):
        if cors_origins.startswith("[") and cors_origins.endswith("]"):
            import json
            try:
                allow_origins = json.loads(cors_origins)
            except Exception:
                allow_origins = [i.strip() for i in cors_origins.split(",")]
        else:
            allow_origins = [i.strip() for i in cors_origins.split(",")]
    elif isinstance(cors_origins, list):
        allow_origins = [str(origin) for origin in cors_origins]
    else:
        allow_origins = [str(cors_origins)]

    cors_kwargs = {
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
    if "*" in allow_origins or not allow_origins:
        logging.warning("CORS: Allowing all origins via regex due to '*' in BACKEND_CORS_ORIGINS")
        cors_kwargs["allow_origin_regex"] = r"https?://.*"
    else:
        cors_kwargs["allow_origins"] = allow_origins

    application.add_middleware(CORSMiddleware, **cors_kwargs)
    application.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    application.include_router(router, prefix=settings.API_PREFIX)
    application.add_exception_handler(CustomException, http_exception_handler)

    return application


app = get_application()
# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000)
