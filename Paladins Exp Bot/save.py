from turtle import goto
from pyautogui import *
from discord_webhook import *
import pyautogui
import time
import keyboard
import random
import os
import win32api, win32con
import subprocess

clear = lambda: os.system('cls')

def click(a): 
    win32api.SetCursorPos((a[0],a[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def click2():
    win32api.SetCursorPos((235, 297))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

webhook = DiscordWebhook(url='', rate_limit_retry=True)
response = None

start = time.time()

while True:
    if (time.time() - start >= 2700): # if 45minutes since started
        subprocess.call("TASKKILL /F /IM Paladins.exe", shell=True)
        time.sleep(5)
        subprocess.run("start steam://run/444090", shell=True)
        time.sleep(10)
        start = time.time()

    champ_select = pyautogui.locateCenterOnScreen("images/champions/sha/champ_select.png", confidence = 0.7)
    if champ_select != None: clear(); print("clicking champion"); click(champ_select)

    lock_in = pyautogui.locateCenterOnScreen("images/ui/lock_in.png", confidence = 0.7)
    if lock_in != None: clear(); print("locking in champion"); click(lock_in)

    ability = pyautogui.locateCenterOnScreen("images/champions/sha/ability.png", confidence = 0.8)   
    if ability != None: # anti-afk
        clear()
        print("afk")
        pyautogui.keyDown('w'); time.sleep(0.2)
        pyautogui.keyUp('w'); time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0); time.sleep(0.1); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0); time.sleep(0.1); win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
        pyautogui.keyDown('s'); time.sleep(0.2)
        pyautogui.keyUp('s'); time.sleep(15)

    play_button = pyautogui.locateCenterOnScreen("images/ui/play_button.png", confidence = 0.6)
    if play_button != None:
        clear()
        print("making champions variable")
        champions = pyautogui.locateCenterOnScreen("images/ui/champions.png", confidence = 0.6)
        if champions != None:
            clear()
            print("clicking champions")
            click2()
            win32api.SetCursorPos((5, 5))
            time.sleep(3)
            print("sending webhook")

            im = pyautogui.screenshot(region=(310, 490, 103, 103))
            im.save("images/currentLevel.png")

            webhook = DiscordWebhook(
                url = 'https://discord.com/api/webhooks/1014427274621239316/96JMPrJXduiuPhZEUFl39iAWjWuWihPLJuSi_gMAF4fvH6SsXwwi6jBS_unSqL5HqnCu', 
                rate_limit_retry=True, 
                )
            
            webhook.remove_file('attachment://file1.png')
            with open("images/currentLevel.png", "rb") as f: webhook.add_file(file=f.read(), filename="file1.png")
            
            if response != None:
                webhook.delete(response)

            response = webhook.execute()
             
            pyautogui.keyDown('escape'); time.sleep(0.2)
            pyautogui.keyUp('escape'); time.sleep(1)
        print("clicking play")
        click(play_button)

    training_gamemode = pyautogui.locateCenterOnScreen("images/ui/training_gamemode.png")
    if training_gamemode != None: clear(); print("clicking training"); click(training_gamemode)
    
    tdm_training = pyautogui.locateCenterOnScreen("images/ui/tdm_training.png")
    if tdm_training != None: clear(); print("clicking tdm"); click(tdm_training)
    
    talent = pyautogui.locateCenterOnScreen("images/champions/sha/talent.png", confidence = 0.7)
    if talent != None: clear(); print("clicking talent"); click(talent)

    card_deck = pyautogui.locateCenterOnScreen("images/champions/sha/card_deck.png", confidence = 0.7)
    if card_deck != None: clear(); print("clicking first card deck"); click(card_deck)

    equip = pyautogui.locateCenterOnScreen("images/ui/equip.png", confidence = 0.7)
    if equip != None: clear(); print("equipping card deck"); click(equip)
    
    match_summary = pyautogui.locateCenterOnScreen("images/ui/match_summary.png", confidence = 0.8)
    if match_summary != None:
        clear()
        print("game ended")
        time.sleep(3)
        pyautogui.keyDown('escape'); time.sleep(0.2)
        pyautogui.keyUp('escape'); time.sleep(2)

    purchase = pyautogui.locateCenterOnScreen("images/ui/purchase.png", confidence = 0.8)
    if purchase != None:
        clear()
        print("battle pass leveled")
        click(purchase)
