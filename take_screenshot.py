import pyautogui
import time

# Wait a few seconds so you can switch to the SUMO window
print("Get ready! Taking a screenshot in 5 seconds...")
time.sleep(5)

# Take a screenshot of your current screen
screenshot = pyautogui.screenshot()

# Save the image
screenshot.save("sumo_screenshot.png")
print("Screenshot saved as sumo_screenshot.png ✅")
