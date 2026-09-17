import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. 加载数据 (Load Data)
# ---------------------------------------------------------------------------
HERE = Path(__file__).parent
DATA_PATH = HERE / "data" / "enso_data.csv"
OUT_DIR = HERE / "out"
OUT_DIR.mkdir(exist_ok=True)

# 如果本地存在 CSV 则读取，不存在则直接载入内存数据
if DATA_PATH.exists():
    df = pd.read_csv(DATA_PATH)
else:
    import io
    data_str = """Year,ENSO_Phase,ONI_Index,Precipitation_Anomaly_mm,Precipitation_Anomaly_pct
1998,El Nino,2.1,230,18.5
1999,La Nina,-1.5,-120,-9.6
2000,La Nina,-1.3,-90,-7.2
2001,Neutral,-0.3,15,1.2
2002,El Nino,1.1,110,8.8
2003,Neutral,0.2,-20,-1.6
2004,El Nino,0.7,60,4.8
2005,Neutral,-0.1,10,0.8
2006,El Nino,0.9,85,6.8
2007,La Nina,-1.1,-80,-6.4
2008,La Nina,-0.8,-60,-4.8
2009,El Nino,1.3,140,11.2
2010,La Nina,-1.4,-110,-8.8
2011,La Nina,-1.0,-75,-6.0
2012,Neutral,-0.2,5,0.4
2013,Neutral,-0.3,-15,-1.2
2014,Neutral,0.4,30,2.4
2015,El Nino,2.5,280,22.4
2016,El Nino,2.2,210,16.8
2017,La Nina,-0.8,-65,-5.2
2018,Neutral,0.5,40,3.2
2019,El Nino,0.8,70,5.6
2020,La Nina,-1.1,-95,-7.6
2021,La Nina,-1.0,-85,-6.8
2022,La Nina,-0.9,-70,-5.6
2023,El Nino,1.8,190,15.2
2024,El Nino,1.2,130,10.4
2025,La Nina,-0.7,-50,-4.0"""
    df = pd.read_csv(io.StringIO(data_str))

# ---------------------------------------------------------------------------
# 2. 清新配色与审美参数 (Style & Fresh Colors)
# ---------------------------------------------------------------------------
BG_COLOR = "#FAFAFA"       # 极简浅灰白背景
TEXT_COLOR = "#2B2B2B"     # 深灰色优雅字号

# 莫兰迪/柔和色系配色：
COLOR_MAP = {
    "El Nino": "#E07A5F",   # 珊瑚柔红 (Warm Soft Coral)
    "La Nina": "#3D405B",   # 雾霭黛蓝 (Fresh Deep Teal/Slate)
    "Neutral": "#8D99AE"    # 鼠尾草灰 (Muted Sage Gray)
}

# 气泡大小映射：根据 ONI 指数绝对值计算气泡面积
bubble_sizes = np.abs(df["ONI_Index"]) * 350 + 80

# ---------------------------------------------------------------------------
# 3. 创建画布并绘制气泡图 (Create Plot)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# 绘制辅助线 (0 基准线)
ax.axhline(0, color="#D3D3D3", linestyle="--", linewidth=1, zorder=1)

# 按类别绘制气泡以生成优雅图例 (Plot Phase by Phase)
for phase, color in COLOR_MAP.items():
    subset = df[df["ENSO_Phase"] == phase]
    sizes = np.abs(subset["ONI_Index"]) * 350 + 80
    ax.scatter(
        subset["Year"], 
        subset["Precipitation_Anomaly_pct"], 
        s=sizes, 
        color=color, 
        alpha=0.65, 
        edgecolors="white", 
        linewidth=1.5, 
        label=phase,
        zorder=3
    )

# ---------------------------------------------------------------------------
# 4. 细节调整与标注 (Details & Typography)
# ---------------------------------------------------------------------------
# 标题与坐标轴标签
ax.set_title("Precipitation Anomaly & ENSO Intensity (1998–2025)", 
             fontsize=16, fontweight="bold", pad=20, color=TEXT_COLOR)
ax.set_xlabel("Year", fontsize=11, labelpad=10, color=TEXT_COLOR)
ax.set_ylabel("Precipitation Anomaly (%)", fontsize=11, labelpad=10, color=TEXT_COLOR)

# 设置 X 轴年份刻度
ax.set_xticks(df["Year"])
ax.set_xticklabels(df["Year"], rotation=45, fontsize=8, color=TEXT_COLOR)

# 隐藏上方和右侧的边框线 (Clean Spines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')

# 网格线
ax.grid(True, linestyle=":", alpha=0.4, color="#AAAAAA", zorder=0)

# 图例设置 (Legend)
legend = ax.legend(title="ENSO Phase", frameon=True, facecolor=BG_COLOR, edgecolor="none", loc="upper left")
legend.get_title().set_color(TEXT_COLOR)
for text in legend.get_texts():
    text.set_color(TEXT_COLOR)

# ---------------------------------------------------------------------------
# 5. 保存图表 (Save Output)
# ---------------------------------------------------------------------------
plt.tight_layout()
output_file = OUT_DIR / "enso_bubble_chart.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
print(f"Chart saved successfully to: {output_file}")
