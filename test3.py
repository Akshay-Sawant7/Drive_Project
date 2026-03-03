import pyautogui
import time
import os
import subprocess

# ----------------------------
# CONFIGURATION
# ----------------------------
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
 
CONFIDENCE = 0.85
TIMEOUT = 70
CHECK_INTERVAL = 1
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

 
# ----------------------------
# UTIL FUNCTIONS
# ----------------------------
def get_image_path(image_name):
    return os.path.join(BASE_DIR, image_name)
 
 
def wait_and_click(image_name, timeout=TIMEOUT):
    """
    Wait until image appears and click it.
    """
    print(f"Waiting for {image_name}...")
 
    start_time = time.time()
    image_path = get_image_path(image_name)
 
    while time.time() - start_time < timeout:
        try:
            # Try without grayscale first (more reliable for some installers)
            location = pyautogui.locateCenterOnScreen(
                image_path,
                confidence=CONFIDENCE,
                grayscale=False
            )
        except Exception:
            location = None

        if not location:
            try:
                # Fallback to a grayscale search
                location = pyautogui.locateCenterOnScreen(
                    image_path,
                    confidence=max(0.5, CONFIDENCE - 0.1),
                    grayscale=True
                )
            except Exception:
                location = None

        if location:
            print(f"Found {image_name} at {location}, clicking...")
            pyautogui.click(location)
            return True
 
        time.sleep(CHECK_INTERVAL)
 
    # On timeout, save a screenshot to help debugging
    dump_path = os.path.join(BASE_DIR, f"screenshot_timeout_{int(time.time())}_{image_name}")
    try:
        dump_file = dump_path + ".png"
        pyautogui.screenshot(dump_file)
        print(f"Saved screenshot for debugging: {dump_file}")
    except Exception:
        print("Failed to save screenshot")

    raise FileNotFoundError(f"{image_name} not found within {timeout} seconds. Screenshot: {dump_file}")
 
 
def wait_and_type(image_name, text):
    wait_and_click(image_name)
    pyautogui.write(text, interval=0.05)
 
 
# ----------------------------
# INSTALLATION FLOW
# ----------------------------
def launch_installer(installer_path):
    print("Launching installer...")
    subprocess.Popen(installer_path)
    time.sleep(10)
 
 
def install_nuxeo():
    wait_and_click("OK.png")
    wait_and_click("I_accept_the_agreement.png")
    wait_and_click("Next.png")
    time.sleep(2)  # Short wait before next click
    wait_and_click("Next.png")

    # Install button can take time to appear — allow a long timeout here
    wait_and_click("Install.png", timeout=TIMEOUT)

    print("Installing... please wait (this may take several minutes)")
    time.sleep(15)

    # After clicking Install, wait until Finish appears (very long timeout for large installs)
    try:
        wait_and_click("Finish.png", timeout=80)
    except FileNotFoundError as e:
        print("Finish button not detected within expected time. Check saved screenshot for debugging.")
        raise
    time.sleep(10)         
    pyautogui.press("enter") # For Apply
    time.sleep(10)

    pyautogui.press("enter") # For Release Notes
    time.sleep(15)
 
 
def add_account(nuxeo_url):
    wait_and_click("Add_Account.png")
    time.sleep(2)
    wait_and_type("URL_field.png", nuxeo_url)
    wait_and_click("Connect.png")
 
 
def login(username, password):
    wait_and_type("Username.png", username)
    pyautogui.press("tab")
    pyautogui.write(password, interval=0.05)
    pyautogui.press("enter")
 

def close_browser():
    print("Closing browser...")
    # Add logic to close the browser if needed
    time.sleep(5)
    pyautogui.hotkey('alt', 'f4')
    print("Browser closed ")
 
# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
 
    #installer_path = r"C:\Users\jrathod\Downloads\nuxeo-drive-6.0.0.exe"   # Working
    #installer_path = r"C:\Users\jrathod\Downloads\nuxeo-drive-5.5.1.exe" # Working
    #installer_path = r"C:\Users\jrathod\Downloads\nuxeo-drive-6.1.0.21.exe" # Working
    installer_path = r"C:\Users\Akshay\Downloads\nuxeo-drive.exe"
 
    print("===== NUXEO DRIVE AUTOMATION STARTED =====")
    start_time = time.time()
 
    launch_installer(installer_path)
    install_nuxeo()
    add_account("https://drive-2023.beta.nuxeocloud.com/nuxeo")
    login("test1", "test1")
    close_browser()
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
 
    print("===== AUTOMATION COMPLETED SUCCESSFULLY =====")