import pyautogui

play_button = pyautogui.locateCenterOnScreen('images/ui/play_button.png', region=(65, 175, 500, 350), confidence = 0.8)

if play_button != None:
    print("yes")
else:
    print("no")
