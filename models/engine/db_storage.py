#!/usr/bin/python3
"""This module defines the DBStorage class for HBNB project"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DBStorage:
    """A class for database storage."""
    __engine = None
    __session = None

    obj_cls = {
        "User": User,
        "BaseModel": BaseModel,
        "State": State,
        "Place": Place,
        "City": City,
        "Review": Review,
        "Amenity": Amenity
    }

    db_dict = {}

    def __init__(self):
        """Initializes a new DBStorage instance."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage."""
        if cls is not None:
            if isinstance(cls, str) and cls in self.obj_cls:
                cls = self.obj_cls[cls]
            return {k: v for k, v in self.db_dict.items() if isinstance(v, cls)}
        return self.db_dict

    def new(self, obj):
        """Adds a new model to the database session."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.db_dict[key] = obj

    def save(self):
        """Commits all changes to the database."""
        self.__session.commit()

    def reload(self):
        """Reloads models from the database."""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

        session = self.__session()

        for cls in self.obj_cls.values():
            for instance in session.query(cls):
                key = "{}.{}".format(type(instance).__name__, instance.id)
                self.db_dict[key] = instance

        session.close()