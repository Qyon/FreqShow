#!/bin/bash
# Installs FreqShow 

sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
sudo apt-get install libatlas-base-dev gfortran
sudo pip install --upgrade pip
sudo pip install scipy

cp runFreq.sh $HOME/

crontab cronfile

