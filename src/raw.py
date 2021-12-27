from typing import List
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from datetime import datetime
from src.schemas import User
from uuid import uuid4

app = FastAPI(
    title="Access Suite API"
)

# Connect to Database
while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='access_suite', user='postgres', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfully")

        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(6)

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


@app.get("/posts")
def index():
    cursor.execute(""" SELECT * FROM users """)
    users = cursor.fetchall()
    return {"data": users}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    cursor.execute(""" INSERT INTO users (id, name, created_at, updated_at) VALUES (%s, %s, %s, %s) RETURNING * """,
                   (str(uuid4()), user.name, datetime.now(), datetime.now()))

    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM users WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return {"data": post}


@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, user: User):
    cursor.execute(""" UPDATE users SET name = %s WHERE id = %s RETURNING * """, (user.name, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM users WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return {"data": "post deleted"}
