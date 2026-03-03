import pyautogui
import time
import subprocess
import sys

# ================= CONFIG =================
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

CONFIDENCE = 0.7
DEFAULT_TIMEOUT = 90
CHECK_INTERVAL = 1

# ================= UTILS =================
def log(msg):
    print(f"🔹 {msg}")

def wait_for_image(image, timeout=DEFAULT_TIMEOUT, confidence=CONFIDENCE):
    """
    Wait until image appears on screen.
    Returns center coordinates if found, else None.
    """
    log(f"Waiting for → {image}")
    start = time.time()

    while time.time() - start < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(
                image,
                confidence=confidence,
                grayscale=True
            )
            if location:
                log(f"Found → {image}")
                return location
        except Exception:
            pass

        time.sleep(CHECK_INTERVAL)

    log(f"Timeout → {image}")
    return None


def click_image(image, timeout=DEFAULT_TIMEOUT, confidence=CONFIDENCE):
    """
    Wait for image and click it.
    """
    location = wait_for_image(image, timeout, confidence)
    if not location:
        raise Exception(f"❌ Image not found: {image}")

    pyautogui.click(location)
    log(f"Clicked → {image}")
    time.sleep(2)


# ================= INSTALLER STEPS =================
INSTALLATION_STEPS = [
    ("Ok.png", "Language OK"),
    ("I_accept_the_agreement.png", "Accept Agreement"),
    ("Next.png", "Next"),
    ("Next.png", "Next Again"),
    ("Install.png", "Install"),
    ("Finish.png", "Install"),
]

# ================= MAIN FLOW =================
def run_steps(steps):
    for image, label in steps:
        log(f"Step: {label}")
        click_image(image)


def main():
    log("Launching Nuxeo Drive installer...")
    subprocess.Popen(
        r"C:\Users\Akshay\Downloads\nuxeo-drive.exe"
    )

    time.sleep(5)  # installer initial load

    try:
        run_steps(INSTALLATION_STEPS)
        log("🎉 Installation completed successfully")

    except Exception as e:
        log(str(e))
        sys.exit(1)


# ================= ENTRY =================
if __name__ == "__main__":
    main()