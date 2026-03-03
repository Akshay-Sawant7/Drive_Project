import pyautogui
import time
import subprocess
from typing import Tuple

print("Launching Nuxeo Drive installer...")
subprocess.Popen(r"C:\Users\Akshay\Downloads\nxidrive\nuxeo-drive-6.1.0.19.exe")
print("Installer launched successfully")

location = pyautogui.locateOnScreen("language_ok.png", confidence=0.8)
if location:
    pyautogui.click(location)
else:
    print("Button not found")