FreqShow
========

![FreqShow](/sample.jpg)

Raspberry Pi &amp; PiTFT-based RTL-SDR frequency scanning and display tool.  See installation and usage instructions in the guide at: https://learn.adafruit.com/freq-show-raspberry-pi-rtl-sdr-scanner/overview

## UPDATE

2020-10-08
```
Using Bangood PTFT 2.8 Resistive touch screen
Model: mzdpi-vga-zero version b
Install onto Buster using script instructions:
Doc: http://raspberrypiwiki.com/2.8_inch_Touch_Screen_for_Pi_zero#Setup_screen_via_script_.28Recommend.29

Edit freqshow.py:
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV'      , '/dev/fb0')
    os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
    os.putenv('SDL_MOUSEDEV'   , '/dev/input/event0')
```

Fix for missing pygame:
```
sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev

sudo pip install pygame

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

