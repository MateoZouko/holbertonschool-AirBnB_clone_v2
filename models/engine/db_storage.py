#!/usr/bin/python3
"""This is the DB storage a"""


from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel
from os import getenv


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        u = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        ht = getenv('HBNB_MYSQL_HOST', default='localhost')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine(f'mysql+mysqldb://{u}:{pwd}@{ht}/{db}')
        self.reload()

        """Drop all tables if in test environment"""
        if env == 'test':
            BaseModel.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        from models import base_model
        result = {}
        classes = [State, City, User, Place, Review, Amenity]

        if cls:
            classes = [cls]

        for class_obj in classes:
            objects = self.__session.query(class_obj).all()
            for obj in objects:
                key = f"{obj.__class__.__name__}.{obj.id}"
                result[key] = obj

        return result

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        self.__session.close()
