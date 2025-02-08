#!/usr/bin/python3
"""FileStorage module"""
import json
from models.base_model import BaseModel
from models.state import State
from models.city import City


class FileStorage:
    """Serializes and deserializes instances to/from a JSON file"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        with open(self.__file_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, "r") as f:
                data = json.load(f)
                for obj_data in data.values():
                    cls_name = obj_data["__class__"]
                    self.__objects[f"{cls_name}.{obj_data['id']}"] = eval
                    (cls_name)(**obj_data)
        except FileNotFoundError:
            pass

    def close(self):
        """Calls reload() method to deserialize JSON file to objects"""
        self.reload()
