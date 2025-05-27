import pyautogui
import time
import os
import shutil

# Settings
num_screenshots = 100  # Change this as needed
delay = 1  # seconds between screenshots

# Paths
dataset_root = os.path.join(os.getcwd(), "dataset")
images_dir = os.path.join(dataset_root, "images")
zip_path = os.path.join(os.getcwd(), "screenshot_dataset")

# Make directories
os.makedirs(images_dir, exist_ok=True)

print(f"Taking {num_screenshots} screenshots every {delay} second(s)...")

# Screenshot loop
for i in range(1, num_screenshots + 1):
    filename = os.path.join(images_dir, f"frame_{i:04}.png")
    print(f"[{i}/{num_screenshots}] Saving {filename}")
    pyautogui.screenshot().save(filename)
    time.sleep(delay)

print("All screenshots taken ✅")

# Zip it up
shutil.make_archive(zip_path, 'zip', dataset_root)
print(f"Zipped to: {zip_path}.zip 🎉")
