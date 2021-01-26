#!/bin/bash

echo Enter the ensemble \(eg 5A\) to tune \in to

read ensemble
sudo ./Data-transmission/build/products/bin/receiver 10.0.0.1 1000 $ensemble &
