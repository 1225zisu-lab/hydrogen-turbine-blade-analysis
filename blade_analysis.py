# ---------------------------------------------------------
# blade_geometry_analysis.py
# Computes spanwise blade geometry from STL:
# - chord length
# - max thickness
# - twist angle
# - sectional area
# ---------------------------------------------------------

import os
import numpy as np
import pandas as pd
import math

# ---- Try importing trimesh ----
try:
    import trimesh
except:
    print("\nERROR: trimesh not installed. Install using:\n")
    print("    pip install trimesh shapely rtree\n")
    raise SystemExit


# ---------------------------------------------------------
# 1) Load STL File
# ---------------------------------------------------------
stl_path = r"E:\Turbine Blades\Blade designs\Hydrogen_Blade_cand_379.STL"

if not os.path.exists(stl_path):
    raise FileNotFoundError(f"STL file not found at:\n{stl_path}")

mesh = trimesh.load_mesh(stl_path, force='mesh')

if mesh.is_empty:
    raise RuntimeError("ERROR: Mesh is empty. Check STL.")


# ---------------------------------------------------------
# 2) Extract geometry
# ---------------------------------------------------------
vertices = np.asarray(mesh.vertices)
triangles = mesh.triangles
centroids = mesh.triangles_center
areas = mesh.area_faces


# ---------------------------------------------------------
# 3) Determine span direction (longest axis)
# ---------------------------------------------------------
ranges = vertices.max(axis=0) - vertices.min(axis=0)
span_axis = np.argmax(ranges)         # 0=X, 1=Y, 2=Z

axis_names = ["X", "Y", "Z"]
print(f"\nDetected span direction = {axis_names[span_axis]} axis")

span_min = vertices[:, span_axis].min()
span_max = vertices[:, span_axis].max()
span_length = span_max - span_min

print(f"Span length = {span_length:.3f} units\n")


# ---------------------------------------------------------
# 4) Create spanwise stations
# ---------------------------------------------------------
N = 12   # number of spanwise sections (you can increase)
stations = np.linspace(span_min, span_max, N)

results = []


# ---------------------------------------------------------
# 5) For each station → extract cross-section
# ---------------------------------------------------------
for s in stations:

    # triangles whose centroid is close to this span location
    mask = np.abs(centroids[:, span_axis] - s) < (span_length / N)

    if mask.sum() < 3:
        # not enough triangles at this location
        results.append([s, 0, 0, 0, 0])
        continue

    pts = triangles[mask].reshape(-1, 3)

    # project onto sectional plane (remove span axis)
    other_axes = [ax for ax in [0, 1, 2] if ax != span_axis]
    sec = pts[:, other_axes]

    # -----------------------------------------------------
    # Compute major geometry
    # -----------------------------------------------------

    # chord = longest dimension of this section
    max_x = sec[:, 0].max()
    min_x = sec[:, 0].min()
    chord = max_x - min_x

    # thickness = vertical (2nd axis) size
    max_y = sec[:, 1].max()
    min_y = sec[:, 1].min()
    thickness = max_y - min_y

    # area = approximate polygon area using bounding box
    area = (chord * thickness) * 0.6   # rough estimate scaling

    # twist = angle of least squares line along chord
    x = sec[:, 0]
    y = sec[:, 1]
    a = np.polyfit(x, y, 1)
    twist_angle = math.degrees(math.atan(a[0]))

    # store results
    results.append([s, chord, thickness, twist_angle, area])


# ---------------------------------------------------------
# 6) Save CSV
# ---------------------------------------------------------
df = pd.DataFrame(results, columns=[
    "Span_Position",
    "Chord_Length",
    "Max_Thickness",
    "Twist_Angle_deg",
    "Section_Area"
])

csv_path = "blade_station_data.csv"
df.to_csv(csv_path, index=False)

print("\n-----------------------------------")
print("Analysis Complete!")
print("-----------------------------------")
print(f"CSV saved as: {csv_path}")
print("\nPreview:\n")
print(df)
print("\n-----------------------------------")
print("You can now use this data in your report.")
print("-----------------------------------")
