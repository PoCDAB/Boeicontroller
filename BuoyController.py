import RPi.GPIO as gpio
import json as js
import spidev

from FileOps import FileOps
from time import sleep

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)


class BuoyController:

    # GPIO led pin definition
    gpio.setup(7, gpio.OUT, initial=gpio.LOW)

    # open the SPI bus
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 100000

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.accepted_name = self.ip + ".json"
        self.f1 = FileOps(self.accepted_name)

    # read data from MCP3008
    def read_channel(self, channel):
        adc = self.spi.xfer2([1, (8+channel) << 4, 0])
        light_data = ((adc[1] & 3) << 8) + adc[2]
        return light_data

    def check_light_level(self, defaults=940):
        """check the light levels of the surrounding area. The value could be changed if deemed necessary for
        different situations"""
        return True if self.read_channel(0) > defaults else False


    def main(self):
        print("running controller")
        config = self.f1.read_config()
        while True:
            light_level = config["light_lvl"]
            on_time = config["on_time"]
            off_time = config["off_time"]

            if self.check_light_level(light_level):
                gpio.output(7, gpio.HIGH)
                sleep(on_time)
            gpio.output(7, gpio.LOW)
            sleep(off_time)


print("creating object")
buoy = BuoyController("10.0.0.1", 4242)
print("running main")
buoy.main()

