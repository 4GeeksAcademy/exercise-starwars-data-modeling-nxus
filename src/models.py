from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    favorites = relationship('Favorite', back_populates='user')

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=True)
    homeworld_id = Column(Integer, ForeignKey('planets.id'))
    
    homeworld = relationship('Planet', back_populates='characters')

class Planet(Base):
    __tablename__ = 'planets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    climate = Column(String, nullable=True)
    terrain = Column(String, nullable=True)
    
    characters = relationship('Character', back_populates='homeworld')

class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    character_id = Column(Integer, ForeignKey('characters.id'))
    planet_id = Column(Integer, ForeignKey('planets.id'))
    
    user = relationship('User', back_populates='favorites')
    character = relationship('Character')
    planet = relationship('Planet')


engine = create_engine('sqlite:///starwars_blog.db')
Base.metadata.create_all(engine)
