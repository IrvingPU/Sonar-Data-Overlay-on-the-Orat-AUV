import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Append path to access pyall.py in utils
current_dir = os.path.dirname(__file__)
utils_path = os.path.abspath(os.path.join(current_dir, '..', 'utils'))
sys.path.append(utils_path)

from pyall import allreader  # Lowercase class name from your pyall.py

# Path to the .all file
all_file_path = r"D:\IrvingPU\UIB\TFM\Sonar-Data-Overlay-on-the-Orat-AUV\data\raw\aurora_dataset_sample\JC125\M86\multibeam_echosounder\raw\M0860005.all"

# Create and initialize reader
reader = allreader(all_file_path)

# Check file
if not reader.fileptr:
    print("Could not open file.")
    sys.exit()

# Start reading (note: this does not extract beam depths yet)
print("Reading .all file...")

# This class as-is may not support beam extraction yet.
# Placeholder "records" for future parsed data
records = reader.read() if hasattr(reader, 'read') else []

print(f"File opened: {reader.fileName}")
print(f"Size: {reader.fileSize / 1024:.1f} KB")
print(f"Total records read: {len(records)}")

# Placeholder for when real depth parsing is implemented
x_points, y_points, z_points = [], [], []

# TODO: When .read() and datagram parsing is ready, loop through results like:
for i, record in enumerate(records):
    if isinstance(record, dict) and 'depths' in record:
        x_points.extend(record['x'])
        y_points.extend(record['y'])
        z_points.extend(record['depths'])

# For now, simulate some fake data for plotting
if not z_points:  # If real data not available, plot mock data
    z_points = np.random.normal(100, 10, 1000)
    x_points = np.linspace(-50, 50, 1000)
    y_points = np.linspace(-100, 100, 1000)

# Plot bathymetry scatter
plt.figure(figsize=(10, 6))
sc = plt.scatter(x_points, y_points, c=z_points, cmap='viridis', s=2)
plt.colorbar(sc, label='Depth (m)')
plt.title("MBES Point Cloud (Simulated)")
plt.xlabel("Across-Track (m)")
plt.ylabel("Along-Track (m)")
plt.grid(True)
plt.tight_layout()
plt.show()

