import subprocess
import pyautogui
import webbrowser
import time
import os
import getpass

USER_NAME = getpass.getuser()


def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)

#Open Outlook
subprocess.Popen(r'C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE')
#Open OneNote
subprocess.Popen(r'C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE')


################OPEN ALL################
webbrowser.open('https://teams.microsoft.com/')
webbrowser.open('https://youtube.com/')
#webbrowser.open('https://Site.example/')



####sleepy tiem####
time.sleep(3)

#######SEPERATE TABS#########
pyautogui.click(56,14)
with pyautogui.hold('shift'):
    pyautogui.click(365, 21)
    pyautogui.drag(0,150,.5)

with pyautogui.hold('win'):
    pyautogui.press('right')
    time.sleep(.25)
    pyautogui.press('right')
    time.sleep(.25)
    pyautogui.press('right')
    time.sleep(.25)

pyautogui.moveTo(587, 13)
pyautogui.drag(-400, 0, 1, button='left')
pyautogui.moveTo(587, 13)
pyautogui.drag(-200, 0, 1, button='left')


#import virtualbox

#vbox = virtualbox.VirtualBox()
#machine = vbox.find_machine("you_virtual_machine_name")  
#proc = machine.launch_vm_process(session, "gui")