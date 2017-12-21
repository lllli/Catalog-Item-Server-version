from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

base = declarative_base()

def curr_time():
    return datetime.datetime.now()

class User(base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Platform(base):
    __tablename__ = 'platform'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    date = Column(DateTime, default=curr_time,onupdate=curr_time)
    def __init__(self, name):
        self.name = name

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }

class Game(base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(), nullable=False)
    cover = Column(String(250), nullable=False)
    release = Column(String(250),nullable=False)
    platform_id = Column(Integer, ForeignKey('platform.id'))
    platform = relationship(Platform)
    date = Column(DateTime, default=curr_time,onupdate=curr_time)

    def __init__(self, title, description, cover, release, platform_id):
        self.title = title
        self.description = description
        self.cover = cover
        self.release = release
        self.platform_id = platform_id

    @property
    def serialize(self):
        """Return serializeable format of the CategoryItem Object"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'cover': self.cover,
            'release': self.release,
        }

engine = create_engine('postgresql://catalog:password@localhost/catalog')
base.metadata.create_all(engine)
