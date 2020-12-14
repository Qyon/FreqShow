FreqShow
========

![FreqShow](/sample.jpg)

Raspberry Pi &amp; PiTFT-based RTL-SDR frequency scanning and display tool.  See installation and usage instructions in the guide at: 

https://learn.adafruit.com/freq-show-raspberry-pi-rtl-sdr-scanner/overview


## UPDATE

2020-10-08
```
Install Buster Lite
Login via SSH
sudo apt update
sudo apt upgrade
sudo apt install git python3-pip python3-numpy

If using Adafruit PTFT touch screens
Follow 
https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/overview

----
If using Bangood PTFT 2.8 Resistive touch screen
Model: mzdpi-vga-zero version b
Touch: ADS7846 Touchscreen
Follow: 
http://raspberrypiwiki.com/2.8_inch_Touch_Screen_for_Pi_zero#Setup_screen_via_script_.28Recommend.29
sudo apt-get install libts0 evtest libts-bin
ls -l /dev/input
Note that /dev/fb0 or fb1, and event0 or event1 so try as needed.

Test Touch:
sudo evtest
Select ADS7846 Touchscreen
Touch around on screen 

Calibrate: 
sudo TSLIB_FBDEVICE=/dev/fb0 TSLIB_TSDEVICE=/dev/input/event1 ts_calibrate
Use pen to touch each point. Run again if necessary.
----

For both screen types, install pygame2 and SDL2:
sudo pip3 install pygame
sudo pip3 install pyrtlsdr
sudo apt install libsdl2-mixer-dev libsdl2-image-dev libsdl2-ttf-dev libportmidi-dev libfreetype6-dev

```
LIBSDL2 issue:  You need LibSDL2.0.12 or higher
If necessary build from source:
https://www.libsdl.org/download-2.0.php
cd ~
wget https://www.libsdl.org/release/SDL2-2.0.12.tar.gz
tar xvf SDL2-2.0.12.tar.gz
cd SDL2-2.0.12
./configure
make
sudo make install
sudo nano /etc/ld.so.conf.d/arm-linux-gnueabihf.conf
Add /usr/local/lib at top of file
sudo ldconfig
When you start freqshow.py you should see
pygame 2.0.0 (SDL 2.0.12, python 3.7.3)
```

Go to below to install RTL-SDR and base FreqShow:
https://learn.adafruit.com/freq-show-raspberry-pi-rtl-sdr-scanner/installation

Edit freqshow.py: (if Bangood screen)
    #os.putenv('SDL_VIDEODRIVER', 'fbcon') # Not used
    os.putenv('SDL_FBDEV'      , '/dev/fb0')
    os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
    os.putenv('SDL_MOUSEDEV'   , '/dev/input/event1')

Once installed, you need to use Python3:
cd ~/FreqShow/
sudo python3 freqshow.py

If you get the original FreqShow, YEA! 
Test it to make sure touchscreen works
Now install the update, below:

```


2018-07-23 

This version includes feature updates:
+ Grid display pattern background
+ Noise smoothing 
+ Lowered floor for Spectrograph
+ Faster Waterfall display
+ Automatic startup on reboot
+ Automatic shutdown on Quit

Once you have FreqShow running as per Adafruit instructions (above), run 
 
```
$ cd /home/pi
$ mv FreqShow FreqShow.ORG
$ git clone https://github.com/rgrokett/FreqShow.git
$ cd FreqShow
$ bash install.sh
```

to install the reboot cron and startup file. (This assumes installed to /home/pi on Raspberry.) This replaces the original FreqShow with the new version.

Edit model.py if you wish to change the initial frequency 

START_FREQ = 103    # Default startup Frequency in mhz

When you reboot, the new FreqShow will run automatically.

Manually run FreqShow using:

	$ sudo python freqshow.py


Extra Feature:
Once you determine everything is working properly, you can edit runFreq.sh and uncomment the shutdown command.  
DO NOT do this until all is working correctly, else you will not be able to fix it and have to start all over.

$ nano ~/runFreq.sh

