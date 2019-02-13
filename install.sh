#!/bin/bash

VAR=$(id -u)
if [ $VAR = 0 ]; then
	echo -e " ========== \n Do not run this file with root!\n =========="
	exit
fi

SIMINP=/opt/simin
USRSIMIN=/usr/bin/simin
sudo mkdir $SIMINP;
sudo cp -r * $SIMINP/
sudo cp simin /usr/bin/
sudo chmod +x $USRSIMIN
sudo cp simin-no /usr/bin/
sudo chmod +x /usr/bin/simin-no
sudo cp simin.desktop /usr/share/applications
sudo rm -rf $SIMINP/simin.desktop $SIMINP/install.sh __pycache__ $SIMINP/simin $SIMINP/simin-no
sudo chown -R $(id -u):$(id -g) $SIMINP
echo "Done!"
