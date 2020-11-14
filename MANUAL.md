# Basic command

* execcmd(cmd), execute the command, return -1 if error, str(shell output) otherwise
* execcmdNostr(cmd), execute the command, return -1 if error, shell output otherwise
* displayError()
* displayMsg(msg,t), shows a short "msg" message for "t" seconds

example:

    ret=execcmd("hostname -I")
    if(ret==-1):
        displayError()    
        return()



* autoKillCommand(tx1,t), execute the command "tx1" for "t" seconds,it also kills the process return -1 if error, no output otherwise. Usefull for command thaht dosent write any output such as AIRODUMP or HTOP. 
* autoKillCommandNoKill(tx1,t), execute the command "tx1" for "t" seconds,not kills the process return -1 if error, no output otherwise. Usefull if u want to kill the process before the time "t".
* killCommand(cmd), kills ALL the commands that contains "cmd", example: cmd="ps -aux | grep cmd  | head -n 1 | cut -d ' ' -f7"
* checklist(_list), shows a selection menu for a given list of entry, return the selected entry.
* waitingLoop(msg), display a message "msg" and waits ultil the user will press "right"

example:

    cmdMail = "mailsnarf -i wlan0 > Mail"+str(victimIP)+".mbox"
    if(autoKillCommandNoKill(cmdMail,myTime)==-1):
        displayError()
        return()
    time.sleep(10)
    waitingLoop("press right to exit")      
    killCommand("mailsnarf")


# Add a new menu/submenu
* on the switch_menu(argument) function add 7 new entrys.
example:
###### newmenu
        49: "_WIRED THINGS",
        50: "_newsubmenu2",
        51: "_newsubmenu3",
        52: "_newsubmenu4",
        53: "_newsubmenu5",
        54: "_newsubmenu6",
        55: "_UpdateOledMenu",
* on the main() funciton add:
###### new menus section
            if (page == 49): 
                if curseur == 1:
                    page = 56
                if curseur == 7:
                    page = update()

# Add a new submenu
* on the switch_menu(argument) function add 7 new entrys.
example:
###### newsections
        56: "_Nmap 172.16.0.2",
        57: "_",
        58: "_",
        59: "_",
        60: "_",
        61: "_",
        62: "_",
###### new menus section
            if (page == 56): 
                if curseur == 1:
                    page = nmapLocal()
               
