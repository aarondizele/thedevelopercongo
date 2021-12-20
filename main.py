import uvicorn
from fastapi import FastAPI
from typing import Optional
from models.blog import Blog

app = FastAPI()


@app.get('/')
def index():
    return {"data": {"name": "Aaron"}}


@app.get('/blog')
def get_blog(limit: int, published: bool = False, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs list of DB'}
    else:
        return {'data': f'{limit} unpublished blogs list of DB'}


@app.get('/blog/{id}')
def show_blog(id:str):
    return {"data": id}


@app.get('/blog/{id}/comments')
def comments(id: str):
    return {"data": {'1', '2'}}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished'}


@app.post('/blog')
def create_post(blog: Blog):
    return {'data': f'Blog is created with title as {blog.title}'}


# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port=9000)