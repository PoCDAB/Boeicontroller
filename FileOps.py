import json as js

from os import remove
from os.path import isfile


class FileOps:


    def __init__(self, file_name: str):
        self.file_name = file_name
        self.config_name = "config.json"
        self.preset_config = {"light_lvl" : 940, "on_time" : 1, "off_time" : 2}


    def save_config(self):
        "saves the newer config file and deletes it in order to avoid clutter."
        if isfile(self.file_name):
            with open(self.config_name, "w") as file:
                js.dump(self.pass_new(), file, indent=2)
                remove(self.file_name) # delete the newly arrived config to prevent clutter


    def read_config(self):
        """pass the existing config over to the caller if present. 
        Creates a preset config using the field "preset_config" if config.json doesn't exist """
        if not isfile(self.config_name):
            with open(self.config_name,"w") as file:
                js.dump(self.preset_config, file, indent=2)
                return self.preset_config # return the preset config for now
        with open(self.config_name, "r") as file:
            json_string = ""
            for line in file:
                json_string += line
            return js.loads(json_string)


    def pass_new(self): 
        """checks if a new config is present and passes the data through to the caller"""
        if isfile(self.file_name):
            with open(self.file_name, "r") as file:
                json_string = ""
                for line in file:
                    json_string += line
                return js.loads(json_string) 