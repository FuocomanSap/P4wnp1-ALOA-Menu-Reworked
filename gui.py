# -*- coding:utf-8 -*-
#imports 
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator
from luma.core import lib
from luma.oled.device import sh1106
import RPi.GPIO as GPIO
import datetime
import time
import subprocess
from subprocess import Popen
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import socket, sys
import os
import base64
import struct
import smbus2 as smbus

UPS = 0 # 1 = UPS Lite connected / 0 = No UPS Lite hat
SCNTYPE = 1  # 1= OLED #2 = TERMINAL MODE BETA TESTS VERSION

def execcmd(cmd):
    try:
        return (str(subprocess.check_output(cmd, shell = True )))
    except:
        return (-1)
def execcmdNostr(cmd):
    try:
        return ((subprocess.check_output(cmd, shell = True )))
    except:
        return (-1)


def displayError():
    DisplayText(
            "",
            "",
            "",
            "      INTERNAL ERROR",
            "",
            "",
            ""
            )
    time.sleep(5) 



def readVoltage(bus):
        "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = bus.read_word_data(address, 2)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000/16
        return voltage


def readCapacity(bus):
        "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = bus.read_word_data(address, 4)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity

#not needed if you are using spi(like me -fuocoman)
#bus = smbus.SMBus(0)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

GPIO.setwarnings(False)

# Load default font.
font = ImageFont.load_default()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 128
height = 64
image = Image.new('1', (width, height))
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
line1 = top
line2 = top+8
line3 = top+16
line4 = top+25
line5 = top+34
line6 = top+43
line7 = top+52
brightness = 255 #Max
fichier=""
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
RST = 25
CS = 8
DC = 24

#GPIO define and OLED configuration
RST_PIN        = 25 #waveshare settings
CS_PIN         = 8  #waveshare settings
DC_PIN         = 24 #waveshare settings
KEY_UP_PIN     = 6  #stick up
KEY_DOWN_PIN   = 19 #stick down
KEY_LEFT_PIN   = 5 #5  #sitck left // go back
KEY_RIGHT_PIN  = 26 #stick right // go in // validate
KEY_PRESS_PIN  = 13 #stick center button
KEY1_PIN       = 21 #key 1 // up
KEY2_PIN       = 20  #20 #key 2 // cancel/goback
KEY3_PIN       = 16 #key 3 // down
USER_I2C = 0      #set to 1 if your oled is I2C or  0 if use SPI interface
#init GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
screensaver = 0
#SPI
#serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)
if SCNTYPE == 1:
    if  USER_I2C == 1:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RST,GPIO.OUT)
        GPIO.output(RST,GPIO.HIGH)
        serial = i2c(port=1, address=0x3c)
    else:
        serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)
if SCNTYPE == 1:
    device = sh1106(serial, rotate=2) #sh1106
def DisplayText(l1,l2,l3,l4,l5,l6,l7):
    # simple routine to display 7 lines of text
    if SCNTYPE == 1:
        with canvas(device) as draw:
            draw.text((0, line1), l1,  font=font, fill=255)
            draw.text((0, line2), l2, font=font, fill=255)
            draw.text((0, line3), l3,  font=font, fill=255)
            draw.text((0, line4), l4,  font=font, fill=255)
            draw.text((0, line5), l5, font=font, fill=255)
            draw.text((0, line6), l6, font=font, fill=255)
            draw.text((0, line7), l7, font=font, fill=255)
    if SCNTYPE == 2:
            os.system('clear')
            print(l1)
            print(l2)
            print(l3)
            print(l4)
            print(l5)
            print(l6)
            print(l7)
def shell(cmd):
    return(subprocess.check_output(cmd, shell = True ))
