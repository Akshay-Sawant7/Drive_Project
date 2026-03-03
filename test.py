import pyautogui
import time
import subprocess

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


def wait_for_image(
    image_path,
    timeout=60,
    confidence=0.7,
    interval=1
):
    """
    Wait until an image appears on screen.
    Returns center coordinates if found, else None.
    """
    print(f"Waiting for image: {image_path}")

    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(
                image_path,
                confidence=confidence
            )
            if location:
                print(f"Image found: {image_path}")
                return location
        except pyautogui.ImageNotFoundException:
            pass

        time.sleep(interval)

    print(f"Timeout: Image not found → {image_path}")
    return None


###################

print("Launching Nuxeo Drive installer...")
subprocess.Popen(
    r"C:\Users\Akshay\Downloads\nxidrive\nuxeo-drive-6.1.0.19.exe"
)
print("Installer launched successfully")

ok_button = wait_for_image(
    "language_ok.png",
    timeout=90,
    confidence=0.7
)
if ok_button:
    pyautogui.click(ok_button)
else:
    raise Exception("Language OK button did not appear")

agreement = wait_for_image(
    "I_accept_the_agreement.png",
    timeout=90,
    confidence=0.7
)
if agreement:
    pyautogui.click(agreement)
else:
    raise Exception("Language OK button did not appear")