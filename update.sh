#!/bin/bash 
sleep 5
List=$(ps -aux | grep '/gui.py' | head -n 1 | cut -d " " -f8)
kill $List
apt install git -y
mkdir /tmp/updt
cd /tmp/updt
git clone https://github.com/FuocomanSap/P4wnp1-ALOA-Menu-Reworked.git
cd P4wnp1-ALOA-Menu-Reworked/
#/bin/bash install.sh & #the best version, but freeze the rasp
/bin/bash install.sh
#cd /root # not required
rm -rf /tmp/updt
reboot
