# import uvicorn
from fastapi import Depends, FastAPI, status, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from src.routers import users, blogs, authenticate
from src import models, schemas
from src.database import Database
from dotenv import load_dotenv


app = FastAPI(
    docs_url="/openapi",
    redoc_url="/openapi_redoc",
    title="The Developers Congo",
    description="This is an OpenAPI for The Developers Congo Platform",
    version="1.0.1",
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

# Load Local Environment
load_dotenv()

@app.on_event('startup')
async def startup():
    Database.create_db_and_tables()

@app.on_event('shutdown')
async def shutdown():
    pass # await database.disconnect()

@app.post("/create-posts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": "successfully created posts", "data": f"title {payload['title']}, content {payload['content']}"}

# if task_id not in tasks:
#   type(task_id)
#   len(tasks)
#   tasks[task_id] = "This did'nt exist before"
#


# ALTER TABLE public.users DROP COLUMN created_at;
# ALTER TABLE public.users ADD COLUMN created_at timestamp with time zone;

# alembic revision -m "create model tables v1" --autogenerate
# alembic revision <revision_name>
# alembic current
# alembic heads
# alembic upgrade head
# alembic revision --autogenerate -m "<message>"

# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port=9000)
