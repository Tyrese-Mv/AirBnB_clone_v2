#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os

class DBStorage:
    __engine = None
    __session = None
    """This class manages storage of hbnb models in Database"""

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('HBNB_MYSQL_USER'),
            os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            os.getenv('HBNB_MYSQL_DB')
        ), pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        object = {}
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                objKey = "{}.{}".format(type(obj).__name__, obj.id)
                object[objKey] = obj
        else:
            for cls in [User, State, City, Amenity, Place, Review]:
                query = self.__session.query(cls).all()
                for obj in query:
                    objKey = "{}.{}".format(type(obj).__name__, obj.id)
                object[objKey] = obj
        return object

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
