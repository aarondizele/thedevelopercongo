from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    description: Optional[str] = None
    published: Optional[bool] = True