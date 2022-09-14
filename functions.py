from imports import *

version = "2.9.0"
default_confidence = 0.8
response = None
logCount = 0

def watermark():
    os.system("cls")
    print(f" ______       _            _ _           ")
    print(f" | ___ \     | |          | (_)          ")
    print(f" | |_/ / ___ | |_ __ _  __| |_ _ __  ___ ")
    print(f" | ___ \/ _ \| __/ _` |/ _` | | '_ \/ __|")
    print(f" | |_/ / (_) | || (_| | (_| | | | | \__ " + '\\')
    print(f" \____/ \___/ \__\__,_|\__,_|_|_| |_|___/  {version} by curv3#0984\n\n")

def log(msg):
    global logCount
    logCount += 1
    if logCount > 15:
        watermark()
    x = open("logs.txt", "a")
    x.write(msg + "\n")
    print(f" {msg}")

def gameRunning():
    call = 'TASKLIST', '/FI', 'imagename eq %s' % 'Paladins.exe'
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith('Paladins.exe'.lower())

def mouseMove(x, y):
    for n in range(10):
        try:
            w = int(pyautogui.position()[0] + (x - pyautogui.position()[0]) / 10 * n)
            h = int(pyautogui.position()[1] + (y - pyautogui.position()[1]) / 10 * n)
            win32api.SetCursorPos((w, h))
        except: continue
        time.sleep(0.05/10)

def mouseMoveClick(vector, name = ""):
    log(f"moving mouse and clicking {name} @ {str(vector)}")
    mouseMove(vector[0], vector[1])
    try:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.20)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    except: return
    time.sleep(1)

def champion_select():
    champion_frame = None
    lock_in = None

    try: champion_frame = pyautogui.locateCenterOnScreen('images/champions/' + champion.lower() + '/champion_select.png', region=(regions.champion_select), confidence = default_confidence)
    except: return

    if champion_frame != None:
        mouseMoveClick(champion_frame, 'champion_frame')

    try: lock_in = pyautogui.locateCenterOnScreen('images/ui/lock_in.png', region=(regions.lock_in), confidence = default_confidence)
    except: return

    if lock_in != None:
        mouseMoveClick(lock_in, 'lock_in')

def play_game():
    play_button = None
    champions_button = None  
    try: play_button = pyautogui.locateCenterOnScreen('images/ui/play_button.png', region=(regions.main_menu), confidence = default_confidence)
    except: return

    try: champions_button = pyautogui.locateCenterOnScreen('images/ui/champions_button.png', region=(regions.main_menu), confidence = default_confidence)
    except: return

    if play_button != None and champions_button != None:
        
        if webhook.find('https://discord.com/api/webhooks/') != -1:
            global response
            mouseMoveClick(champions_button, 'champions_button')

            scroll = None
            try: scroll = pyautogui.locateCenterOnScreen('images/ui/double_arrow.png', region=(regions.double_arrow), confidence = default_confidence)
            except: return

            if scroll != None:
                mouseMoveClick(scroll, 'scroll')

                mastery_filter = None
                try: mastery_filter = pyautogui.locateCenterOnScreen('images/ui/mastery_filter.png', region=(regions.mastery_filter), confidence = default_confidence)
                except: return

                if mastery_filter != None:
                    mouseMoveClick(mastery_filter, 'mastery_filter')

                    role_filter = None
                    try: role_filter = pyautogui.locateCenterOnScreen('images/ui/role_filter.png', region=(regions.role_filter), confidence = default_confidence)
                    except: return

                    if role_filter != None:
                        mouseMoveClick(role_filter, 'role_filter')

                    mastery = None
                    try: mastery = pyautogui.locateOnScreen('images/champions/' + champion.lower() + '/mastery.png', region=(regions.champion_mastery), confidence = 0.7)
                    except: return

                    if mastery != None:
                        screenshot1 = pyautogui.screenshot(region=(mastery[0] - 3, mastery[1] - 3, 100, 100))
                        screenshot2 = pyautogui.screenshot(region=(regions.player_profile))
                        screenshot1.save('images/champions/' + champion + '/current_mastery.png')
                        screenshot2.save('images/current_profile_level.png')

                        wh = DiscordWebhook( url = webhook,  rate_limit_retry = True)
                        wh.remove_file('attachment://file1.png')
                        wh.remove_file('attachment://file2.png')

                        with open('images/champions/' + champion + '/current_mastery.png', "rb") as f: 
                            wh.add_file(file = f.read(), filename = "file1.png")

                        with open('images/current_profile_level.png', "rb") as b:
                            wh.add_file(file = b.read(), filename = "file2.png")

                        if response != None:
                            log(f"deleting old webhook")
                            wh.delete(response)

                        log(f"updating webhook")
                        response = wh.execute()

            close = None
            try: close = pyautogui.locateCenterOnScreen('images/ui/menu_x.png', region=(regions.menu_x), confidence = default_confidence)
            except: return

            if close != None:
                mouseMoveClick(close, 'close')
                time.sleep(1)
                mouseMoveClick(play_button, 'play_button')
        else:
            mouseMoveClick(play_button, 'play_button')
                    