def switch_menu(argument):
    switcher = {
    0: "_  KALI_ARM",
        1: "_SYSTEM RELATED",
        2: "_",
        3: "_WIRELESS THINGS",
        4: "_",
        5: "_",
        6: "_INFOSEC TOOLS",
        7: "_System information",
        8: "_OLED brightness",
        9: "_",
        10: "_Display OFF",
        11: "_Keys Test",
        12: "_Reboot GUI",
        13: "_System shutdown",
        14: "_",
        15: "_",
        16: "_",
        17: "_",
        18: "_",
        19: "_",
        20: "_",
        21: "_Scan WIFI AP",
        22: "_Hosts Discovery",
        23: "_Nmap",
        24: "_Vulnerability Scan",
        25: "_Deauther-Bcast",
        26: "_",
        27: "_",
        28: "_Send to oled group",
        29: "_",
        30: "_",
        31: "_",
        32: "_",
        33: "_",
        34: "_",
        35: "_",
        36: "_",
        37: "_",
        38: "_",
        39: "_",
        40: "_",
        41: "_",
        42: "_",
        43: "_",
        44: "_",
        45: "_",
        46: "_",
        47: "_",
        48: "_",
        #newmenu
        49: "_WIRED THINGS",
        50: "_newsubmenu2",
        51: "_newsubmenu3",
        52: "_newsubmenu4",
        53: "_newsubmenu5",
        54: "_newsubmenu6",
        55: "_UpdateOledMenu",
        #newsections
        56: "_",
        57: "_",
        58: "_",
        59: "_",
        60: "_",
        61: "_",
        62: "_",
        #newsections
        63: "_",
        64: "_",
        65: "_",
        66: "_",
        67: "_",
        68: "_",
        69: "_"

}
    return switcher.get(argument, "Invalid")
def about():
    # simple sub routine to show an About
    DisplayText(
        "  :KALI_ARM:",
        "KALI (c) ",
        "V 0.1",
        "based od",
        "by BeBoX's GUI",
        "and updated",
        "by FuocomanSap"
        )
    while GPIO.input(KEY_LEFT_PIN):
        #wait
        menu = 1
    page = 0
#system information sub routine
def sysinfos():
    while GPIO.input(KEY_LEFT_PIN):
        now = datetime.datetime.now()
        today_time = now.strftime("%H:%M:%S")
        today_date = now.strftime("%d %b %y")
        cmd = "hostname -I"
        qui = execcmd(cmd)
        if(qui==-1):
            displayError()
            return()
        IP = qui.split(" ")[0]
        IP2 = qui.split(" ")[1]
        IP3 = qui.split(" ")[2]
        cmd = "top -bn1 | grep %Cpu | awk '{printf \"%.0f\",$2}'"
        temp = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
        temp = int(temp)/1000
        if UPS == 1:
            volt = "BAT :%5.2fV " % readVoltage(bus)
            batt = int(readCapacity(bus))
        else:
            volt = "BAT : N/C "
            batt = 0
        if batt>100:
            batt=100
        BATT = volt + str(batt) + "% t:" + str(temp)
        #print(str(subprocess.check_output(cmd, shell = True )))
        res = execcmd(cmd)
        if(res==-1):
            displayError()
            return()
        proc = "CPU:" + res.split("'")[1] + "%"
        cmd = " cat /sys/class/thermal/thermal_zone0/temp "
        res = execcmd(cmd)
        if(res==-1):
            displayError()
            return()
        cpuTemp = res.split("'")[1].split("\\")[0]
        cpuTemp = str(int(cpuTemp)/1000)
        proc += " Temp: " + cpuTemp
        cmd = "free -m | awk 'NR==2{printf \"MEM :%.2f%%\", $3*100/$2 }'"
        res = execcmd(cmd)
        if(res==-1):
            displayError()
            return()
        MemUsage = res.split("'")[1] # + proc
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        res = execcmd(cmd)
        if(res==-1):
            displayError()
            return()
        Disk = res.split("'")[1]   
        DisplayText(
            "WIFI: " + IP.split("'")[1],
            #str(BATT)
            str(proc),
            str(MemUsage),
            Disk,
            "BTH.: " + str(IP3),
            "USB.: " + str(IP2),
            today_date + " " + today_time
            )
        time.sleep(0.1)
    #page = 7
def IdentOS(ips):
    #return os name if found ex. Microsoft Windows 7 ,  Linux 3.X
    return(shell("nmap -p 22,80,445,65123,56123 -O " + ips + " | grep Running: | cut -d \":\" -f2 | cut -d \"|\" -f1"))
