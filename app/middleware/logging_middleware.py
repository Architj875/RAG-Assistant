import time

from fastapi import Request

from app.utils.logger import logger

async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    logger.info(
        "Incoming Request: %s %s",
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        "Completed: %s %s -> %d (%.3f sec)",
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )

    return response