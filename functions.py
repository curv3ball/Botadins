from imports import *

version = "2.9.3"
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

def currentTime():
    return time.strftime("%I:%M %p")

def log(msg):
    global logCount
    logCount += 1
    if logCount > 15:
        watermark()
        logCount = 0

    t = time.strftime("%I:%M %p")
    x = open("logs.txt", "a")
    x.write("[" + currentTime() + "] " + msg + "\n")
    print(f"[{t}] {msg}")

def gameRunning():
    call = 'TASKLIST', '/FI', 'imagename eq %s' % 'Paladins.exe'
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith('Paladins.exe'.lower())

def hideConsole():
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW = 6
    hWnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hWnd, SW)

def mouseMove(x, y):
    for n in range(10):
        try:
            w = int(pyautogui.position()[0] + (x - pyautogui.position()[0]) / 10 * n)
            h = int(pyautogui.position()[1] + (y - pyautogui.position()[1]) / 10 * n)
            win32api.SetCursorPos((w, h))
        except: continue
        time.sleep(0.05/10)

def mouseMoveClick(vector, name = ""):
    mouseMove(vector[0], vector[1]) #<-- this is to make it smooth, its just a visual effect the cursor isnt foreground idk how to fix that i searched online too
    #win32api.SetCursorPos(vector)
    try:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.20)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    except: log(f"failed to click mouse at {vector}")
    time.sleep(1)

def champion_select():
    while not keyboard.is_pressed("delete"):
        champion_frame = None
        lock_in = None

        try: champion_frame = pyautogui.locateCenterOnScreen('images/champions/' + champion.lower() + '/champion_select.png', region=(regions.champion_select), confidence = default_confidence)
        except: return

        if champion_frame != None:
            log( f"caller: {champion_select.__name__} | selecting champion | location: {champion_frame[0], champion_frame[1]}" )
            mouseMoveClick(champion_frame, 'champion_frame')

        try: lock_in = pyautogui.locateCenterOnScreen('images/ui/lock_in.png', region=(regions.lock_in), confidence = default_confidence)
        except: return

        if lock_in != None:
            log( f"caller: {champion_select.__name__} | locking champion | location: {champion_frame[0], champion_frame[1]}" )
            mouseMoveClick(lock_in, 'lock_in')

def play_game():
    while not keyboard.is_pressed("delete"):
        play_button = None
        champions_button = None  
        try: play_button = pyautogui.locateCenterOnScreen('images/ui/play_button.png', region=(regions.main_menu), confidence = default_confidence)
        except: return

        try: champions_button = pyautogui.locateCenterOnScreen('images/ui/champions_button.png', region=(regions.main_menu), confidence = default_confidence)
        except: return

        if play_button != None and champions_button != None:
            
            if webhook.find('https://discord.com/api/webhooks/') != -1:
                global response
                log( f"caller: {play_game.__name__} | " f"found: {'images/ui/champions_button.png'} | " f"location: {champions_button[0], champions_button[1]}" )
                mouseMoveClick(champions_button, 'champions_button')

                scroll = None
                try: scroll = pyautogui.locateCenterOnScreen('images/ui/double_arrow.png', region=(regions.double_arrow), confidence = default_confidence)
                except: return

                if scroll != None:
                    log( f"caller: {play_game.__name__} | " f"found: {'images/ui/double_arrow.png'} | " f"location: {scroll[0], scroll[1]}" )
                    mouseMoveClick(scroll, 'scroll')

                    mastery_filter = None
                    try: mastery_filter = pyautogui.locateCenterOnScreen('images/ui/mastery_filter.png', region=(regions.mastery_filter), confidence = default_confidence)
                    except: return

                    if mastery_filter != None:
                        log( f"caller: {play_game.__name__} | " f"found: {'images/ui/mastery_filter.png'} | " f"location: {mastery_filter[0], mastery_filter[1]}" )
                        mouseMoveClick(mastery_filter, 'mastery_filter')

                        role_filter = None
                        try: role_filter = pyautogui.locateCenterOnScreen('images/ui/role_filter.png', region=(regions.role_filter), confidence = default_confidence)
                        except: return

                        if role_filter != None:
                            log( f"caller: {play_game.__name__} | " f"found: {'images/ui/role_filter.png'} | " f"location: {role_filter[0], role_filter[1]}" )
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
                                log( f"caller: {play_game.__name__} | deleting old webhook" )
                                wh.delete(response)

                            log( f"caller: {play_game.__name__} | updating webhook" )
                            response = wh.execute()

                close = None
                try: close = pyautogui.locateCenterOnScreen('images/ui/menu_x.png', region=(regions.menu_x), confidence = default_confidence)
                except: return

                if close != None:
                    log( f"caller: {play_game.__name__} | " f"found: {'images/ui/menu_x.png'} | " f"location: {close[0], close[1]}" )
                    mouseMoveClick(close, 'close')
                    time.sleep(2)
                    log( f"caller: {play_game.__name__} | " f"found: {'images/ui/play_button.png'} | " f"location: {play_button[0], play_button[1]}" )
                    mouseMoveClick(play_button, 'play_button')
            else:
                log( f"caller: {play_game.__name__} | " f"found: {'images/ui/play_button.png'} | " f"location: {play_button[0], play_button[1]}" )
                mouseMoveClick(play_button, 'play_button')
                    
