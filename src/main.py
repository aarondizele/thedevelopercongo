# import uvicorn
from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.routers import users, blogs, authenticate
from src import models, schemas
from src.database import Database

# Create Database Tables
Database.init()

app = FastAPI(
    docs_url="/openapi",
    redoc_url="/openapi_redoc",
    title="The Developers Congo",
    description="This is an OpenAPI for The Developers Congo Platform",
    version="1.0.1"
)

app.include_router(authenticate.router)
app.include_router(blogs.router)
app.include_router(users.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def startup():
    pass # await database.connect()

@app.on_event('shutdown')
async def shutdown():
    pass # await database.disconnect()

# if task_id not in tasks:
#   tasks[task_id] = "This did'nt exist before"
#
# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port=9000)
