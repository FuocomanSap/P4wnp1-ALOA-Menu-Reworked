# variant for Kali-arm
##### INFOS

This project was born from: https://github.com/beboxos/P4wnP1_ALOA_OLED_MENU_V2, since python2.7 is deprecated and therefore no longer compatible with the libraries in use, I opened a Fork, updated the code to Python3.7 and made a PullRequest.
 
Since the original repo seems to be no longer maintained, I decided to open a new one with updates made so that everyone can take advantage of this fantastic project of https://github.com/beboxos .

If BeboXos returns to his repo this will be closed, and i hope so.

All rights to the original code are owned by BeboXos.

## what's new
I updated the code to work with python3.7, fixed some bugs and added new features.
* hosts discovery
* nmap on a specific host and save the report
* update the gui-code via gui-option
* vulnerability scan (experimental...help me)
* Deauther(Jammer-like) on Wifi AP, working on
* TODO Deauther(Jammer-like) on a specific client
* TODO others

## Installation:
On boot partition edit config.txt to set I2C and SPI to active
in termnial you can type 
* nano /boot/config.txt

find the section far away down and set : 

* dtparam=i2c_arm=on
* dtparam=i2c1=on

and find and set spi section 

* dtparam=spi=on


###### Note for i2c: (on gui.py)

 ######  uncomment the "bus = smbus.SMBus(0)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)" line
 ######  set USER_I2C=1
 ######  (if ups) set UPS=1

###### Note for SPI: (on gui.py) (currently set like this)

 ######  comment the "bus = smbus.SMBus(0)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)" line
 ######  set USER_I2C=0
 ######  (if you have a ups) set UPS=1

* chmod +x install.sh update.sh
* run sh install.sh 
the script will automatically install all the files needed




##### GPIO 8 keys are default waveshare hat

you can edit to set to your hat if different
* GPIO
* KEY_UP_PIN     : 6, 
* KEY_DOWN_PIN   : 19, 
* KEY_LEFT_PIN   : 5, 
* KEY_RIGHT_PIN  : 26, 
* KEY_PRESS_PIN  : 13, 
* KEY1_PIN       : 21, 
* KEY2_PIN       : 20, 
* KEY3_PIN       : 16



## Start at boot
in P4wnP1 web interface , create a trigger action that runs the script runmenu.sh in you default template (by default startup)
select the script runmenu.sh.
* open the web interface
* select Tigger action
* add one
* select runmenu.sh
* select store and type startup



enjoy
# i'm not responsible on usage you do with this repo, it's for educational purpose only
