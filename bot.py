import functions
from imports import *

start_time = time.time()
secondsToRun = 2100

debug = False

if __name__ == "__main__":
    functions.watermark()
    
    _this = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(_this , win32con.SW_FORCEMINIMIZE)

    if not functions.gameRunning():
        subprocess.run("start steam://run/444090", shell=True)
        time.sleep(5)
    
    champion_select = threading.Thread(target = functions.champion_select)
    play_game = threading.Thread(target = functions.play_game)
    bot_tdm = threading.Thread(target = functions.bot_tdm)
    spawn_champion = threading.Thread(target = functions.spawn_champion)
    anti_afk = threading.Thread(target = functions.anti_afk)
    end_game = threading.Thread(target = functions.end_game)
    misc = threading.Thread(target = functions.misc)

    threads = [ champion_select, play_game, bot_tdm, spawn_champion, anti_afk, end_game, misc ]

    for function in threads:
        function.start()
        print(f"{function}")

    while not keyboard.is_pressed("delete"):
        time.sleep(1)
        time_difference = time.time() - start_time

        if debug:
            print( f"count \t {time_difference}" )

    print(f"bot stopped, killing {threads.count()} threads")
    for function in threads:
        function.join()
        print(f"{function}")

     