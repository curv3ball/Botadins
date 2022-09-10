import os
import win32api
import win32con
import time
import ctypes
import sys
import keyboard
import multiprocessing
import pyautogui
import images
from discord_webhook import *

webhook_url = ""

file = open(os.path.dirname(__file__) + '/../webhook.txt')
for line in file:
    webhook_url = line

webhook = DiscordWebhook(url=webhook_url, rate_limit_retry = True)
default_confidence = 0.9
activeResponse = None
safeSleep = 2 - (0.025 * multiprocessing.cpu_count())

def currentTime():
    return (time.strftime("%I:%M %p"))

def mouseMove(x, y):
    win32api.SetCursorPos((x, y))

def mouseClick(msg, a):
    print("clicking " + msg + " @ " + str(a))
    mouseMove(a[0], a[1])
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(safeSleep)

def play():
    
    searching = pyautogui.locateCenterOnScreen(images.searching, region=(1045, 115, 70, 50), confidence = default_confidence)

    if searching != None:
        return

    champions_button = pyautogui.locateCenterOnScreen(images.champions, region=(65, 175, 500, 350), confidence = default_confidence)
        
    play_button = pyautogui.locateCenterOnScreen(images.play_button, region=(65, 175, 500, 350), confidence = default_confidence)

    if champions_button != None and play_button != None:
        print("clicking champions_button")
        mouseClick("champions_button", champions_button)

        evie = pyautogui.locateOnScreen(images.evieSmall, region=(65, 240, 1000, 625), confidence = 0.7)

        if evie != None:
            print("sending discord webhook")
            championSnapshot = pyautogui.screenshot(region=(evie[0] - 5, evie[1] - 3, 100, 100))
            championSnapshot.save(images.currentLevel)
            profileSnapshot = pyautogui.screenshot(region=(1460, 963, 413, 93))
            profileSnapshot.save(images.currentProfile)

            webhook = DiscordWebhook(url = webhook_url, rate_limit_retry = True)
            webhook.remove_file('attachment://file1.png')
            webhook.remove_file('attachment://file2.png')

            with open(images.currentLevel, "rb") as f:
                webhook.add_file(file=f.read(), filename="file1.png")

            with open(images.currentProfile, "rb") as b:
                webhook.add_file(file=b.read(), filename="file2.png")

            global activeResponse

            if activeResponse != None:
                webhook.delete(activeResponse)

            activeResponse = webhook.execute()

        pyautogui.keyDown('escape'); time.sleep(0.1)
        pyautogui.keyUp('escape'); time.sleep(1)

        time.sleep(safeSleep)

        play_button = pyautogui.locateCenterOnScreen(images.play_button, region=(65, 175, 500, 350), confidence = default_confidence)

        if play_button != None:
            print("clicking play_button")
            mouseClick("play_button", play_button)

def main():
    while not keyboard.is_pressed("delete"):
        play()
    
    sys.exit()
    
main()