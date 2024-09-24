from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    favorites = relationship('Favorite', back_populates='user')
    posts = relationship('Post', back_populates='author')

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=True)
    homeworld_id = Column(Integer, ForeignKey('planets.id'))
    description = Column(String, nullable=True)  # Additional property
    
    homeworld = relationship('Planet', back_populates='characters')
    favorites = relationship('Favorite', back_populates='character')

class Planet(Base):
    __tablename__ = 'planets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    climate = Column(String, nullable=True)
    terrain = Column(String, nullable=True)
    
    characters = relationship('Character', back_populates='homeworld')
    favorites = relationship('Favorite', back_populates='planet')

class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    character_id = Column(Integer, ForeignKey('characters.id'))
    planet_id = Column(Integer, ForeignKey('planets.id'))
    
    user = relationship('User', back_populates='favorites')
    character = relationship('Character')
    planet = relationship('Planet')

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    category = relationship('Category', back_populates='posts')

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    
    user = relationship('User')
    post = relationship('Post', back_populates='comments')

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    posts = relationship('Post', back_populates='category')

engine = create_engine('sqlite:///starwars_blog.db')
Base.metadata.create_all(engine)