def OsDetails(ips):
    return(shell("nmap -p 22,80,445,65123,56123 -O " + ips + " | grep \"OS details:\" | cut -d \":\" -f2 | cut -d \",\" -f1"))
def OLEDContrast(contrast):
    #set contrast 0 to 255
    if SCNTYPE == 1:
        while GPIO.input(KEY_LEFT_PIN):
            #loop until press left to quit
            with canvas(device) as draw:
                if GPIO.input(KEY_UP_PIN): # button is released
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
                else: # button is pressed:
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled
                        contrast = contrast +5
                        if contrast>255:
                            contrast = 255

                if GPIO.input(KEY_DOWN_PIN): # button is released
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
                else: # button is pressed:
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled
                        contrast = contrast-5
                        if contrast<0:
                            contrast = 0
                device.contrast(contrast)
                draw.text((54, line4), "Value : " + str(contrast),  font=font, fill=255)
    return(contrast)
def splash():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'bootwhat.bmp'))
    splash = Image.open(img_path) \
        .transform((device.width, device.height), Image.AFFINE, (1, 0, 0, 0, 1, 0), Image.BILINEAR) \
        .convert(device.mode)
    device.display(splash)
    time.sleep(5) #5 sec splash boot screen
def SreenOFF():
    #put screen off until press left
    if SCNTYPE == 1:
        while GPIO.input(KEY_LEFT_PIN):
            device.hide()
            time.sleep(0.1)
        device.show()
def KeyTest():
    if SCNTYPE == 1:
        while GPIO.input(KEY_LEFT_PIN):
            with canvas(device) as draw:
                if GPIO.input(KEY_UP_PIN): # button is released
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
                else: # button is pressed:
                        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1)  #Up filled

                if GPIO.input(KEY_LEFT_PIN): # button is released
                        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left
                else: # button is pressed:
                        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1)  #left filled

                if GPIO.input(KEY_RIGHT_PIN): # button is released
                        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right
                else: # button is pressed:
                        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1) #right filled

                if GPIO.input(KEY_DOWN_PIN): # button is released
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
                else: # button is pressed:
                        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1) #down filled

                if GPIO.input(KEY_PRESS_PIN): # button is released
                        draw.rectangle((20, 22,40,40), outline=255, fill=0) #center 
                else: # button is pressed:
                        draw.rectangle((20, 22,40,40), outline=255, fill=1) #center filled

                if GPIO.input(KEY1_PIN): # button is released
                        draw.ellipse((70,0,90,20), outline=255, fill=0) #A button
                else: # button is pressed:
                        draw.ellipse((70,0,90,20), outline=255, fill=1) #A button filled

                if GPIO.input(KEY2_PIN): # button is released
                        draw.ellipse((100,20,120,40), outline=255, fill=0) #B button
                else: # button is pressed:
                        draw.ellipse((100,20,120,40), outline=255, fill=1) #B button filled
                        
                if GPIO.input(KEY3_PIN): # button is released
                        draw.ellipse((70,40,90,60), outline=255, fill=0) #A button
                else: # button is pressed:
                        draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
def FileSelect(path,ext):
    cmd = "ls -F --format=single-column  " + path + "*" + ext
    res = execcmd(cmd)
    if(res==-1):
        displayError()
        return()
    listattack=res.split("'")[1]
    listattack=listattack.replace(ext,"")
    listattack=listattack.replace(path,"")
    listattack=listattack.replace("*","")
    listattack=listattack.replace("\\n","\\")
    listattack=listattack.split("\\")
    print(listattack)
    maxi=len(listattack) #number of records
    cur=0
    retour = ""
    ligne = ["","","","","","","",""]
    time.sleep(0.5)
    while GPIO.input(KEY_LEFT_PIN):
        #on boucle
        tok=0
        if maxi < 7:
            for n in range(0,7):
                if n<maxi:
                    if n == cur:
                        ligne[n] = ">"+listattack[n]
                    else:
                        ligne[n] = " "+listattack[n]
                else:
                    ligne[n] = ""
        else:
            if cur+7<maxi:
                for n in range (cur,cur + 7):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]
                    tok=tok+1
            else:
                for n in range(maxi-8,maxi-1):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]                            
                    tok=tok+1
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur -1
            if cur<0:
                cur = 0
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur + 1
            if cur>maxi-2:
                cur = maxi-2
        if GPIO.input(KEY_RIGHT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            retour = listattack[cur]+ext
            return(retour)
        #print(str(cur) + " " + listattack[cur])        #debug
        DisplayText(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6])
        time.sleep(0.1)
    return("")
