# global files
import time
import random
import os
import win32api
import win32con
import subprocess
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

# project files
import regions

# local variables
version = "v2.8.6"
webhook_url = ""
file = open(os.path.dirname(__file__) + '/../webhook.txt')
for line in file: webhook_url = line
webhook = DiscordWebhook(url=webhook_url, rate_limit_retry = True)
response = None
start = time.time()
default_confidence = 0.9

def locateCenter(image, region, x = 0.7): return pyautogui.locateCenterOnScreen(image, region=(region), confidence = x )

def locate(image, region, x = 0.7):
    return pyautogui.locateOnScreen(image, region = (region), confidence = x)

# logs to file
def log(msg):
    x = open("logs.txt", "a")
    x.write(str(msg) + "\n")
    lambda: os.system('cls')
    print(str(msg))

def currentTime():
    return (time.strftime("%I:%M %p"))

def mouseMove(x, y):
    win32api.SetCursorPos((x, y))

# standard mouse_event
def mouseClick(msg, a): log(msg); win32api.SetCursorPos((a[0],a[1])); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0); time.sleep(0.2); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


print("______       _            _ _           ")
print("| ___ \     | |          | (_)          ")
print("| |_/ / ___ | |_ __ _  __| |_ _ __  ___ ")
print("| ___ \/ _ \| __/ _` |/ _` | | '_ \/ __|")
print("| |_/ / (_) | || (_| | (_| | | | | \__ " + '\\')
print("\____/ \___/ \__\__,_|\__,_|_|_| |_|___/  " + version + " by curv3#0984\n\n")

while not keyboard.is_pressed("delete"):
    champion_select = locateCenter('images/champions/androxus/champ_select.png', regions.champion_select, 0.8)
    if champion_select != None:
        mouseClick("champion_select [" + str(champion_select) + "]", champion_select)

    champion_lock = locateCenter('images/ui/lock_in.png', regions.champion_select, default_confidence)
    if champion_lock != None:
        mouseClick("champion_lock [" + str(champion_lock) + "]", champion_lock)

    champions_button = locateCenter('images/ui/champions.png', regions.main_menu, default_confidence)
    play_button = locateCenter('images/ui/play_button.png', regions.main_menu, default_confidence)
    if champions_button != None and play_button != None:
        mouseClick("champions_button [" + str(champions_button) + "]", champions_button)
        mouseMove(15, 15); time.sleep(1)
        
        androxus = locate("images/champions/androxus/pic.png", regions.champions, default_confidence)
        if androxus != None:
            pic = pyautogui.screenshot(region=(androxus[0] - 5, androxus[1] - 3, 100, 100))
            pic2 = pyautogui.screenshot(region=(regions.player_profile))
            pic2.save("images/currentProfile.png")
            pic.save("images/currentLevel.png")

            webhook = DiscordWebhook( url = webhook_url,  rate_limit_retry=True)
            webhook.remove_file('attachment://file1.png')
            webhook.remove_file('attachment://file2.png')

            with open("images/currentLevel.png", "rb") as f: 
                webhook.add_file(file=f.read(), filename="file1.png")

            with open("images/currentProfile.png", "rb") as b:
                webhook.add_file(file=b.read(), filename="file2.png")

            if response != None:
                webhook.delete(response)
            
            log("sending webhook")
            response = webhook.execute()

        pyautogui.keyDown('escape'); time.sleep(0.2)
        pyautogui.keyUp('escape'); time.sleep(1)
        
        if play_button != None:
            mouseClick("play_button [" + str(play_button) + "]", play_button)

    gamemode_top = locateCenter('images/ui/training_gamemode.png', regions.gamemode_select_top, default_confidence)
    if gamemode_top != None:
        mouseClick("gamemode_top [" + str(gamemode_top) + "]", gamemode_top)

    gamemode_bottom = locateCenter('images/ui/tdm_training.png', regions.gamemode_select_bottom, default_confidence)
    if gamemode_bottom != None:
        mouseClick("gamemode_bottom [" + str(gamemode_bottom) + "]", gamemode_bottom)

    talent_select = locateCenter('images/champions/androxus/talent.png', regions.talent_select, default_confidence)
    if talent_select != None:
        mouseClick("talent_select [" + str(talent_select) + "]", talent_select)

    loadout_select = locateCenter('images/champions/androxus/card_deck.png', regions.loadout_select, default_confidence)
    if loadout_select != None:
        mouseClick("loadout_select [" + str(loadout_select) + "]", loadout_select)

    loadout_equip = locateCenter('images/ui/equip.png', regions.loadout_equip, default_confidence)
    if loadout_equip != None:
        mouseClick("loadout_equip [" + str(loadout_equip) + "]", loadout_equip)
    
    spawned = locateCenter('images/champions/androxus/spawned.png', regions.spawned, default_confidence)
    if spawned != None:
        pyautogui.keyDown('w'); time.sleep(0.1)
        pyautogui.keyUp('w'); time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0); time.sleep(0.1); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0); time.sleep(0.1); win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
        pyautogui.keyDown('s'); time.sleep(0.1)
        pyautogui.keyUp('s'); time.sleep(1)

    endgame_summary = locateCenter('images/ui/match_summary.png', regions.endgame_top, default_confidence)
    if endgame_summary != None:
        pyautogui.keyDown('escape'); time.sleep(0.2)
        pyautogui.keyUp('escape'); time.sleep(1)

    purchase = pyautogui.locateCenterOnScreen("images/ui/purchase.png", confidence = 0.8)
    if purchase != None:
        mouseClick("battlepass [" + str(purchase) + "]", purchase)

    ok = pyautogui.locateCenterOnScreen("images/ui/ok.png", confidence = 0.7)
    if ok != None:
        mouseClick("ok [" + str(ok) + "]", ok)

print("bot stopped")