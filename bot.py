from imports import *
import functions

if __name__ == '__main__':
    Play = threading.Thread(target=functions.play)
    BotTDM = threading.Thread(target=functions.startMatch)
    ChampionSelect = threading.Thread(target=functions.lockChampion)
    SpawnCharacter = threading.Thread(target=functions.spawnChampion)
    AntiAFK = threading.Thread(target=functions.antiAFK)

    Play.start()
    BotTDM.start()
    ChampionSelect.start()
    SpawnCharacter.start()
    AntiAFK.start()
 
    os.system("cls")

    print("______       _            _ _           ")
    print("| ___ \     | |          | (_)          ")
    print("| |_/ / ___ | |_ __ _  __| |_ _ __  ___ ")
    print("| ___ \/ _ \| __/ _` |/ _` | | '_ \/ __|")
    print("| |_/ / (_) | || (_| | (_| | | | | \__ " + '\\')
    print("\____/ \___/ \__\__,_|\__,_|_|_| |_|___/  v2.8.5 by curv3#0984\n\n")
                                    

    while not keyboard.is_pressed("delete"):
        Play.join()
        BotTDM.join()
        ChampionSelect.join()
        SpawnCharacter.join()
        AntiAFK.join()
        functions.closeBot()
        sys.exit(0)