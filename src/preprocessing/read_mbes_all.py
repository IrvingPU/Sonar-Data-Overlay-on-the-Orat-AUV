import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# --- Setup path to import pyall ---
current_dir = os.path.dirname(__file__)
pyall_path = os.path.abspath(os.path.join(current_dir, '..', 'utils', 'pyall'))
sys.path.append(pyall_path)

from pyall import allreader

# --- Path to the .all file ---
all_file_path = os.path.abspath(os.path.join(
    current_dir, '..', '..', 'data', 'raw', 'aurora_dataset_sample', 'JC125',
    'M86', 'multibeam_echosounder', 'raw', 'M0860005.all'))

reader = allreader(all_file_path)

if not reader.fileptr:
    print("Could not open the .all file.")
    sys.exit()

print("Reading datagrams...")

x_points, y_points, z_points = [], [], []

while reader.moredata():
    try:
        typeofdatagram, datagram = reader.readdatagram()
        if typeofdatagram in ['X', 'D']:
            datagram.read()
            depths = getattr(datagram, 'depth', None)
            across = getattr(datagram, 'acrosstrackdistance', None)
            along = getattr(datagram, 'alongtrackdistance', None)

            if depths is not None and across is not None and along is not None:
                x_points.extend(across)
                y_points.extend(along)
                z_points.extend(depths)
    except Exception as e:
        print(f"Skipping datagram: {e}")
        continue

print(f"Extracted points: {len(z_points)}")

x = np.array(x_points)
y = np.array(y_points)
z = np.array(z_points)

valid = (z > 0) & (z < 10000)
x, y, z = x[valid], y[valid], z[valid]
print(f"Filtered points: {len(z)}")

# --- Plot ---
plt.figure(figsize=(10, 6))
sc = plt.scatter(x, y, c=z, cmap='viridis', s=1)
plt.colorbar(sc, label='Depth (m)')
plt.title("MBES Bathymetric Point Cloud")
plt.xlabel("Across-Track (m)")
plt.ylabel("Along-Track (m)")
plt.tight_layout()
plt.grid(True)
plt.show()

# --- Save outputs ---
output_csv = os.path.abspath(os.path.join(current_dir, '..', '..', 'notebooks', 'mbes_points.csv'))
output_npz = os.path.abspath(os.path.join(current_dir, '..', '..', 'notebooks', 'mbes_points.npz'))

df = pd.DataFrame({'x': x, 'y': y, 'seafloor_depth': z})
df.to_csv(output_csv, index=False)
np.savez(output_npz, x=x, y=y, z=z)
print(f"Saved point cloud CSV: {output_csv}")
print(f"Saved point cloud NPZ: {output_npz}")

# --- Load aligned dataset for integration ---
aligned_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'data', 'processed', 'aligned_sss_mbes_dataset.csv'))
aligned_df = pd.read_csv(aligned_path)

lon_col = [col for col in aligned_df.columns if col.lower() in ['lon', 'longitude']][0]
lat_col = [col for col in aligned_df.columns if col.lower() in ['lat', 'latitude']][0]
query_points = aligned_df[[lon_col, lat_col]].values

mbes_tree = KDTree(np.column_stack((x, y)))
distances, indices = mbes_tree.query(query_points)

aligned_df['seafloor_depth'] = z[indices]
print(f"Aligned dataset columns: {list(aligned_df.columns)}")

# --- Export enriched data ---
final_output = os.path.abspath(os.path.join(current_dir, '..', '..', 'data', 'processed', 'aligned_sss_mbes_with_depth.csv'))
aligned_df.to_csv(final_output, index=False)
print(f"Saved enriched dataset: {final_output}")

