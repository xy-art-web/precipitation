# /// script
# dependencies = ["pandas", "matplotlib", "numpy", "shapely"]
# ///

from pathlib import Path
import json
import urllib.request

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from shapely.geometry import shape

# 1. Load Data
HERE = Path(__file__).parent
DOWNLOADS = Path.home() / "Downloads"

csv_candidates = [
    HERE / "walmart.csv",
    HERE / "walmart_2.csv",
    HERE / "walmart_7.csv",
    DOWNLOADS / "walmart.csv",
]

CSV_PATH = next((p for p in csv_candidates if p.exists()), None)
OUT_DIR = HERE / "out"
OUT_DIR.mkdir(exist_ok=True)

if not CSV_PATH:
    raise FileNotFoundError("CSV data file not found!")

df = pd.read_csv(CSV_PATH)

# 2. Filter coordinates for contiguous United States
df_us = df[
    (df["lng"] > -125) & (df["lng"] < -66) & (df["lat"] > 24) & (df["lat"] < 50)
].copy()

# 3. Albers Equal Area Projection Function
def albers_projection(lon, lat, lon_0=-96, lat_1=29.5, lat_2=45.5, lat_0=37.5):
    phi = np.radians(lat)
    lam = np.radians(lon)
    phi1 = np.radians(lat_1)
    phi2 = np.radians(lat_2)
    phi0 = np.radians(lat_0)
    lam0 = np.radians(lon_0)

    n = 0.5 * (np.sin(phi1) + np.sin(phi2))
    C = np.cos(phi1) ** 2 + 2 * n * np.sin(phi1)
    rho0 = (6371) * np.sqrt(C - 2 * n * np.sin(phi0)) / n

    theta = n * (lam - lam0)
    rho = (6371) * np.sqrt(C - 2 * n * np.sin(phi)) / n

    x = rho * np.sin(theta)
    y = rho0 - rho * np.cos(theta)
    return x, y

df_us["x"], df_us["y"] = albers_projection(df_us["lng"].values, df_us["lat"].values)

# 4. Fetch US States GeoJSON Data
url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    geojson_data = json.loads(resp.read().decode())

# 5. Initialize Canvas
fig = plt.figure(figsize=(16, 10), facecolor="white")
ax = fig.add_axes([0.06, 0.08, 0.90, 0.78])
ax.set_aspect("equal")

excluded_states = ["AK", "HI", "PR", "VI", "GU", "US.AK", "US.HI", "US.PR"]

# Draw contiguous US state boundaries
for feat in geojson_data["features"]:
    state_id = feat["id"]
    state_code = state_id.replace("US.", "")
    if state_code in excluded_states or state_id in excluded_states:
        continue
    
    geom = shape(feat["geometry"])
    geoms = [geom] if geom.geom_type == 'Polygon' else geom.geoms
    for poly in geoms:
        lons, lats = poly.exterior.xy
        px, py = albers_projection(np.array(lons), np.array(lats))
        ax.plot(px, py, color="#8fa3b8", linewidth=0.7, zorder=1)

ax.set_xlim(-2600, 2600)
ax.set_ylim(-1650, 1850)

# 6. Hexagonal Binning Aggregation
cmap_purple_blue = LinearSegmentedColormap.from_list(
    "PurpleToBlue",
    ["#e0f3f8", "#abd9e9", "#74add1", "#4575b4", "#5e3c99", "#4a148c"]
)

hb = ax.hexbin(
    df_us["x"],
    df_us["y"],
    gridsize=58,
    cmap=cmap_purple_blue,
    mincnt=1,
    edgecolors="#5a738e",
    linewidths=0.4,
    alpha=0.92,
    zorder=2
)

# 7. Geographic Graticules and Coordinate Labels
lons_grid = np.arange(-120, -60, 10)
lats_grid = np.arange(25, 55, 5)

for lon_val in lons_grid:
    lats_line = np.linspace(20, 52, 100)
    lons_line = np.full_like(lats_line, lon_val)
    gx, gy = albers_projection(lons_line, lats_line)
    ax.plot(gx, gy, color="#bdc3c7", linestyle="--", linewidth=0.6, alpha=0.7, zorder=3)
    # Longitude label at the bottom
    tx, ty = albers_projection(lon_val, 23.5)
    ax.text(tx, ty, f"{abs(lon_val)}°W", fontsize=8, color="#555555", ha="center", va="top")

for lat_val in lats_grid:
    lons_line = np.linspace(-126, -65, 100)
    lats_line = np.full_like(lons_line, lat_val)
    gx, gy = albers_projection(lons_line, lats_line)
    ax.plot(gx, gy, color="#bdc3c7", linestyle="--", linewidth=0.6, alpha=0.7, zorder=3)
    # Latitude label on the left
    tx, ty = albers_projection(-125.5, lat_val)
    ax.text(tx, ty, f"{lat_val}°N", fontsize=8, color="#555555", ha="right", va="center")

# Hide default pixel axes and use geographic graticule labels instead
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_color("#cccccc")
    spine.set_linewidth(0.8)

# 8. Alaska and Hawaii Inset Outlines
for feat in geojson_data["features"]:
    state_id = feat["id"]
    state_code = state_id.replace("US.", "")
    
    if state_code in ["AK", "US.AK"]:
        geom = shape(feat["geometry"])
        geoms = [geom] if geom.geom_type == 'Polygon' else geom.geoms
        for poly in geoms:
            lons, lats = poly.exterior.xy
            px = (np.array(lons) + 160) * 35 - 2300
            py = (np.array(lats) - 60) * 35 - 1100
            ax.plot(px, py, color="#8fa3b8", linewidth=0.7, zorder=1)
            
    elif state_code in ["HI", "US.HI"]:
        geom = shape(feat["geometry"])
        geoms = [geom] if geom.geom_type == 'Polygon' else geom.geoms
        for poly in geoms:
            lons, lats = poly.exterior.xy
            px = (np.array(lons) + 157) * 55 - 1200
            py = (np.array(lats) - 20) * 55 - 1300
            ax.plot(px, py, color="#8fa3b8", linewidth=0.7, zorder=1)

# 9. Titles and Colorbar
fig.text(
    0.06, 0.93, 
    "Walmart Store Density in the U.S.", 
    fontsize=24, fontweight="bold", color="#1a1a1a"
)
fig.text(
    0.06, 0.89, 
    f"Data Source: Local walmart.csv | Total Stores Analyzed: {len(df):,}", 
    fontsize=11, color="#555555"
)

cb_ax = fig.add_axes([0.62, 0.90, 0.32, 0.02])
cb = fig.colorbar(hb, cax=cb_ax, orientation="horizontal")
cb.set_label("Number of Walmart Stores", fontsize=10, color="#333333", labelpad=6)
cb.ax.tick_params(labelsize=9)

# 10. Save Output File
output_file = OUT_DIR / "walmart_map_with_graticules.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")
print(f"Success! Map with hexagonal binning and graticules generated at: {output_file}")
