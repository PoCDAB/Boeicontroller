import os
import json as js

def check_json(source: str, write=False, light_lvl=940, on_time=5, off_time=10):
    """check_json checks whether there's an existing config on the machine and in the same folder/location
    if it does exist, it gets returned to the caller. If it doesn't exist, a new file will be created
    with preset data in order for the buoy to function. Overwrite the """
    if os.path.isfile(source):
        if write:
            with open(source, "r+") as json_data:  # update the existing values and save them
                config_data = js.load(json_data)
                config_data["light_lvl"] = light_lvl
                config_data["on_time"] = on_time
                config_data["off_time"] = off_time
                print(config_data)
                json_data.seek(0)
                json_data.truncate()
                js.dump(config_data, json_data, indent=2)
        else:
            json_data = open(source, "r")
            dict_data = js.load(json_data)
            config_data = [dict_data["light_lvl"],
                            dict_data["on_time"], dict_data["off_time"]]
            json_data.close()
            return config_data
    # create new with presets if json config does not exist
    else:
        json_data = open(source, "w")
        dict_data = {"light_lvl": light_lvl,
                        "on_time": on_time, "off_time": off_time}
        js.dump(dict_data, json_data, indent=2)
        json_data.flush()
        json_data.close()
        return check_json(source)


def compare_config():
    """function for checking if the existing transmission contains similar data compared to
    the newly received data. If the data differs, update the config file"""
    new_file = check_json("10.0.0.1.json")
    existing_file = check_json("config.json")

    if new_file == existing_file:
        return existing_file
    else:
        check_json("config.json", True, new_file[0],
                    new_file[1], new_file[2])

compare_config()