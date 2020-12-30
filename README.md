FreqShow
========


![FreqShow](/sample.jpg)

Raspberry Pi &amp; PiTFT-based RTL-SDR frequency scanning and display tool.  See installation and usage instructions in the guide at: 

https://learn.adafruit.com/freq-show-raspberry-pi-rtl-sdr-scanner/overview


## UPDATE

2020-12-08
```
Install Raspberry Pi OS with desktop (not Lite!)
Login via SSH or Terminal:

sudo apt update
sudo apt upgrade

----
If using Adafruit PTFT touch screens
Follow 
https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/overview

----
If using Bangood PTFT 2.8 Resistive touch screen
Model: mzdpi-vga-zero version b
Touch: ADS7846 Touchscreen
Follow: 
http://raspberrypiwiki.com/2.8_inch_Touch_Screen_for_Pi_zero#Setup_screen_via_script_.28Recommend.29

----
```

## For both screen types:

It should boot to Desktop and the touchscreen work.
Complete the GUI setup screens.
Next, turn off the GUI desktop
```
sudo raspi-config
Select System Options -> Boot -> Console
```

### Install RTLSDR:
```
sudo apt-get install cmake libusb-1.0-0-dev pandoc
cd ~
git clone git://git.osmocom.org/rtl-sdr.git
cd rtl-sdr
mkdir build
cd build
cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON
make
sudo make install
sudo ldconfig
sudo pip3 install pyrtlsdr
sudo reboot
```

### Install Adafruit FreqShow:
```
cd ~
git clone https://github.com/adafruit/FreqShow.git
cd FreqShow

Edit freqshow.py: 
Comment out all:
    #os.putenv('SDL_VIDEODRIVER', 'fbcon') # Not used
    #os.putenv('SDL_FBDEV'      , '/dev/fb0')
    #os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
    #os.putenv('SDL_MOUSEDEV'   , '/dev/input/event1')

If calibration isn't working:
   pygame.mouse.set_visible(True)

Once installed, you need to use Python3:
cd ~/FreqShow/
sudo python3 freqshow.py
```

If you get the original FreqShow, YEA! 
Test it to make sure touchscreen works
Now install the update, below:

## Update To FreqShow
This version includes feature updates:
+ Grid display pattern background
+ Noise smoothing 
+ Lowered floor for Spectrograph
+ Faster Waterfall display
+ Automatic startup on reboot
+ Automatic shutdown on Quit

Once you have FreqShow running as per Adafruit instructions (above), run 
 
```
cd /home/pi
mv FreqShow FreqShow.ORG
git clone https://github.com/rgrokett/FreqShow.git
cd FreqShow
bash install.sh
```


When you reboot, the new FreqShow will run automatically.

Manually run FreqShow using:
```
sudo python3 freqshow.py
```


Extra Features:

Edit model.py if you wish to change the initial frequency 
nano model.py
```
START_FREQ = 145    # Default startup Frequency in mhz
```

Once you determine everything is working properly, you can edit runFreq.sh and uncomment the shutdown command.  
DO NOT do this until all is working correctly, else you will not be able to fix it and have to start all over.

```
nano ~/runFreq.sh
```

