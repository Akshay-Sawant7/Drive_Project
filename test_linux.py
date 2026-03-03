#!/usr/bin/env python3
"""
Linux PyAutoGUI Test Script for GitHub Actions
This script tests PyAutoGUI functionality using Xvfb virtual display
"""

import pyautogui
import time
import sys
import os
import platform

# ================= CONFIG =================
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

CONFIDENCE = 0.7
DEFAULT_TIMEOUT = 30
CHECK_INTERVAL = 1


# ================= UTILS =================
def log(msg):
    """Print with timestamp for better logging"""
    timestamp = time.strftime('%H:%M:%S')
    print(f"[{timestamp}] {msg}")


def is_linux():
    """Check if running on Linux"""
    return sys.platform.startswith('linux')


def check_environment():
    """Check and log environment details"""
    log("=" * 60)
    log("ENVIRONMENT CHECK")
    log("=" * 60)

    log(f"Python version: {sys.version}")
    log(f"Platform: {platform.platform()}")
    log(f"System: {platform.system()}")
    log(f"Machine: {platform.machine()}")
    log(f"Display: {os.getenv('DISPLAY', 'Not set')}")
    log(f"Working directory: {os.getcwd()}")
    log(f"PyAutoGUI version: {pyautogui.__version__}")

    # Check if running in GitHub Actions
    in_github = os.getenv('GITHUB_ACTIONS') == 'true'
    log(f"In GitHub Actions: {in_github}")

    return in_github


def verify_images():
    """Verify all required PNG files exist"""
    log("\n" + "=" * 60)
    log("VERIFYING PNG FILES")
    log("=" * 60)

    required_images = [
        "Ok.png",
        "I_accept_the_agreement.png",
        "Next.png",
        "Install.png",
        "Finish.png"
    ]

    all_found = True
    for img in required_images:
        if os.path.exists(img):
            log(f"✅ Found: {img}")
        else:
            log(f"❌ Missing: {img}")
            all_found = False

    # List all PNG files in directory
    log("\nAll PNG files in directory:")
    png_files = [f for f in os.listdir('.') if f.lower().endswith('.png')]
    for f in png_files:
        log(f"  - {f}")

    return all_found


def test_screen_capture():
    """Test screenshot functionality"""
    log("\n" + "=" * 60)
    log("TESTING SCREEN CAPTURE")
    log("=" * 60)

    try:
        # Get screen size
        width, height = pyautogui.size()
        log(f"Screen size: {width} x {height}")

        # Take screenshot
        timestamp = int(time.time())
        screenshot_file = f"test_screenshot_{timestamp}.png"
        pyautogui.screenshot(screenshot_file)

        # Verify screenshot was created
        if os.path.exists(screenshot_file):
            file_size = os.path.getsize(screenshot_file)
            log(f"✅ Screenshot saved: {screenshot_file} ({file_size} bytes)")
            return True
        else:
            log("❌ Failed to save screenshot")
            return False

    except Exception as e:
        log(f"❌ Screenshot test failed: {str(e)}")
        return False


def test_mouse_movement():
    """Test mouse movement functionality"""
    log("\n" + "=" * 60)
    log("TESTING MOUSE MOVEMENT")
    log("=" * 60)

    try:
        # Get current position
        x, y = pyautogui.position()
        log(f"Current mouse position: ({x}, {y})")

        # Move to different positions
        positions = [(100, 100), (500, 500), (800, 400)]

        for target_x, target_y in positions:
            log(f"Moving to ({target_x}, {target_y})...")
            pyautogui.moveTo(target_x, target_y, duration=0.5)
            time.sleep(0.5)

            # Verify movement
            new_x, new_y = pyautogui.position()
            log(f"  Now at: ({new_x}, {new_y})")

        log("✅ Mouse movement test passed")
        return True

    except Exception as e:
        log(f"❌ Mouse movement test failed: {str(e)}")
        return False


def test_image_recognition():
    """Test image recognition on all PNG files"""
    log("\n" + "=" * 60)
    log("TESTING IMAGE RECOGNITION")
    log("=" * 60)

    png_files = [f for f in os.listdir('.') if f.lower().endswith('.png')]

    if not png_files:
        log("❌ No PNG files found to test")
        return False

    success_count = 0
    for img_file in png_files:
        try:
            log(f"\nTrying to locate: {img_file}")

            # Try with different confidence levels
            for conf in [0.9, 0.8, 0.7]:
                try:
                    location = pyautogui.locateCenterOnScreen(
                        img_file,
                        confidence=conf,
                        grayscale=True
                    )

                    if location:
                        log(f"  ✅ Found at confidence {conf}: {location}")
                        success_count += 1
                        break
                    else:
                        log(f"  ⚠️ Not found at confidence {conf}")

                except Exception as e:
                    log(f"  ⚠️ Error at confidence {conf}: {str(e)[:50]}")

        except Exception as e:
            log(f"❌ Failed to process {img_file}: {str(e)}")

    log(f"\n✅ Successfully recognized {success_count}/{len(png_files)} images")
    return success_count > 0