def bot_tdm():
    while not keyboard.is_pressed("delete"):
        gamemode_top = None
        gamemode_bottom = None
        gamemode_top_pic = 'images/ui/training_gamemode.png'
        try: gamemode_top = pyautogui.locateCenterOnScreen(gamemode_top_pic, region=(regions.gamemode_select_top), confidence = default_confidence)
        except: return

        if gamemode_top != None:
            log( f"caller: {bot_tdm.__name__} | " f"found: {gamemode_top_pic} | " f"location: {gamemode_top[0], gamemode_top[1]}" )
            mouseMoveClick(gamemode_top, 'gamemode_top')
            
        try: gamemode_bottom = pyautogui.locateCenterOnScreen('images/ui/tdm_training.png', region=(regions.gamemode_select_bottom), confidence = default_confidence)
        except: return

        if gamemode_bottom != None:
            log( f"caller: {bot_tdm.__name__} | " f"found: {gamemode_bottom} | " f"location: {gamemode_bottom[0], gamemode_bottom[1]}" )
            mouseMoveClick(gamemode_bottom, 'gamemode_bottom')
     
def spawn_champion():
    while not keyboard.is_pressed("delete"):
        # fix for octavia, she has a special screen
        if champion.lower() == "octavia":
            passive = None
            try: passive = pyautogui.locateCenterOnScreen('images/champions/' + champion.lower() + '/team_passive.png', region=(regions.octavia_passive), confidence = 0.7)
            except: return
            if passive != None:
                log( f"caller: {spawn_champion.__name__} | found octavia passive | location: {passive[0], passive[1]}" )
                mouseMoveClick(passive, 'passive')

        talent = None
        loadout = None
        equip = None

        try: talent = pyautogui.locateCenterOnScreen('images/champions/' + champion.lower() + '/talent.png', region=(regions.talent_select), confidence = default_confidence)
        except: return

        if talent != None:
            log( f"caller: {spawn_champion.__name__} | " f"found: {'talent.png'} | " f"location: {talent[0], talent[1]}" )
            mouseMoveClick(talent, 'talent')

        try: loadout = pyautogui.locateCenterOnScreen('images/champions/' + champion.lower() + '/card_deck.png', region=(regions.loadout_select), confidence = default_confidence)
        except: return

        if loadout != None:
            log( f"caller: {spawn_champion.__name__} | " f"found: {'card_deck.png'} | " f"location: {loadout[0], loadout[1]}" )
            mouseMoveClick(loadout, 'loadout')

        try: equip = pyautogui.locateCenterOnScreen('images/ui/equip.png', region=(regions.loadout_equip), confidence = default_confidence)
        except: return

        if equip != None:
            log( f"caller: {spawn_champion.__name__} | " f"found: {'equip.png'} | " f"location: {equip[0], equip[1]}" )
            mouseMoveClick(equip, 'equip')

def anti_afk():
    while not keyboard.is_pressed("delete"):
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
    while not keyboard.is_pressed("delete"):
        summary = None
        try: summary = pyautogui.locateCenterOnScreen('images/ui/match_summary.png', region=(regions.endgame_top), confidence = default_confidence)
        except: return

        if summary != None:
            close = None

            try: close = pyautogui.locateCenterOnScreen('images/ui/menu_x.png', region=(regions.menu_x), confidence = default_confidence)
            except: return

            if close != None:
                log( f"caller: {end_game.__name__} | " f"found: {'images/ui/menu_x.png'} | " f"location: {close[0], close[1]}" )
                mouseMoveClick(close, 'close')

def misc():
    while not keyboard.is_pressed("delete"):
        purchase = None
        ok = None
        ok2 = None
        close = None
        cancel = None
        continue_ = None

        try: purchase = pyautogui.locateCenterOnScreen('images/ui/purchase.png', confidence = default_confidence)
        except: return

        if purchase != None:
            log( f"caller: {misc.__name__} | " f"found: {'images/ui/purchase.png'} | " f"location: {purchase[0], purchase[1]}" )
            mouseMoveClick(purchase, 'purchase')

        try: ok = pyautogui.locateCenterOnScreen('images/ui/ok.png', confidence = default_confidence)
        except: return

        if ok != None:
            log( f"caller: {misc.__name__} | " f"found: {'images/ui/ok.png'} | " f"location: {ok[0], ok[1]}" )
            mouseMoveClick(ok, 'ok')

        try: ok2 = pyautogui.locateCenterOnScreen('images/ui/ok2.png', confidence = default_confidence)
        except: return

        if ok2 != None:
            log( f"caller: {misc.__name__} | " f"found: {'images/ui/ok2.png'} | " f"location: {ok2[0], ok2[1]}" )
            mouseMoveClick(ok2, 'ok2')

        try: close = pyautogui.locateCenterOnScreen('images/ui/close.png', confidence = default_confidence)
        except: return

        if close != None:
            log( f"caller: {misc.__name__} | " f"found: {'images/ui/close.png'} | " f"location: {close[0], close[1]}" )
            mouseMoveClick(close, 'close')

        try: cancel = pyautogui.locateCenterOnScreen('images/ui/cancel.png', confidence = default_confidence)
        except: return

        if cancel != None:
            log( f"caller: {misc.__name__} | " f"found: {'images/ui/cancel.png'} | " f"location: {cancel[0], cancel[1]}" )
            mouseMoveClick(cancel, 'cancel')

        try: continue_ = pyautogui.locateCenterOnScreen('images/ui/continue.png', confidence = default_confidence)
        except: return

        if continue_ != None:
            log( f"caller: {misc.__name__} | " f"found: {'images/ui/continue_.png'} | " f"location: {continue_[0], continue_[1]}" )
            mouseMoveClick(continue_, 'continue')