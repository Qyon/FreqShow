#!/bin/bash
# Installs FreqShow 

sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python3-scipy

cp runFreq.sh $HOME/

crontab cronfile