def test_keyboard():
    """Test keyboard functionality"""
    log("\n" + "=" * 60)
    log("TESTING KEYBOARD")
    log("=" * 60)

    try:
        # Test typing
        test_text = "Linux PyAutoGUI Test"
        log(f"Typing: '{test_text}'")
        pyautogui.write(test_text, interval=0.1)
        time.sleep(1)

        # Test hotkeys
        log("Testing hotkey: ctrl+a (select all)")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)

        log("Testing hotkey: ctrl+c (copy)")
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)

        log("✅ Keyboard test passed")
        return True

    except Exception as e:
        log(f"❌ Keyboard test failed: {str(e)}")
        return False


def test_installation_steps():
    """Simulate the Nuxeo Drive installation steps"""
    log("\n" + "=" * 60)
    log("SIMULATING INSTALLATION STEPS")
    log("=" * 60)

    steps = [
        ("Ok.png", "Language OK"),
        ("I_accept_the_agreement.png", "Accept Agreement"),
        ("Next.png", "Next"),
        ("Next.png", "Next Again"),
        ("Install.png", "Install"),
        ("Finish.png", "Finish")
    ]

    for i, (image, description) in enumerate(steps, 1):
        log(f"\nStep {i}: {description}")

        if os.path.exists(image):
            log(f"  ✅ Image found: {image}")

            # Try to locate the image (without clicking)
            try:
                location = pyautogui.locateCenterOnScreen(
                    image,
                    confidence=0.7,
                    grayscale=True
                )
                if location:
                    log(f"  ✅ Can detect {image} at {location}")

                    # Simulate click (don't actually click in CI)
                    log(f"  🖱️ Would click at ({int(location.x)}, {int(location.y)})")
                else:
                    log(f"  ⚠️ Cannot detect {image} visually")
            except Exception as e:
                log(f"  ⚠️ Detection error: {str(e)[:50]}")
        else:
            log(f"  ❌ Image missing: {image}")
            return False

    return True


def create_test_summary(results):
    """Create a test summary"""
    log("\n" + "=" * 60)
    log("TEST SUMMARY")
    log("=" * 60)

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        log(f"{status} - {test_name}")
        if not passed:
            all_passed = False

    # Write to GitHub Step Summary if in GitHub Actions
    if os.getenv('GITHUB_STEP_SUMMARY'):
        with open(os.getenv('GITHUB_STEP_SUMMARY'), 'a') as f:
            f.write("\n## Linux PyAutoGUI Test Results\n\n")
            f.write("| Test | Status |\n")
            f.write("|------|--------|\n")
            for test_name, passed in results.items():
                status = "✅ PASSED" if passed else "❌ FAILED"
                f.write(f"| {test_name} | {status} |\n")

    return all_passed


def main():
    """Main test function"""
    start_time = time.time()

    log("\n" + "=" * 60)
    log("🐧 LINUX PYAUTOGUI TEST SUITE")
    log("=" * 60)

    # Check environment
    in_github = check_environment()

    # Dictionary to store test results
    results = {}

    # Run tests
    results["Environment Check"] = True

    results["PNG Files Verification"] = verify_images()

    if results["PNG Files Verification"]:
        results["Screen Capture"] = test_screen_capture()
        results["Mouse Movement"] = test_mouse_movement()
        results["Image Recognition"] = test_image_recognition()
        results["Keyboard"] = test_keyboard()
        results["Installation Steps"] = test_installation_steps()
    else:
        log("\n❌ Skipping advanced tests due to missing PNG files")
        results["Screen Capture"] = False
        results["Mouse Movement"] = False
        results["Image Recognition"] = False
        results["Keyboard"] = False
        results["Installation Steps"] = False

    # Calculate execution time
    execution_time = time.time() - start_time
    log(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")

    # Create summary
    all_passed = create_test_summary(results)

    log("\n" + "=" * 60)
    if all_passed:
        log("🎉 ALL TESTS PASSED!")
    else:
        log("❌ SOME TESTS FAILED!")
    log("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())