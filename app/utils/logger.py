import logging
from fastapi import Request, Response

# Setup logging configuration
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


async def log_request(request: Request, call_next):
    response: Response = await call_next(request)

    # Log the required info
    log_data = {
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
    }
    logging.info(log_data)

    return response
