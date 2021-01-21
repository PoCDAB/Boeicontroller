import RPi.GPIO as gpio
import ast
import json as js
import os
import re
import socket
import spidev

from DABreceiver import DABreceiver 
from time import sleep

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)


class BuoyController:
    
    ip = None
    port = None
    first_run = True
    accepted_name = ip + ".json"

    # GPIO led pin definition
    gpio.setup(7, gpio.OUT, initial=gpio.LOW)

    # open the SPI bus
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 100000


    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.ip = port
        self.DAB = DABreceiver(self.ip, self.ip)
        
    # read data from MCP3008
    def read_channel(self, channel):
        adc = spi.xfer2([1, (8+channel) << 4, 0])
        light_data = ((adc[1] & 3) << 8) + adc[2]
        return light_data

    def check_light_level(self, defaults=940):
        """check the light levels of the surrounding area. The value could be changed if deemed necessary for
        different situations""" 
        return True if self.read_channel(0) > defaults else False


    def check_json(self, source:str, write=False, light_lvl=940, on_time=5, off_time=10):
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
                    json_data.seek(0)
                    json_data.truncate()
                    js.dump(source, json_data, indent=2)
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
            dict_data = {"light_lvl": light_lvl, "on_time": on_time, "off_time": off_time}
            js.dump(dict_data, json_data, indent=2)
            json_data.flush()
            json_data.close()
            return check_json()


    def compare_config(self):
        """function for checking if the existing transmission contains similar data compared to
        the newly received data. If the data differs, update the config file"""
        new_file = check_json("192.168.1.1.json")
        existing_file = check_json("config.json")    
            
        if new_file == existing_file:
            return existing_file
        else:
            check_json("config.json", True, new_file[0],
                    new_file[1], new_file[2])


    def main(self):
        while True:
            self.DAB.main()
            dab_data = compare_config()
            
            light_level = dab_data[0]
            on_time = dab_data[1]
            off_time = dab_data[2]

            if check_light_level(light_level):
                gpio.output(7, gpio.HIGH)
                sleep(on_time)
            gpio.Output(7, gpio.LOW)
            sleep(off_time)

buoy = BuoyController("10.0.0.1")
buoy.main()
