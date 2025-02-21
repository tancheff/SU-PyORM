import pyautogui
import time
import random


while True:
    pyautogui.hotkey('alt', 'tab')  # Simulates Alt+Tab
    time.sleep(random.randint(1, 10))
    pyautogui.hotkey('alt', 'tab')
    time.sleep(random.randint(200, 240))  # Wait for 1 minute
