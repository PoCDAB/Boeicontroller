import RPi.GPIO as GPIOimport 
import spidev
import time
import os
import ast 
import re
import mmap

from time import sleep

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

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

# arbitrary light level check for the LDR sensor
def check_light_level(defaults=940):
    return True if read_channel(0) > defaults else False

# function to find the specific line of code in a transmission from the receiver
def instructons_ops():
    pattern = re.compile(b"\\[\\d\\d\\d,\\d\\d?\\d?,\\d\\d?\\d?\\]") 
    w
    with open('receiver_transmission.txt', 'rb', 0) as file,\
    mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
        if re.search(pattern, s):
            data = s[:9]
            return ast.literal_eval(data.decode('utf-8')) # list format: [light level, on-time, off-time]

# function to prevent the receiver_transmission.txt to go out of control in size
def file_ops():
    if os.path.isfile('receiver_transmission.txt'):
        if os.stat('receiver_transmission.txt') > 1024:
            os.remove('receiver_transmission.txt')


def main(defaults=25):
    while True:
        if check_light_level():
            gpio.output(7, gpio.HIGH)
            sleep(defaults - 20])
        gpio.Output(7, gpio.LOW)
        sleep(defaults)

