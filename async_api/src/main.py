import logging

import uvicorn
from api.v1 import film, genre, person
from core.logger import LOGGING
from core.middleware import apply_middleware
from db import connections
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    title="Read-only API for movie theater",
    description="Info about movies, genres and people",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    await connections.init_connectons()


@app.on_event("shutdown")
async def shutdown():
    await connections.close_connections()


# plug in router to a server with prefix /v1/film
# tag for comfortable navitagion through docs
app.include_router(film.router, prefix="/api/v1/film", tags=["film"])
app.include_router(person.router, prefix="/api/v1/person", tags=["person"])
app.include_router(genre.router, prefix="/api/v1/genre", tags=["genre"])
apply_middleware(app=app)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
