FreqShow
========

![FreqShow](/sample.jpg)

Raspberry Pi &amp; PiTFT-based RTL-SDR frequency scanning and display tool.  See installation and usage instructions in the guide at: https://learn.adafruit.com/freq-show-raspberry-pi-rtl-sdr-scanner/overview

## UPDATE

2018-07-23 

This version includes feature updates:
+ Grid display pattern background
+ Noise smoothing 
+ Lowered floor for Spectrograph
+ Faster Waterfall display
+ Automatic startup on reboot
+ Automatic shutdown on Quit

Once you have FreqShow running as per Adafruit instructions (above), run 

	$ bash install.sh

to install the reboot cron and startup file. (This assumes installed to /home/pi on Raspberry.)

Edit model.py if you wish to change the initial frequency 

START_FREQ = 103    # Default startup Frequency in mhz


Manually run FreqShow using:

	$ sudo python freqshow.py


