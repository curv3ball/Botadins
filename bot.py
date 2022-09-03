# global files
from json import load
from discord_webhook import *
import pyautogui
import time
import random
import os
import win32api
import win32con
import subprocess

# project files
import functions
import regions

# local variables
webhook = DiscordWebhook(url=' ', rate_limit_retry=True)
response = None
btime = 0
start = time.time()
default_confidence = 0.9

while True:
    if (time.time() - start >= 2700): # 2700 / 60 = 45
        functions.log("restarting game")
        functions.restartGame()

    champion_select = functions.locateCenter('images/champions/sha/champ_select.png', regions.champion_select, 0.8)
    if champion_select != None:
        functions.click("champion_select [" + str(champion_select) + "]", champion_select)

    champion_lock = functions.locateCenter('images/ui/lock_in.png', regions.champion_select, default_confidence)
    if champion_lock != None:
        functions.click("champion_lock [" + str(champion_lock) + "]", champion_lock)

    champions_button = functions.locateCenter('images/ui/champions.png', regions.main_menu, default_confidence)
    play_button = functions.locateCenter('images/ui/play_button.png', regions.main_menu, default_confidence)
    if champions_button != None and play_button != None:
        functions.click("champions_button [" + str(champions_button) + "]", champions_button)
        functions.mouseMove(15, 15); time.sleep(1)
        
        sha = functions.locate("images/champions/sha/pic.png", regions.champions, default_confidence)
        if sha != None:
            pic = pyautogui.screenshot(region=(sha[0] - 2, sha[1] - 2, 100, 100))
            pic.save("images/currentLevel.png")

            webhook = DiscordWebhook( url = ' ',  rate_limit_retry=True)
            webhook.remove_file('attachment://file1.png')

            with open("images/currentLevel.png", "rb") as f: 
                webhook.add_file(file=f.read(), filename="file1.png")

            if response != None:
                webhook.delete(response)
            
            functions.log("sending webhook")
            response = webhook.execute()

        pyautogui.keyDown('escape'); time.sleep(0.2)
        pyautogui.keyUp('escape'); time.sleep(1)
        
        if play_button != None:
            functions.click("play_button [" + str(play_button) + "]", play_button)

    gamemode_top = functions.locateCenter('images/ui/training_gamemode.png', regions.gamemode_select_top, default_confidence)
    if gamemode_top != None:
        functions.click("gamemode_top [" + str(gamemode_top) + "]", gamemode_top)

    gamemode_bottom = functions.locateCenter('images/ui/tdm_training.png', regions.gamemode_select_bottom, default_confidence)
    if gamemode_bottom != None:
        functions.click("gamemode_bottom [" + str(gamemode_bottom) + "]", gamemode_bottom)

    talent_select = functions.locateCenter('images/champions/sha/talent.png', regions.talent_select, default_confidence)
    if talent_select != None:
        functions.click("talent_select [" + str(talent_select) + "]", talent_select)

    loadout_select = functions.locateCenter('images/champions/sha/card_deck.png', regions.loadout_select, default_confidence)
    if loadout_select != None:
        functions.click("loadout_select [" + str(loadout_select) + "]", loadout_select)

    loadout_equip = functions.locateCenter('images/ui/equip.png', regions.loadout_equip, default_confidence)
    if loadout_equip != None:
        functions.click("loadout_equip [" + str(loadout_equip) + "]", loadout_equip)
    
    abilities_select = functions.locateCenter('images/champions/sha/ability.png', regions.abilities_select, default_confidence)
    if abilities_select != None:
        pyautogui.keyDown('w'); time.sleep(0.1)
        pyautogui.keyUp('w'); time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0); time.sleep(0.1); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0); time.sleep(0.1); win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
        pyautogui.keyDown('s'); time.sleep(0.1)
        pyautogui.keyUp('s'); time.sleep(1)
    