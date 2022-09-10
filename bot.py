import os
import win32api
import win32con
import time
import ctypes
import sys
import functions
import keyboard

print("______       _            _ _           ")
print("| ___ \     | |          | (_)          ")
print("| |_/ / ___ | |_ __ _  __| |_ _ __  ___ ")
print("| ___ \/ _ \| __/ _` |/ _` | | '_ \/ __|")
print("| |_/ / (_) | || (_| | (_| | | | | \__ " + '\\')
print("\____/ \___/ \__\__,_|\__,_|_|_| |_|___/  v2.8.5 by curv3#0984\n\n")
                                    
while not keyboard.is_pressed("delete"):
    functions.play()
    functions.startMatch()
    functions.lockChampion()
    functions.spawnChampion()
    functions.antiAFK()
    
sys.exit(0)