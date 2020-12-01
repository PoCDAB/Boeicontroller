import RPi.GPIO as GPIOimport 
import spidev
import time
import os
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
def check_light_level():
    return True if read_channel(0) > 940 else False

def file_ops():
    with open('receiver_transmission.txt', 'r') as f:
        contents = f.read()
        instruct
        pass #TODO put the specific data here which should be read and passed to the variables
        
#format lightlevel eg 940, on delay 4, sleep delay,


while True:
    if check_light_level():
        gpio.output(, gpio.HIGH)
        sleep()
    gpio.Output(7, gpio.LOW)
    sleep(30)