def templateSelect(liste):
    # GetTemplateList("BLUETOOTH").split("\n")
    fichier = GetTemplateList(liste).split("\n")
    maxi = len(fichier)
    cur=1
    retour = ""
    ligne = ["","","","","","","",""]
    time.sleep(0.5)
    while GPIO.input(KEY_LEFT_PIN):
        #on boucle
        tok=1
        if maxi < 8:
            for n in range(1,8):
                if n<maxi:
                    if n == cur:
                        ligne[n-1] = ">"+fichier[n]
                    else:
                        ligne[n-1] = " "+fichier[n]
                else:
                    ligne[n-1] = ""
        else:
            if cur+7<maxi:
                for n in range (cur,cur + 7):
                    if n == cur:
                        ligne[tok-1] = ">"+fichier[n]
                    else:
                        ligne[tok-1] = " "+fichier[n]
                    tok=tok+1
            else:
                for n in range(maxi-8,maxi-1):
                    if n == cur:
                        ligne[tok-1] = ">"+fichier[n]
                    else:
                        ligne[tok-1] = " "+fichier[n]                            
                    tok=tok+1
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur -1
            if cur<1:
                cur = 1
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur + 1
            if cur>maxi-2:
                cur = maxi-2
        if GPIO.input(KEY_RIGHT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            retour = fichier[cur]
            print(retour)
            return(retour)    
        # ----------
        DisplayText(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6])
        time.sleep(0.1)

def restart():
    DisplayText(
    "",
    "",
    "",
    "PLEASE WAIT ...",
    "",
    "",
    ""
    )
    cmd="python3.7 /root/BeBoXGui/runmenu.py &"
    exe = execcmd(cmd)
    if(exe==-1):
                displayError()
                return()
    return()




def ListWifi ():
    cmd =subprocess.check_output("sudo iwlist wlan0 scan", shell = True )
    return cmd
def LwifiExt (word,liste):
    for n in range(len(liste)):
        if liste[n].find(word) != -1:
            rep = liste[n].split(":")
            return rep[1]
    return 0
def scanwifi():
    #list wifi APs
    cmd ="sudo iwlist wlan0 scan | grep ESSID"
    res = execcmd(cmd)
    if(res==-1):
        displayError()
        return()
    SSID=res.split("'")[1]
    SSID=SSID.replace("                    ESSID:","")
    SSID=SSID.replace("\"","")
    ssidlist=SSID.split("\\n")
    cmd ="sudo iwlist wlan0 scan | grep Encryption"
    res = execcmd(cmd)
    if(res==-1):
        displayError()
        return()
    Ekey=res.split("'")[1]
    Ekey=Ekey.replace("                    Encryption ","")
    Ekeylist=Ekey.split("\\n")     
    for n in range(0,len(ssidlist)):
        if ssidlist[n]=="":ssidlist[n]="Hidden"
        ssidlist[n]=ssidlist[n]+" ["+Ekeylist[n]+"]"
    #----------------------------------------------------------
    listattack=ssidlist
    maxi=len(listattack) #number of records
    cur=0
    retour = ""
    ligne = ["","","","","","","",""]
    time.sleep(0.5)
    while GPIO.input(KEY_LEFT_PIN):
        #on boucle
        tok=0
        if maxi < 7:
            for n in range(0,7):
                if n<maxi:
                    if n == cur:
                        ligne[n] = ">"+listattack[n]
                    else:
                        ligne[n] = " "+listattack[n]
                else:
                    ligne[n] = ""
        else:
            if cur+7<maxi:
                for n in range (cur,cur + 7):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]
                    tok=tok+1
            else:
                for n in range(maxi-8,maxi-1):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]                            
                    tok=tok+1
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur -1
            if cur<0:
                cur = 0
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur + 1
            if cur>maxi-2:
                cur = maxi-2
        if GPIO.input(KEY_RIGHT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            retour = listattack[cur]
            DisplayText(" TOBE IMPLEMENTED (WIFI)","","","","","","")
            time.sleep(2)
            return(retour)
        #print(str(cur) + " " + listattack[cur])        #debug
        DisplayText(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6])
        time.sleep(0.1)
    return("")



