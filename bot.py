from ast import PyCF_ONLY_AST
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
import regions

from discord_webhook import *

webhook_url = ""

file = open(os.path.dirname(__file__) + '/../webhook.txt')
for line in file:
    webhook_url = line

webhook = DiscordWebhook(url=webhook_url, rate_limit_retry = True)
default_confidence = 0.9
activeResponse = None
safeSleep = 2 - (0.025 * multiprocessing.cpu_count())
lastUpdate = 0

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

def locateCenter(image, region, x = 0.9):
    return pyautogui.locateCenterOnScreen(image, region = (region), confidence = x)

def locate(image, region, x = 0.9):
    return pyautogui.locateOnScreen(image, region = (region), confidence = x)

def play():
    confidence = default_confidence
    try: searching = locateCenter(images.searching, regions.searching, confidence)
    except: print("failed to run locateCenter() on searching")

    if searching != None:
        return

    try: champions_button = locateCenter(images.champions, regions.main_menu, confidence)
    except: print("failed to run locateCenter() on champions_button")
        
    try: play_button = locateCenter(images.play_button, regions.main_menu, confidence)
    except: print("failed to run locateCenter() on play_button")

    if champions_button != None and play_button != None:
        try: mouseClick("champions_button", champions_button)
        except: print("mouseClick failed [location= " + str(champions_button) + "]")

        try: evie = locate(images.evieSmall, regions.champions, 0.7)
        except: print("failed to run locate() on evie")

        if evie != None:
            championSnapshot = pyautogui.screenshot(region=(evie[0] - 5, evie[1] - 3, 100, 100))
            championSnapshot.save(images.currentLevel)
            profileSnapshot = pyautogui.screenshot(region=(regions.player_profile))
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

        try: play_button = locateCenter(images.play_button, regions.main_menu, confidence)
        except: print("failed to run locateCenter() on play_button")

        if play_button != None:
            try: mouseClick("play_button", play_button)
            except: print("mouseClick failed [location= " + str(play_button) + "]")

def startMatch():
    confidence = default_confidence
    if not keyboard.is_pressed("delete"):
        gamemode_top = None
        gamemode_bottom = None
        
        try: gamemode_top = locateCenter(images.training_gamemode, regions.gamemode_select_top, confidence)
        except: print("failed to run locateCenter() on gamemode_top")

        if gamemode_top != None:
            try: mouseClick("gamemode_top", gamemode_top)
            except: print("mouseClick failed [location= " + str(gamemode_top) + "]")

        try: gamemode_bottom = locateCenter(images.tdm_training, regions.gamemode_select_bottom, confidence)
        except: print("failed to run locateCenter() on gamemode_bottom")
        
        if gamemode_bottom != None:
            try: mouseClick("gamemode_bottom", gamemode_bottom)
            except: print("mouseClick failed [location= " + str(gamemode_bottom) + "]")

def main():
    print("______       _            _ _           ")
    print("| ___ \     | |          | (_)          ")
    print("| |_/ / ___ | |_ __ _  __| |_ _ __  ___ ")
    print("| ___ \/ _ \| __/ _` |/ _` | | '_ \/ __|")
    print("| |_/ / (_) | || (_| | (_| | | | | \__ " + '\\')
    print("\____/ \___/ \__\__,_|\__,_|_|_| |_|___/  v2.8.5 by curv3#0984\n\n")

    confidence = default_confidence                    
    
    while not keyboard.is_pressed("delete"):
        play()

main()
sys.exit(0)