import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from defects import router as defects_router
from app.db import connect_to_mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield

app = FastAPI(title='Rdmg API', lifespan=lifespan)

app.include_router(defects_router, prefix='/api/defects', tags=['Defects'])

app.mount('/', StaticFiles(directory='static', html=True), name='client')

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
