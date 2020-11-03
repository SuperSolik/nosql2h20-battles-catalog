import os
import shutil

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .views import router, error_response


def create_app():
    origins = [
        "http://localhost",
        "http://localhost:4200",
    ]

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    if os.path.exists(settings.TEMP_DIR):
        shutil.rmtree(settings.TEMP_DIR)

    os.mkdir(settings.TEMP_DIR)


@app.on_event("shutdown")
async def shutdown_event():
    shutil.rmtree(settings.TEMP_DIR)


@app.exception_handler(Exception)
async def exception_handler(r: Request, e: Exception):
    return error_response('Server error, something went wrong')
