echo Enter the ensemble\(eg 5A\)
read ensemble
sudo ./Data-transmission/build/products/bin/receiver 10.0.0.1 1000 $ensemble &

sleep 3

cd Boeicontroller

sudo python3 DABreceiver.py &
sudo python3 BuoyController.py
