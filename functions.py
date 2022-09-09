from turtle import home
from imports import *
import regions
import images

webhook_url = ""

file = open(os.path.dirname(__file__) + '/../webhook.txt')
for line in file:
    print("set wehook_url to " + line)
    webhook_url = line

webhook = DiscordWebhook(url=webhook_url, rate_limit_retry = True)
default_confidence = 0.9
activeResponse = None
safeSleep = 2 - (0.025 * multiprocessing.cpu_count())
lastUpdate = 0

def currentTime():
    return (time.strftime("%I:%M %p"))

def closeBot():
    ctypes.windll.user32.MessageBoxW(0, "The bot has been stopped!", "Botadins", 0)
    sys.exit(0)

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
    while not keyboard.is_pressed("delete"):
        searching = None
        try: searching = locateCenter(images.searching, regions.searching, confidence)
        except: print("failed to run locateCenter() on searching")

        if searching != None:
            continue

        try: champions_button = locateCenter(images.champions, regions.main_menu, confidence)
        except: print("failed to run locateCenter() on champions_button")
        
        try: play_button = locateCenter(images.play_button, regions.main_menu, confidence)
        except: print("failed to run locateCenter() on play_button")

        if champions_button != None and play_button != None:
            try: mouseClick("champions_button", champions_button)
            except: print("mouseClick failed [location= " + str(champions_button) + "]")

            try: androxus = locate(images.androxusSmall, regions.champions, 0.7)
            except: print("failed to run locate() on androxus")

            if androxus != None:
                championSnapshot = pyautogui.screenshot(region=(androxus[0] - 5, androxus[1] - 3, 100, 100))
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
        try: champion_select = locateCenter(images.androxusChampSelect, regions.champion_select, confidence)
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
        try: talent_select = locateCenter(images.androxusTalent, regions.talent_select, confidence)
        except: print("failed to run locateCenter() on talent_select")

        if talent_select != None:
            try: mouseClick("talent_select", talent_select)
            except: print("mouseClick failed [location= " + str(talent_select) + "]")

        try: loadout_select = locateCenter(images.androxusCard, regions.loadout_select, confidence)
        except: print("failed to run locateCenter() on loadout_select")

        if loadout_select != None:
            try: mouseClick("loadout_select", loadout_select)
            except: print("mouseClick failed [location= " + str(loadout_select) + "]")

        try: loadout_equip = locateCenter(images.equip, regions.loadout_equip, confidence)
        except: print("failed to run locateCenter() on loadout_equip")

        if loadout_equip != None:
            try: mouseClick("loadout_equip", loadout_equip)
            except: print("mouseClick failed [location= " + str(loadout_equip) + "]")

def antiAFK():
    confidence = default_confidence
    while not keyboard.is_pressed("delete"):
        try: ability = locateCenter(images.androxusAbility, regions.abilities_select, confidence)
        except: print("failed to run locateCenter() on ability")

        if ability != None:
            try: 
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
            except: print("mouseClick failed [location= " + str(purchase) + "]")

        ok = pyautogui.locateCenterOnScreen(images.ok, confidence = default_confidence)
        if ok != None:
            try: mouseClick("ok", ok)
            except: print("mouseClick failed [location= " + str(ok) + "]")
