# Basic command

* execcmd(cmd), execute the command, return -1 if error, str(shell output) otherwise
* execcmdNostr(cmd), execute the command, return -1 if error, shell output otherwise
* displayError()

example:
ret=execcmd("hostname -I")
if(ret==-1):
    displayError()
    return()


* autoKillCommand(tx1,time), execute the command "tx1" for "time" seconds, return -1 if error, no output otherwise. Usefull for command thaht dosent write any output such as AIRODUMP or HTOP. 
* checklist(_list), shows a selection menu for a given list of entry, return the selected entry.

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
               
