from sqlalchemy import Boolean, Column, String, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base
import uuid
# from src.utils import UUID


class User(Base):
    __tablename__ = "users"

    # id = Column(Integer, primary_key=True, index=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), index=True, unique=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    hashed_password = Column(String)

    blogs = relationship("Blog", back_populates="creator")


class Blog(Base):
    __tablename__ = "blog"
    
    # id = Column(Integer, primary_key=True, index=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255))
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="blogs")


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item", back_populates="owner")


# class Item(Base):
#      __tablename__ = "items"

#      id = Column(Integer, primary_key=True, index=True)
#      title = Column(String, index=True)
#      description = Column(String, index=True)
#      owner_id = Column(Integer, ForeignKey("users.id"))

#      owner = relationship("User", back_populates="items")

