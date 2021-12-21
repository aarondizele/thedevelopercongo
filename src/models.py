from sqlalchemy import Boolean, Column, String, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import relationship
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    email = Column(String(255))
    hashed_password = Column(String)

    blogs = relationship("Blog", back_populates="creator")


class Blog(Base):
    __tablename__ = "blog"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="blogs")
    

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

