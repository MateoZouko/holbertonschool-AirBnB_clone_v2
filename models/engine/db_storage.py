from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(os.getenv('HBNB_MYSQL_USER'),
                                             os.getenv('HBNB_MYSQL_PWD'),
                                             os.getenv('HBNB_MYSQL_HOST', 'localhost'),
                                             os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        obj_cls = {"User": User, "State": State, "City": City,
                   "Amenity": Amenity, "Place": Place, "Review": Review}
        db_dict = {}

        if cls is not None:
            query = self.__session.query(obj_cls[cls]).all()
            for obj in query:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dict[key] = obj
        else:
            for cls_name, cls_type in obj_cls.items():
                if cls_name != "BaseModel":
                    query = self.__session.query(cls_type).all()
                    for obj in query:
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        db_dict[key] = obj
        return db_dict

    def new(self, obj):
        if obj:
            self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        self.__session.close()