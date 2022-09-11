import functions
from imports import *
 
if __name__ == "__main__":
    while not keyboard.is_pressed("delete"):
        functions.champion_select()
        functions.play_game()
        functions.bot_tdm() 
        functions.spawn_champion()
        functions.anti_afk()
        functions.end_game()
        functions.misc()
    
    functions.log("bot stopped")