# Boeicontroller
Part of PoC DAB as a sub-project which is made to control buoys at sea using a Raspberry Pi 4, a Nooelec NESDR SMART dab stick (realtek chiplet) and a simple antenna.
The DABreceiver of the [project Data-transmission](https://github.com/PoCDAB/Data-transmission) __has been modified__ in order to work with the OO paradigm. 
Feel free to use it in your own OO implementation however you see fit.

I've included the [DAB cmdline scanner](https://github.com/JvanKatwijk/dab-cmdline) for convenience's sake, use it to scan the specturm whenever you think that you 
don't seem to receive anything. Compiling the cmdline scanner is out of the scope of this project, use the respective [GitHub page](https://github.com/JvanKatwijk/dab-cmdline), 
as the documentation over there should be sufficient in order to set it up.


## setup
Run the ./setup.sh to install all the necessary packages. If all goes well, you should be able to instantly run the project.
If not, open an issue and I'll get in touch with you (fingers crossed).

## executing the main components
simply input ```sudo ./Boeicontroller/run_buoy_rec.sh``` in your cmd. After doing that you'll be prompted with a specific ensemble, during my project, this was 7D. It might or might
not be subject to change. Contact your corresponding RF supplier for more information regarding their ensemble.  

## executing the scanner
``` sudo ./run_scan.sh```... -nuff said

Good luck!
