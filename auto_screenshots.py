import pyautogui
import time
import os

# Number of screenshots to take
num_screenshots = 100

# Time between screenshots (in seconds)
delay = 5

# Folder where screenshots will be saved (current folder)
save_folder = os.getcwd()

print(f"Starting screenshot capture... Total: {num_screenshots}, Delay: {delay} seconds")

for i in range(1, num_screenshots + 1):
    filename = os.path.join(save_folder, f"screenshot_{i:03}.png")
    print(f"Taking screenshot {i}...")

    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

    print(f"Saved: {filename}")
    time.sleep(delay)

print("✅ All screenshots taken successfully!")
