import os
import regions
import win32api
import time
import win32con
import subprocess

try: import pyautogui
except: print("failed to import pyautogui module, installing it now"); os.system('pip install pyautogui')

try: import configparser
except: print("failed to import configparser module, installing it now"); os.system('pip install configparser')

try: import keyboard
except: print("failed to import keyboard module, installing it now"); os.system('pip install keyboard')

try: import discord_webhook
except: print("failed to import discord_webhook module, installing it now"); os.system('pip install discord_webhook')

try: from discord_webhook import *
except: print("failed to import discord_webhook module, try restarting")

try: os.system('pip install Pillow --upgrade')
except: print("failed to update Pillow")

try: os.system('pip install opencv-python')
except: print("failed to install opencv-python")

try: os.system('pip install pypiwin32')
except: print("failed to install opencv-python")

# setup settings.ini
config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../settings.ini')
champion = None
webhook = None

if 'champion' in config['Default']:
    try:
        champions = ['Androxus', 'Ash', 'Atlas', 'Azaan', 'Barik', 'Betty La Bomba', 'Bomb King', 'Buck', 'Cassie', 'Corvus', 'Dredge', 'Drogoz', 'Evie', 'Fernando', 'Furia', 'Grohk', 'Grover', 'Imani', 'Inara', 'IO', 'Jenos', 'Khan', 'Kinessa', 'Koga' 'Lex', 'Lian', 'Lillith', 'Maeve', 'Makoa', "Mal'Damba", 'Moji', 'Octavia',  'Pip', 'Raum', 'Rei', 'Ruckus', 'Saati', 'Seris', 'Sha Lin', 'Skye', 'Strix', 'Talus', 'Terminus', 'Tiberius', 'Torvald', 'Tyra', 'VII', 'Vatu', 'Viktor',  'Vivian', 'Vora', 'Willo', 'Yagorath', 'Ying', 'Zhin']
        content = config['Default']['Champion']

        if content in champions:
            champion = str(content)
        else:
            champion = "Ash"

    except: print("error setting champion from config")
else:
    print('champion not found in config')

if 'webhook' in config['Misc']:
    try:
        content = config['Misc']['Webhook']
        if content.find('https://discord.com/api/webhooks/') != -1:
            webhook = str(content)
        else:
            webhook = ""
    except: print("error setting webhook from config")
else:
    print('webhook not found in config')