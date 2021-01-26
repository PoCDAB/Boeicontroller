#!/bin/bash

echo installing the required libraries......
sleep 2

sudo apt-get update
sudo apt-get install python3-pip python3-autopep8 librtlsdr-dev fftw3 cmake g++ pkg-config autoconf libtins-dev libboost-dev git gnuradio-dev libasio-dev 
sudo pip3 install RPi.GPIO spidev
sudo apt-get update

echo cloning the required repos.....
sleep 2

sudo git clone https://github.com/PoCDAB/Boeicontroller.git
sudo git clone https://github.com/PoCDAB/Data-transmission.git
sudo git clone https://github.com/JvanKatwijk/dab-cmdline.git
sudo git clone git://git.osmocom.org/rtl-sdr.git

echo installing the DAB-stick library....
sleep 2

cd rtl-sdr/
sudo mkdir build
cd build
sudo cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON
sudo make
sudo make install
sudo ldconfig
cd ..
sudo rm -rf build

cd

echo installing the DAB-commandline scanner...
cd dab-cmdline/dab-scanner
sudo mkdir build
cd build
sudo cmake .. -DRTLSDR=ON
sudo make
sudo make install
echo the scanner is located \in /usr/local/bin\!

cd

echo installing the receiver..
sleep 2

cd Data-transmission
sudo mkdir build
cd build
sudo cmake ..
sudo cmake --build .

echo the installation has been finished.