def Osdetection():
    DisplayText(
            "",
            "",
            "",
            "      PLEASE WAIT",
            "",
            "",
            ""
            )
    os=IdentOS("172.16.0.2")
    if(str(os)=="b''"):
        while GPIO.input(KEY_LEFT_PIN):     
            DisplayText(
                "Experimental nmap OS",
                "detection",
                "",
                "Too many fingerprints match this host",
                " Or Zero ",
                "",
                "Press LEFT to exit"
                )
        return
    
    detail=OsDetails("172.16.0.2")

    while GPIO.input(KEY_LEFT_PIN):
        DisplayText(
            "Experimental nmap OS",
            "detection",
            "",
            os.replace("Microsoft","MS").replace("Windows","win"),
            detail.replace("Microsoft","MS").replace("Windows","win"),            
            "",
            "Press LEFT to exit"
            )
    
def socketCreate():
    try:
        global host
        global port
        global s
        port = 4445
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        if port == '':
            socketCreate()
        #socketCreate()
    except socket.error as msg:
        print('socket creation error: ' + str(msg[0]))
def socketBind():
    try:
        print('Binding socket at port %s'%(port))
        s.bind((host,port))
        s.listen(1)
    except socket.error as msg:
        print('socket bindig error: ' + str(msg[0]))
        print('Retring...')
        socketBind()
def socketAccept():
    global conn
    global addr
    global hostname
    try:
        conn, addr = s.accept()
        print('[!] Session opened at %s:%s'%(addr[0],addr[1]))
        menu2()
    except socket.error as msg:
        print('Socket Accepting error: ' + str(msg[0]))
def sendps1(ps1file):        
        f=open(ps1file,"r")
        for x in f:
            conn.send(x.encode())
            result = conn.recv(16834)
            print(result.decode())

        
def hostselect():
    DisplayText("","","","wait, may take a while ","","","")
    cmd = "hostname -I"
    res = execcmd(cmd)
    if(res==-1):
        displayError()
        return()
    subnetIp = res.split(" ")[0].split("'")[1]
    pos = subnetIp.rfind('.')
    cmd = "nmap -sL -Pn " + str(subnetIp[0:pos]) +".0/24 | grep -v 'Nmap scan report for " + subnetIp[0:2] + "'"
    res = execcmd(cmd)
    if(res==-1):
        displayError()
        return()
    hosts = res
    hostlist = hosts.split("\\n")
    del hostlist[-1]
    del hostlist[-1]
    del hostlist[0]
    for i in range(0,len(hostlist)):
        hostlist[i] = hostlist[i][21:]
    #print(hostlist[i][21:])
    fichier = hostlist 
    maxi = len(hostlist)
    cur=1
    retour = ""
    ligne = ["","","","","","","",""]
    time.sleep(0.5)
    while GPIO.input(KEY_LEFT_PIN):
        #on boucle
        tok=1
        if maxi < 8:
            for n in range(1,8):
                if n<maxi:
                    if n == cur:
                        ligne[n-1] = ">"+fichier[n]
                    else:
                        ligne[n-1] = " "+fichier[n]
                else:
                    ligne[n-1] = ""
        else:
            if cur+7<maxi:
                for n in range (cur,cur + 7):
                    if n == cur:
                        ligne[tok-1] = ">"+fichier[n]
                    else:
                        ligne[tok-1] = " "+fichier[n]
                    tok=tok+1
            else:
                for n in range(maxi-8,maxi-1):
                    if n == cur:
                        ligne[tok-1] = ">"+fichier[n]
                    else:
                        ligne[tok-1] = " "+fichier[n]                            
                    tok=tok+1
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur -1
            if cur<1:
                cur = 1
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur + 1
            if cur>maxi-2:
                cur = maxi-2
        if GPIO.input(KEY_RIGHT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            retour = fichier[cur]
            selected= retour.split("(")[1].split(")")[0]
            print(selected)
            #return(retour)
            return(selected)    
        # ----------
        DisplayText(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6])
        time.sleep(0.1)

