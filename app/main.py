from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from app.routers import user_router
from app.utils.logger import log_request
from app.utils.memory_db import load_data_into_memory, save_data_to_json
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_data_into_memory()
    yield


app = FastAPI(title="User Management API", version="1.0.0", lifespan=lifespan)


# Attach the custom logger to every backend request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    return await log_request(request, call_next)


# Custom exception handler for RequestValidationError from models
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract just the `msg` from each error in exc.errors()
    error_messages = [err["msg"] for err in exc.errors()]

    # If there's only one error, return it as a single string else join them
    if len(error_messages) == 1:
        message = error_messages[0]
    else:
        message = "; ".join(error_messages)

    # Return a simplified JSON with a single detail string
    return JSONResponse(status_code=422, content={"detail": message})


app.include_router(user_router.router, prefix="/users", tags=["Users"])
