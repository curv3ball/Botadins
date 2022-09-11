import regions
import images
import os
import win32api
import win32con
import time
import ctypes
import multiprocessing
import subprocess
import sys
import datetime

try: import keyboard
except: print("failed to import keyboard module, installing it now"); os.system('pip install keyboard')

try: import pyautogui
except: print("failed to import pyautogui module, installing it now"); os.system('pip install pyautogui')

try: import discord_webhook
except: print("failed to import discord_webhook module, installing it now"); os.system('pip install discord_webhook')

try: from discord_webhook import *
except: print("discord_webhook not installed, try restarting this program")

try: os.system('pip install Pillow --upgrade')
except: print("failed to update Pillow")

try: os.system('pip install opencv-python')
except: print("failed to install opencv-python")

os.system("cls")

webhook_url = ""

file = open(os.path.dirname(__file__) + '/../webhook.txt')
for line in file:
    webhook_url = line

webhook = DiscordWebhook(url=webhook_url, rate_limit_retry = True)
default_confidence = 0.9
activeResponse = None
safeSleep = 2 - (0.025 * multiprocessing.cpu_count())
championSpawned = False

def currentTime():
    return (time.strftime("%I:%M %p"))

def mouseMove(x, y):
    win32api.SetCursorPos((x, y))

# standard mouse_event
def mouseClick(msg, a): log(msg); win32api.SetCursorPos((a[0],a[1])); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0); time.sleep(0.2); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


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

def play():
    confidence = default_confidence
    while not keyboard.is_pressed("delete"):
        searching = None
        champions_button = None
        play_button = None

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

            try: vii = locate(images.viiSmall, regions.champions, 0.7)
            except: print("failed to run locate() on vii")

            if vii != None:
                championSnapshot = pyautogui.screenshot(region=(vii[0] - 5, vii[1] - 3, 100, 100))
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
    while not keyboard.is_pressed("delete"):
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

def lockChampion():
    confidence = default_confidence
    while not keyboard.is_pressed("delete"):
        champion_select = None
        champion_lock = None

        try: champion_select = locateCenter(images.viiChampSelect, regions.champion_select, confidence)
        except: print("failed to run locateCenter() on champion_select")
        
        if champion_select != None:
            try: mouseClick("champion_select", champion_select)
            except: print("mouseClick failed [location= " + str(champion_select) + "]")

        try: champion_lock = locateCenter(images.lock_in, regions.champion_select, confidence)
        except: print("failed to run locateCenter() on champion_lock")
        
        if champion_lock != None:
            try: mouseClick("champion_lock", champion_lock)
            except: print("mouseClick failed [location= " + str(champion_lock) + "]")

def spawnChampion():
    confidence = default_confidence
    while not keyboard.is_pressed("delete"):
        talent_select = None
        loadout_select = None
        loadout_equip = None

        try: talent_select = locateCenter(images.viiTalent, regions.talent_select, confidence)
        except: print("failed to run locateCenter() on talent_select")

        if talent_select != None:
            try: mouseClick("talent_select", talent_select)
            except: print("mouseClick failed [location= " + str(talent_select) + "]")

        try: loadout_select = locateCenter(images.viiCard, regions.loadout_select, confidence)
        except: print("failed to run locateCenter() on loadout_select")

        if loadout_select != None:
            try: mouseClick("loadout_select", loadout_select)
            except: print("mouseClick failed [location= " + str(loadout_select) + "]")

        try: loadout_equip = locateCenter(images.equip, regions.loadout_equip, confidence)
        except: print("failed to run locateCenter() on loadout_equip")

        if loadout_equip != None:
            try: mouseClick("loadout_equip", loadout_equip)
            except: print("mouseClick failed [location= " + str(loadout_equip) + "]")

        championSpawned = True

def Extra():
    confidence = default_confidence
    while not keyboard.is_pressed("delete"):
        spawned = None
        home = None
        purchase = None
        ok = None

        try: spawned = locateCenter(images.viiSpawned, regions.spawned, 0.7)
        except: print("failed to run locateCenter() on ability")
        
        if spawned != None:
            try:
                print("afking")
                pyautogui.keyDown('w'); time.sleep(0.1)
                pyautogui.keyUp('w'); time.sleep(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0); time.sleep(0.1); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0); time.sleep(0.1); win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
                pyautogui.keyDown('s'); time.sleep(0.1)
                pyautogui.keyUp('s'); time.sleep(1)
            except: print("failure running antiafk()")

        try: home = locateCenter(images.home, regions.home, 0.6)
        except: print("failed to run locateCenter() on end_game")

        if home != None:
            try: mouseClick("home", home)
            except: print("mouseClick failed [location= " + str(home) + "]")

        purchase = pyautogui.locateCenterOnScreen(images.purchase, confidence = default_confidence)
        if purchase != None:
            try: mouseClick("purchase", purchase)
            except: print("mouseClickw failed [location= " + str(purchase) + "]")

        ok = pyautogui.locateCenterOnScreen(images.ok, confidence = default_confidence)
        if ok != None:
            try: mouseClick("ok", ok)
            except: print("mouseClick failed [wlocation= " + str(ok) + "]")