def nmap():
    selected = hostselect()
    choise = 0  
    while(choise == 0):
        DisplayText("                  YES","","save the nmap?","this will take a while","/BeboXgui/nmap/<IP>.txt   ","","                   NO")
        if (not GPIO.input(KEY1_PIN)): # button is released
            choise = 1 #A button
        if not GPIO.input(KEY3_PIN): # button is released   
            choise = 2
    DisplayText("","","","    wait ","","","")
    
    if(choise==1):
        cmd = "nmap -Pn -A " + selected
        ret = execcmd(cmd)
        if(ret==-1):
            displayError()
            return()
        f = open("nmap/" + str(selected) + ".txt","w+")
        reportList = str(ret).split("'")[1].split("\\n")
        for line in reportList:
            #print(line + "\\n")
            f.write(line + "\n")
        f.close()
        cmd = "cat " + "nmap/" + selected +".txt | grep tcp"
        ret = execcmd(cmd)
        if( ret ==-1):
            displayError()
            return()
    else:
        cmd = "nmap -Pn -A " + selected + " | grep tcp"
        ret = execcmd(cmd)
        if(ret==-1):
            displayError()
            return()

    res = str(ret).split("'")[1].split("\\n")[:-1]
    print(res)
    toprint = ["","","","","","",""]
    for i in range(0,len(res)):
        if(i>=len(toprint)): break
        toprint[i]="_"+res[i]
    DisplayText(toprint[0],toprint[1],toprint[2],toprint[3],toprint[4],toprint[5],toprint[6])
    time.sleep(10)
    #TODO add the vulnerability scan



def nmapLocal():
    selected = "172.16.0.2"
    choise = 0  
    while(choise == 0):
        DisplayText("                  YES","","save the nmap?","this will take a while","/BeboXgui/nmap/<IP>.txt   ","","                   NO")
        if (not GPIO.input(KEY1_PIN)): # button is released
            choise = 1 #A button
        if not GPIO.input(KEY3_PIN): # button is released   
            choise = 2
    DisplayText("","","","    wait ","","","")
    
    if(choise==1):
        cmd = "nmap -Pn -A " + selected
        ret = execcmd(cmd)
        if(ret==-1):
            displayError()
            return()
        f = open("nmap/" + str(selected) + ".txt","w+")
        reportList = str(ret).split("'")[1].split("\\n")
        for line in reportList:
            #print(line + "\\n")
            f.write(line + "\n")
        f.close()
        cmd = "cat " + selected +".txt | grep tcp"
        ret = execcmd(cmd)
        if( ret ==-1):
            displayError()
            return()
    else:
        cmd = "nmap -Pn -A " + selected + " | grep tcp"
        ret = execcmd(cmd)
        if(ret==-1):
            displayError()
            return()

    res = str(ret).split("'")[1].split("\\n")[:-1]
    print(res)
    toprint = ["","","","","","",""]
    for i in range(0,len(res)):
        if(i>=len(toprint)): break
        toprint[i]="_"+res[i]
    DisplayText(toprint[0],toprint[1],toprint[2],toprint[3],toprint[4],toprint[5],toprint[6])
    time.sleep(10)
    #TODO add the vulnerability scan

def update():
    DisplayText("","","","U NEED Wifi Connection ","","","")
    time.sleep(8)
    try:
        #Popen(['nohup','/bin/bash','/root/BeBoXGui/update.sh'], stdout=open('/dev/null','w'), stderr=open('/dev/null','a'),preexec_fn=os.setpgrp )
        Popen(['nohup','/bin/bash','/root/BeBoXGui/update.sh'],preexec_fn=os.setpgrp)
        DisplayText("updating","it's a quite buggy","im updating","the screen will freeze","it's normal","im not restarting myself",":>")
        time.sleep(10)
        exit()
    except:
        displayError()
        DisplayText("","","","Do U have Wifi Connection? ","","","")
        time.sleep(5)

