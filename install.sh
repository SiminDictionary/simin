#!/bin/bash
SIMINP=/opt/simin
USRSIMIN=/usr/bin/simin
sudo mkdir $SIMINP;
sudo cp -r * $SIMINP/
sudo cp simin /usr/bin/
sudo chmod +x $USRSIMIN
sudo cp simin.desktop /usr/share/applications
sudo rm -rf $SIMINP/simin.desktop $SIMINP/install.sh __pycache__ $SIMINP/simin
sudo chown -R $(id -u):$(id -g) $SIMINP