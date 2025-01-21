from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings

from api import router as api_router
from db.models import Base
from db.models.db_helper import db_helper


@asynccontextmanager
async def lifespan(application: FastAPI):

    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    yield

    await db_helper.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.get("/")
async def check_life():
    return {"status": "ok"}


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)