def vulnerabilityScan():
    DisplayText("Remeber:","Firts u need to","perform an Nmap","and then ","save the output","this is an","experimental feature")
    time.sleep(5)
    DisplayText("","","","this is experimental :C","","","")
    time.sleep(5)
    selected = FileSelect("/root/BeBoXGui/nmap/",".txt")
    filePath = "/root/BeBoXGui/nmap/" + selected
    cmd = "cat " + filePath + " | grep tcp"
    res = execcmd(cmd)
    if(res==-1):
        displayError()
        time.sleep(5)
        return()
    #print(res)
    toSearch = str(res).split("'")[1].split("\\n")
    del toSearch[-1]
    founded = 0
    for i in toSearch:
        #print(i)
        i = i[23:]
        auxi = i.split(" ")
        print(auxi)
        i = auxi[0] + " " + auxi[1][:-2]
        print("search for: " + i )
        cmd = "searchsploit " + str(i)
        res = execcmd(cmd)
        if(res==-1):
            displayError()
            time.sleep(5)
        if ((str(res).split("'")[1])[1] == "-"):
            founded +=1
    print(founded)
    DisplayText("","","","founded: " + str(founded) ,"","","")


def getSSID():
    #list wifi APs
    cmd ="airmon-ng start wlan0 && airmon-ng start wlan0mon"
    res = execcmd(cmd)
    if(res==-1):
        displayError()
        return()
    try:
        #Popen(['nohup','/bin/bash','/root/BeBoXGui/update.sh'], stdout=open('/dev/null','w'), stderr=open('/dev/null','a'),>
        Popen(['nohup','/bin/bash','test.sh'],preexec_fn=os.setpgrp)
        DisplayText("","","wait","","","","")
        time.sleep(10)
        cmd = "ps -aux | grep 'airodump-ng wlan0mon -w reportAiro -a-' | head -n 1 | cut -d ' ' -f7"
        res = execcmd(cmd)
        if(res==-1):
            displayError()
            time.sleep(5)
            return()
    except:
        displayError()
        time.sleep(5)
        return()
    cmd="cat reportAiro-01.csv"
    res = execcmd(cmd)
    if(res==-1):
        displayError()
        exit()
    cmd="rm -rf reportAiro*"
    toDEl = execcmd(cmd)
    if(toDEl==-1):
        displayError()
        exit()
    res = str(res).replace("\\r","").split("\\n")
    del res[0]
    del res[0]
    toRemove=res.index("Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs")
    res=res[:toRemove-1]
    for i in range(0,len(res)):
        res[i] = res[i].split(",")
        del res[i][-1]
        res[i]=res[i][-1]+ ","+res[i][3] +","+ res[i][0]
    ssidlist=res

    #----------------------------------------------------------
    listattack=ssidlist
    maxi=len(listattack) #number of records
    cur=0
    retour = ""
    ligne = ["","","","","","","",""]
    time.sleep(0.5)
    while GPIO.input(KEY_LEFT_PIN):
        #on boucle
        tok=0
        if maxi < 7:
            for n in range(0,7):
                if n<maxi:
                    if n == cur:
                        ligne[n] = ">"+listattack[n]
                    else:
                        ligne[n] = " "+listattack[n]
                else:
                    ligne[n] = ""
        else:
            if cur+7<maxi:
                for n in range (cur,cur + 7):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]
                    tok=tok+1
            else:
                for n in range(maxi-8,maxi-1):
                    if n == cur:
                        ligne[tok] = ">"+listattack[n]
                    else:
                        ligne[tok] = " "+listattack[n]                            
                    tok=tok+1
        if GPIO.input(KEY_UP_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur -1
            if cur<0:
                cur = 0
        if GPIO.input(KEY_DOWN_PIN): # button is released
            menu = 1
        else: # button is pressed:
            cur = cur + 1
            if cur>maxi-2:
                cur = maxi-2
        if GPIO.input(KEY_RIGHT_PIN): # button is released
            menu = 1
        else: # button is pressed:
            retour = listattack[cur]
            print(retour)
            return(retour)
        #print(str(cur) + " " + listattack[cur])        #debug
        DisplayText(ligne[0],ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6])
        time.sleep(0.1)
    return("")



