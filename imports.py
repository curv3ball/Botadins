import os
import win32api
import win32con
import time
import ctypes
import sys
import threading
import multiprocessing

def importlog(m):
    print("importing module " + m)

try: importlog("discord_webhook"); from discord_webhook import *
except: print("discord_webhook module not loaded")

try: importlog("keyboard"); import keyboard
except: print("keyboard module not loaded")

try: importlog("pyautogui"); import pyautogui
except: print("pyautogui module not loaded")