def bot_tdm():
    gamemode_top = None
    gamemode_bottom = None

    try: gamemode_top = pyautogui.locateCenterOnScreen('images/ui/training_gamemode.png', region=(regions.gamemode_select_top), confidence = default_confidence)
    except: return

    if gamemode_top != None:
        mouseMoveClick(gamemode_top, 'gamemode_top')
        
    try: gamemode_bottom = pyautogui.locateCenterOnScreen('images/ui/tdm_training.png', region=(regions.gamemode_select_bottom), confidence = default_confidence)
    except: return

    if gamemode_bottom != None:
        mouseMoveClick(gamemode_bottom, 'gamemode_bottom')

    
        
def spawn_champion():
    # fix for octavia, she has a special screen
    if champion.lower() == "octavia":
        passive = None

        try: passive = pyautogui.locateCenterOnScreen('images/champions/' + champion.lower() + '/team_passive.png', region=(regions.octavia_passive), confidence = 0.7)
        except: return
        if passive != None:
            mouseMoveClick(passive, 'passive')

    talent = None
    loadout = None
    equip = None

    try: talent = pyautogui.locateCenterOnScreen('images/champions/' + champion.lower() + '/talent.png', region=(regions.talent_select), confidence = default_confidence)
    except: return

    if talent != None:
        mouseMoveClick(talent, 'talent')

    try: loadout = pyautogui.locateCenterOnScreen('images/champions/' + champion.lower() + '/card_deck.png', region=(regions.loadout_select), confidence = default_confidence)
    except: return

    if loadout != None:
        mouseMoveClick(loadout, 'loadout')

    try: equip = pyautogui.locateCenterOnScreen('images/ui/equip.png', region=(regions.loadout_equip), confidence = default_confidence)
    except: return

    if equip != None:
        mouseMoveClick(equip, 'equip')

def anti_afk():
    spawned = None
    try: spawned = pyautogui.locateCenterOnScreen('images/champions/' + champion.lower() + '/spawned.png', region=(regions.spawned), confidence = default_confidence)
    except: return

    if spawned != None:
        pyautogui.keyDown('w'); time.sleep(0.1)
        pyautogui.keyUp('w'); time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0); time.sleep(0.1); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0); time.sleep(0.1); win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
        pyautogui.keyDown('s'); time.sleep(0.1)
        pyautogui.keyUp('s'); time.sleep(1)

def end_game():
    summary = None
    try: summary = pyautogui.locateCenterOnScreen('images/ui/match_summary.png', region=(regions.endgame_top), confidence = default_confidence)
    except: return

    if summary != None:
        close = None

        try: close = pyautogui.locateCenterOnScreen('images/ui/menu_x.png', region=(regions.menu_x), confidence = default_confidence)
        except: return

        if close != None:
            mouseMoveClick(close, 'close')

def misc():
    purchase = None
    ok = None
    ok2 = None
    close = None
    cancel = None
    continue_ = None

    try: purchase = pyautogui.locateCenterOnScreen('images/ui/purchase.png', confidence = default_confidence)
    except: return

    if purchase != None:
        mouseMoveClick(purchase, 'purchase')

    try: ok = pyautogui.locateCenterOnScreen('images/ui/ok.png', confidence = default_confidence)
    except: return

    if ok != None:
        mouseMoveClick(ok, 'ok')

    try: ok2 = pyautogui.locateCenterOnScreen('images/ui/ok2.png', confidence = default_confidence)
    except: return

    if ok2 != None:
        mouseMoveClick(ok2, 'ok2')

    try: close = pyautogui.locateCenterOnScreen('images/ui/close.png', confidence = default_confidence)
    except: return

    if close != None:
        mouseMoveClick(close, 'close')

    try: cancel = pyautogui.locateCenterOnScreen('images/ui/cancel.png', confidence = default_confidence)
    except: return

    if cancel != None:
        mouseMoveClick(cancel, 'cancel')

    try: continue_ = pyautogui.locateCenterOnScreen('images/ui/continue.png', confidence = default_confidence)
    except: return

    if continue_ != None:
        mouseMoveClick(continue_, 'continue')
