from fastapi import status, HTTPException
from typing import List, Optional
from .. import models, schemas
from ..hashing import Hash
from ..database import Database


class BlogRepository:

    def create(request: schemas.InsertBlog, db = Database.session()):
        new_blog = models.Blog(title=request.title, description=request.description, user_id=1)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog


    def all(current_user: schemas.User, db = Database.session()):
        blogs = db.query(models.Blog).filter(models.Blog.user_id == current_user.id).all()
        return blogs


    def show(id: str, db = Database.session()):
        blog = db.query(models.Blog).filter(models.Blog.id == id).first()
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

        blog.update({"title": request.title, "description": request.description})
        db.commit()

        return {"data": "updated"}