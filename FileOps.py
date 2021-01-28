import json as js

from os import remove
from os.path import isfile


class FileOps:


    def __init__(self, file_name: str):
        self.file_name = file_name + ".json"


    def save_config(self):
        if self.check_new():
            with open("config.json", "w") as file:
                js.dump(self.pass_new(), file, indent=2)
                remove(self.file_name)


    def read_config(self):
        with open("config.json", "r") as file:
            json_string = ""
            for line in file:
                json_string += line
            return js.loads(json_string)


    def pass_new(self):
        if self.check_new():
            with open(self.file_name, "r") as file:
                json_string = ""
                for line in file:
                    json_string += line
                return js.loads(json_string)


    def check_new(self):
        return True if isfile(self.file_name) else False
             
f1 = FileOps("10.0.0.1")
print(f1.read_config())
print(type(f1.read_config()))
print(f1.save_config())