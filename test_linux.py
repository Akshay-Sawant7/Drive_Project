import pyautogui
import time
import subprocess
import sys
import os

# ================= CONFIG =================
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

CONFIDENCE = 0.7
DEFAULT_TIMEOUT = 30  # Reduced timeout for CI
CHECK_INTERVAL = 1


# ================= UTILS =================
def log(msg):
    print(f"[INFO] {msg}")


def is_github_actions():
    return os.getenv('GITHUB_ACTIONS') == 'true'


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
        except Exception as e:
            log(f"Error: {str(e)[:50]}")
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
        # Don't fail in GitHub Actions, just log
        if is_github_actions():
            log(f"⚠️ Image not found in CI: {image} (skipping)")
            return False
        else:
            raise Exception(f"❌ Image not found: {image}")

    pyautogui.click(location)
    log(f"Clicked → {image}")
    time.sleep(2)
    return True


# ================= INSTALLER STEPS =================
INSTALLATION_STEPS = [
    ("Ok.png", "Language OK"),
    ("I_accept_the_agreement.png", "Accept Agreement"),
    ("Next.png", "Next"),
    ("Next.png", "Next Again"),
    ("Install.png", "Install"),
    ("Finish.png", "Finish"),
]


# ================= MAIN FLOW =================
def run_steps(steps):
    all_success = True
    for image, label in steps:
        log(f"Step: {label}")
        if not click_image(image):
            all_success = False
    return all_success


def main():
    log("=" * 50)
    log("NUXEO DRIVE AUTOMATION")
    log("=" * 50)

    # Log environment
    log(f"Screen size: {pyautogui.size()}")
    log(f"In GitHub Actions: {is_github_actions()}")

    # Check PNG files exist
    log("\nChecking PNG files...")
    all_images_exist = True
    for image, label in INSTALLATION_STEPS:
        if os.path.exists(image):
            log(f"✅ Found: {image}")
        else:
            log(f"❌ Missing: {image}")
            all_images_exist = False

    if not all_images_exist:
        log("❌ Some images are missing!")
        sys.exit(1)

    # Skip actual installer in GitHub Actions
    if is_github_actions():
        log("\n⚠️ Running in GitHub Actions - verification only")
        log("✅ All images verified successfully!")
        return

    # Real execution (local Windows only)
    log("\nLaunching Nuxeo Drive installer...")
    installer_path = r"C:\Users\Akshay\Downloads\nuxeo-drive.exe"

    if not os.path.exists(installer_path):
        log(f"❌ Installer not found: {installer_path}")
        sys.exit(1)

    subprocess.Popen([installer_path])
    time.sleep(5)

    try:
        if run_steps(INSTALLATION_STEPS):
            log("🎉 Installation completed successfully")
        else:
            log("❌ Some steps failed")
            sys.exit(1)
    except Exception as e:
        log(f"❌ Error: {str(e)}")
        sys.exit(1)


# ================= ENTRY =================
if __name__ == "__main__":
    main()