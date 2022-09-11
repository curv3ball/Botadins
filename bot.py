import time
import os
import ctypes
import sys
import threading
import multiprocessing
import functions

try: import keyboard
except: print("failed to import keyboard module, installing it now"); os.system('pip install keyboard')

try: os.system('pip install Pillow --upgrade')
except: print("failed to update Pillow")

try: os.system('pip install opencv-python')
except: print("failed to install opencv-python")

version = "v2.8.5"

if __name__ == '__main__':

    os.system("cls")

    Play = threading.Thread(target=functions.play)
    BotTDM = threading.Thread(target=functions.startMatch)
    ChampionSelect = threading.Thread(target=functions.lockChampion)
    SpawnCharacter = threading.Thread(target=functions.spawnChampion)
    Extra = threading.Thread(target=functions.Extra)

    Play.start()
    BotTDM.start()
    ChampionSelect.start()
    SpawnCharacter.start()
    Extra.start()

    print("______       _            _ _           ")
    print("| ___ \     | |          | (_)          ")
    print("| |_/ / ___ | |_ __ _  __| |_ _ __  ___ ")
    print("| ___ \/ _ \| __/ _` |/ _` | | '_ \/ __|")
    print("| |_/ / (_) | || (_| | (_| | | | | \__ " + '\\')
    print("\____/ \___/ \__\__,_|\__,_|_|_| |_|___/  " + version + " by curv3#0984")
    print("processor is set to '" + str(functions.safeSleep) + "' to account for your cpu count of '" + str(multiprocessing.cpu_count()) + "'\n\n")

    while keyboard.is_pressed("delete"):
        Play.join()
        BotTDM.join()
        ChampionSelect.join()
        SpawnCharacter.join()
        Extra.join()
        sys.exit(0)