from pickletools import pytuple
import time
import os
import win32api
import win32con
import subprocess
import pyautogui
from datetime import datetime

# local variables
clear = lambda: os.system('cls')

def mouseMove(x, y):
    win32api.SetCursorPos((x, y))

# standard mouse_event
def click(msg, a): log(msg); win32api.SetCursorPos((a[0],a[1])); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0); time.sleep(0.2); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# hardcoded mouse_event cause lazy
def click2(): win32api.SetCursorPos((235, 297)); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0); time.sleep(0.2); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# logs to file
def log(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    x = open("logs.txt", "a")
    x.write("[" + current_time + "] " + str(msg) + "\n")
    lambda: os.system('cls')
    print(str(msg))

# kills paladins.exe and restart it via steam
def restartGame():
    subprocess.call("TASKKILL /F /IM Paladins.exe", shell=True)
    time.sleep(5)
    subprocess.run("start steam://run/444090", shell=True)
    start = time.time()

def locateCenter(image, region, x = 0.7):
    return pyautogui.locateCenterOnScreen(
        image, 
        region=(region), 
        confidence = x
    )

def locate(image, region, x = 0.7):
    return pyautogui.locateOnScreen(
        image,
        region = (region),
        confidence = x
    )