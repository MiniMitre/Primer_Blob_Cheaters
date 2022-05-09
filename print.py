import pyautogui
import time
print(pyautogui.position())

def submitScore():
    pyautogui.click(1000,925)

while pyautogui.pixel(1070,930) != (50, 50, 50):
    submitScore()
    time.sleep(5)
    
