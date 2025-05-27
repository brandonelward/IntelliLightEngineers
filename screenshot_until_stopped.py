import pyautogui
import time
import os

# Save folder
output_dir = os.path.join(os.getcwd(), "continuous_dataset")
os.makedirs(output_dir, exist_ok=True)

print("🟢 Taking screenshots... press Ctrl+C to stop.\n")

count = 1
try:
    while True:
        filename = os.path.join(output_dir, f"frame_{count:04}.png")
        pyautogui.screenshot().save(filename)
        print(f"[{count}] Saved {filename}")
        count += 1
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Screenshot capture stopped by user.")
