import os
import csv
from datetime import datetime

# Path to the folder with screenshots (adjust if needed)
image_folder = os.path.join(os.getcwd(), "screenshot_dataset", "images")
metadata_file = os.path.join(os.getcwd(), "screenshot_dataset", "metadata.csv")

# Get all PNG files
images = sorted([f for f in os.listdir(image_folder) if f.endswith(".png")])

# Write metadata
with open(metadata_file, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["frame", "filename", "generated_time"])

    for frame_number, filename in enumerate(images, start=1):
        timestamp = datetime.now().isoformat()
        writer.writerow([frame_number, filename, timestamp])

print(f"✅ Metadata written to: {metadata_file}")
