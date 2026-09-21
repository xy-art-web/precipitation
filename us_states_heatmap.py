# /// script
# dependencies = ["pandas", "matplotlib", "numpy"]
# ///

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd

# 1. 读取数据文件
HERE = Path(__file__).parent
DOWNLOADS = Path.home() / "Downloads"

csv_candidates = [
    HERE / "walmart.csv",
    HERE / "walmart_7.csv",
    DOWNLOADS / "walmart.csv",
]

CSV_PATH = next((p for p in csv_candidates if p.exists()), None)
OUT_DIR = HERE / "out"
OUT_DIR.mkdir(exist_ok=True)

if not CSV_PATH:
    raise FileNotFoundError("未找到 walmart.csv 数据文件！")

df = pd.read_csv(CSV_PATH)

# 2. 筛选美国本土坐标
df_us = df[
    (df["lng"] > -130)
    & (df["lng"] < -65)
    & (df["lat"] > 24)
    & (df["lat"] < 50)
].copy()

# 3. 阿伯斯等面积投影 (Albers Equal-Area Projection) 矫正坐标变形
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

df_us["x"], df_us["y"] = albers_projection(
    df_us["lng"].values, df_us["lat"].values
)

# 4. 创建画布与比例控制
fig = plt.figure(figsize=(16, 10), facecolor="white")
ax = fig.add_axes([0.05, 0.08, 0.90, 0.72])

# 关键设置：使平面坐标在两个方向保持 1:1，确保六边形呈现正六边形
ax.set_aspect("equal")

# 5. 配色与 Hexbin 绘制
cmap_purple_blue = LinearSegmentedColormap.from_list(
    "PurpleToBlue",
    ["#e0f3f8", "#abd9e9", "#74add1", "#4575b4", "#5e3c99", "#4a148c"]
)

hb = ax.hexbin(
    df_us["x"],
    df_us["y"],
    gridsize=52,
    cmap=cmap_purple_blue,
    mincnt=1,
    edgecolors="#475569",  # 清晰的深灰色描边
    linewidths=0.5,
    alpha=0.92,
)

ax.axis("off")

# 6. 精美标题与排版
fig.text(
    0.06, 0.91, 
    "Walmart Store Density in the U.S.", 
    fontsize=22, fontweight="bold", color="#1a1a1a"
)
fig.text(
    0.06, 0.865, 
    f"Data Source: Local walmart.csv (Updated July 2026 | Total Stores Analyzed: {len(df_us):,})", 
    fontsize=11, color="#444444"
)
fig.text(
    0.06, 0.835, 
    "Hexagon intensity represents store concentration across the contiguous United States (Albers Projection).", 
    fontsize=10, color="#666666"
)

# 7. 右上角 Colorbar 渐变色条
cb_ax = fig.add_axes([0.62, 0.86, 0.30, 0.022])
cb = fig.colorbar(hb, cax=cb_ax, orientation="horizontal")
cb.set_label("Number of Walmart Stores", fontsize=10, color="#333333", labelpad=8)
cb.ax.tick_params(labelsize=8)

# 8. 保存输出
output_file = OUT_DIR / "walmart_albers_hex.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")
print(f"标准比例地图已生成至: {output_file}")