#!/bin/bash 
echo "Install Luma.core drivers"
apt update --fix-missing
apt install python3.7-dev python3-pip libfreetype6-dev libjpeg-dev dsniff mitmproxy -y
apt install --upgrade python3-luma.oled
apt install --upgrade python3-luma.core
echo "Create directories"
mkdir -p /root/BeBoXGui/{images,nmap}
echo "Copying files"
cp *.py /root/BeBoXGui/
cp images/* /root/BeBoXGui/images/
echo "Copying run script in local P4wnP1 script"
cp scripts/runmenu.sh /usr/local/P4wnP1/scripts/
chmod +x /usr/local/P4wnP1/scripts/runmenu.sh
cp update.sh /root/BeBoXGui/
chmod +x /root/BeBoXGui/update.sh
echo "All files are ready"
echo "to run with P4wnP1 boot"
echo "Go thru web interface"
echo "Go in trigger section"
echo "Create new trigger"
echo "on service start :"
echo "run script sh and choose "
echo "runmenu.sh"
echo "Enjoy"
echo "by default gui.py use SPI interface"
echo "if you use I2C oled edit gui.py"
echo "and set I2C_USER = 1"

