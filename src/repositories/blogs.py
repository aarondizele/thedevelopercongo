from fastapi import status, HTTPException
from sqlalchemy import func
from typing import List, Optional
from src import models, schemas
from src.hashing import Hash
from src.database import Database


class BlogRepository:

    def create(request: schemas.InsertBlog, db = Database.session()):
        new_blog = models.Blog(**request.dict(), user_id=1)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog


    def all(current_user: schemas.User, db = Database.session()):
        blogs = db.query(models.Blog).filter(models.Blog.user_id == current_user.id).all()
        return blogs


    def show(id: str, search: str = "", limit: int = 10, skip: int = 0, db = Database.session()):
        blog = db.query(models.Blog).filter(models.Blog.id == id).first()
        # blog = db.query(models.Vote).filter(models.Vote.post_id == id, models.Vote.user_id == id)
        # blog = db.query(models.Blog).join(models.Vote, models.Vote.post_id == models.Blog.id)
        results = db.query(models.Blog, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Blog.id).group_by(models.Blog.id).filter(models.Blog.title.contains(search)).limit(limit).offset(skip).all()

        if not blog:
            raise HTTPException(status_code=404, detail=f"Blog with the id {id} not found")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'data': f'Blog with the id {id} not found'}
        return blog


    def delete(id: str, db = Database.session()):
        blog = db.query(models.Blog).filter(models.Blog.id == id)
        if not blog.first():
            raise HTTPException(status_code=404, detail=f"Blog with the id {id} not found")

        blog.delete(synchronize_session=False)
        db.commit()
        return {"data": f"Blog with id {id} deleted"}


    def update(id: str, request: schemas.InsertBlog, db = Database.session()):
        blog = db.query(models.Blog).filter(models.Blog.id == id)
        if not blog.first():
            raise HTTPException(status_code=404, detail=f"Blog with the id {id} not found")

        # blog.update({"title": request.title, "description": request.description})
        blog.update(request.dict(), synchronize_session=False)
        db.commit()

        return {"data": "updated"}