def deauther():
    getSSID()
    return()
    
        
    


def main():
    socketCreate()
    socketBind()
    socketAccept()
#init vars 
curseur = 1
page=0  
menu = 1
ligne = ["","","","","","","",""]
selection = 0
if SCNTYPE == 1:
    print("sctype")
    splash()  # display boot splash image ---------------------------------------------------------------------
    #print("selected : " + FileSelect(hidpath,".js"))
    device.contrast(2)
while 1:
    if GPIO.input(KEY_UP_PIN): # button is released
        menu = 1
    else: # button is pressed:
        curseur = curseur -1
        if curseur<1:
            if( page == 49): 
                page = 0
            elif (page == 0):
                page = 49   
            curseur = 7
  
    if GPIO.input(KEY_LEFT_PIN): # button is released
        menu = 1
    else: # button is pressed:
                # back to main menu on Page 0
        page = 0    
    if GPIO.input(KEY_RIGHT_PIN): # button is released
        menu = 1
    else: # button is pressed:
        selection = 1
    if GPIO.input(KEY_DOWN_PIN): # button is released
        menu = 1
    else: # button is pressed:
        curseur = curseur + 1
        if curseur>7:
            if( page == 0):
                page = 49
            elif (page == 49):
                page = 0
            curseur = 1
    #-----------
    if selection == 1:
        # une option du menu a ete validee on va calculer la page correspondante
            if page == 7:
                #system menu
                if curseur == 1:
                    sysinfos()
                if curseur == 2:
                    brightness = OLEDContrast(brightness)
               
                    
                if curseur == 4:
                    SreenOFF()
                if curseur == 5:
                    KeyTest()
                if curseur == 6:
                    #cmd = "reboot"
                    #subprocess.check_output(cmd, shell = True )    
                    restart()
                if curseur == 7:
                    exit()    
                    cmd = "poweroff"
                    execcmd(cmd)   
                    
            if page == 14:
                if curseur == 1:
                    #SSID LIST
                    scanwifi()
                #HID related menu
               
            if page == 21:
                if curseur == 1:
                    #SSID LIST
                    scanwifi()
                if curseur == 2:
                    hostselect()
                if curseur == 3:
                    nmap()     
                if curseur == 4:
                    vulnerabilityScan()  
                if curseur == 5:
                    deauther()     
            
            

                
            

            #main menus section
            if (page == 49):
                if curseur == 1:
                    page = 56
                if curseur == 7:
                    update()
           
            if page == 0:
            #we are in main menu
                if curseur == 1:
                    # call about
                    about()
                if curseur == 2:
                    #system menu 
                    page = 7
                    curseur = 1
                if curseur == 3:
                #hid attacks menu
                    page = 14
                    curseur = 1
                if curseur == 4:
                    page = 21
                    curseur = 1
                if curseur == 5:
                    page = 28
                    curseur = 1
                if curseur == 6:
                    page = 35
                    curseur = 1
                if curseur == 7:
                    page = 42
                    curseur = 1
                print(page+curseur)
    ligne[1]=switch_menu(page)
    ligne[2]=switch_menu(page+1)
    ligne[3]=switch_menu(page+2)
    ligne[4]=switch_menu(page+3)
    ligne[5]=switch_menu(page+4)
    ligne[6]=switch_menu(page+5)
    ligne[7]=switch_menu(page+6)
    #add curser on front on current selected line
    for n in range(1,8):
        if page+curseur == page+n:
            if page == 1:
                if readCapacity(bus) < 16:
                    ligne[n] = ligne[n].replace("_","!")
                else:
                    ligne[n] = ligne[n].replace("_",">")
            else:
                ligne[n] = ligne[n].replace("_",">")
        else:
            ligne[n] = ligne[n].replace("_"," ")
    DisplayText(ligne[1],ligne[2],ligne[3],ligne[4],ligne[5],ligne[6],ligne[7])
    #print(page+curseur) #debug trace menu value
    time.sleep(0.1)
    selection = 0
GPIO.cleanup()
