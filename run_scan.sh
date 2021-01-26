#!/bin/bash
cd /usr/local/bin

echo Enter the ensemble \(like 5A or 13F\) to start scanning \(the scanner goes through the list and skips the ones below the input ensemble\)

read ensemble
sudo dab-scanner-rtlsdr -C $ensemble
