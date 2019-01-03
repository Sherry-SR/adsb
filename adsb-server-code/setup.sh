#########################################################################
# File Name: setup.sh
# Author: Laputa
# mail: xiaomiliu1@126.com
# Created Time: Mon 31 Aug 2015 03:23:04 PM CST
#########################################################################
#!/bin/bash
sudo apt-get install -y cmake build-essential python-pip libusb-1.0-0-dev python-numpy git apache2
cd rtl-sdr
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
sudo pip install pyrtlsdr
sudo pip install requests

cd ../../
PKG_PATH=$PWD"/rtl-sdr/build/librtlsdr.pc"
echo $PKG_PATH
export PKG_CONFIG_PATH=$PKG_PATH
cd dump1090
make
sudo echo "blacklist dvb_usb_rtl28xxu" > /etc/modprobe.d/adsb-blacklist.conf

sudo chown pi /var/www
cp map4.html /var/www

echo 'OK!'
echo 'You MUST restart your system to blacklist the kernel module dvb_usb_rtl28xxu'
