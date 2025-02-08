#!/usr/bin/python3
""" FileStorage module for managing file-based storage of objects """

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Handles storage of all class instances in a JSON file"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary of objects, optionally filtered by class."""
        if cls:
            return {k: v for k, v in self.__objects.items()
                    if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            temp = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for k, v in temp.items():
                    cls_name = v["__class__"]
                    self.__objects[k] = eval(cls_name)(**v)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from storage if it exists."""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def close(self):
        """Method to deserialize JSON file to objects"""
        self.reload()
