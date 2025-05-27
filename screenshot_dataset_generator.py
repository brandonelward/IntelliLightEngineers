import pyautogui
import time
import os

# Number of screenshots to take
num_screenshots = 100  # change as needed
delay = 1  # seconds between shots

# Create dataset directory
dataset_dir = os.path.join(os.getcwd(), "dataset", "images")
os.makedirs(dataset_dir, exist_ok=True)

print(f"Saving screenshots to: {dataset_dir}")
print(f"Capturing {num_screenshots} screenshots, one every {delay} second(s)")

for i in range(1, num_screenshots + 1):
    filename = os.path.join(dataset_dir, f"frame_{i:04}.png")
    print(f"[{i}/{num_screenshots}] Capturing {filename}")
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    time.sleep(delay)

print("🎉 Dataset generation complete!")
