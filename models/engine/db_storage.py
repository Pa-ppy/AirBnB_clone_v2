#!/usr/bin/python3
"""DBStorage module"""
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
import os


class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a DBStorage object"""
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")
        self.__engine = create_engine(f"mysql+mysqldb://{user}:\
                {pwd}@{host}/{db}", pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries on the database session"""
        if cls:
            return {f"{obj.__class__.__name__}.{obj.id}":
                    obj for obj in self.__session.query(cls).all()}
        else:
            result = {}
            for cls in [State, City]:
                result.update({f"{obj.__class__.__name__}.{obj.id}":
                               obj for obj in self.__session.query(cls).all()})
            return result

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and initializes session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Calls remove() method on the private session attribute"""
        self.__session.remove()
