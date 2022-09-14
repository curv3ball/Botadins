import functions
from imports import *

startTime = time.time()
secondsToRun = 2100

if __name__ == "__main__":
    functions.watermark()
    
    if not functions.gameRunning():
        subprocess.run("start steam://run/444090", shell=True)
        time.sleep(5)

    while not keyboard.is_pressed("delete"):
        functions.champion_select()
        functions.play_game()
        functions.bot_tdm() 
        functions.spawn_champion()
        functions.anti_afk()
        functions.end_game()
        functions.misc()
        
        endTime = time.time()

        secDif = int(endTime - startTime)
        minDif = secDif / 60

        sec = int(secondsToRun)
        min = sec / 60

        if secDif >= secondsToRun:
            print(f"{int(min)} minutes have passed, restarting")
            subprocess.call("taskkill /IM Paladins.exe")
            time.sleep(5)
            print(f"opening game in 5 seconds")
            subprocess.run("start steam://run/444090", shell=True)
            functions.watermark()
            time.sleep(5)
            startTime = time.time()

    functions.log("bot stopped")