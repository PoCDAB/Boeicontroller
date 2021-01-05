import RPi.GPIO as gpio
import ast
import json
import os
import re
import socket
import spidev
from time import sleep

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

ip = "10.0.0.1"
port = 4242
first_run = True

# GPIO led pin definition
gpio.setup(7, gpio.OUT, initial=gpio.LOW)

# open the SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000


# read data from MCP3008
def read_channel(channel):
    adc = spi.xfer2([1, (8+channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def check_light_level(defaults=940):
    """check the light levels of the surrounding area. The value could be changed if deemed necessary for
    different situations""" 
    return True if read_channel(0) > defaults else False


def receive_data():
    """listen to the receiver with the predefined data which correspond to the receiver's data"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    data, addr = sock.recvfrom(4096)

    # returns a list with values from the transmission if the regex checks out
    return ast.literal_eval(data.decode('utf-8')) if re_ops(data) else False


def re_ops(transmission):
    """checks the DAB transmission for a list which contains the following format: 
    [123, 1 optional 2 optional 3, 1 optional 2 optional 3]"""
    pattern = re.compile(b"\\[\\d\\d\\d,\\d\\d?\\d?,\\d\\d?\\d?\\]")
    return True if re.search(pattern, transmission) else False


def check_json(write=False, light_lvl=940, on_time=5, off_time=10):
    """check_json checks whether there's an existing config on the machine and in the same folder/location
    if it does exist, it gets returned to the caller. If it doesn't exist, a new file will be created 
    with preset data in order for the buoy to function. Overwrite the """
    file = "config.json"
    if os.path.isfile(file):
        if write:
            with open(file, "r+") as json_data:  # update the existing values and save them
                config_data = js.load(json_data)
                config_data["light_lvl"] = light_lvl
                config_data["on_time"] = on_time
                config_data["off_time"] = off_time
                json_data.seek(0)
                json_data.truncate()
                js.dump(config_data, json_data, indent=2)
        else:
            json_data = open(file, "r")
            dict_data = js.load(json_data)
            config_data = [dict_data["light_lvl"],
                            dict_data["on_time"], dict_data["off_time"]]
            json_data.close()
            return config_data
    # create new with presets if json config does not exist
    else:
        json_data = open(file, "w")
        dict_data = {"light_lvl": light_lvl, "on_time": on_time, "off_time": off_time}
        js.dump(dict_data, json_data, indent=2)
        json_data.flush()
        json_data.close()
        return check_json()


def compare_transmission():
    """function for checking if the existing transmission contains similar data compared to
    the newly received data. If the data differs, update the config file"""
    dab_transmission = receive_data()
    existing_data = check_json()

    if dab_transmission == existing_data:
        return existing_data
    else:
        check_json(True, dab_transmission[0],
                   dab_transmission[1], dab_transmission[2])


def main():
    while True:
        dab_data = compare_transmission()
        
        light_level = dab_data[0]
        on_time = dab_data[1]
        off_time = dab_data[2]

        if check_light_level(light_level):
            gpio.output(7, gpio.HIGH)
            sleep(on_time)
        gpio.Output(7, gpio.LOW)
        sleep(off_time)
