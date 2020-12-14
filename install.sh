#!/bin/bash
# Installs FreqShow 

sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python-scipy

cp runFreq.sh $HOME/

crontab cronfile

