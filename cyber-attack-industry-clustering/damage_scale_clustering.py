import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter
from utils.tv_distance import tv_distance
import seaborn as sns

matplotlib.use("TkAgg")
mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH2")

df = pd.read_csv(file_path)

# 피해 구간별 산업군 분포 비율
bins = [0.0, 0.01, 0.02, 0.1, 0.4, 1.0]
labels = ["0~0.01", "0.01~0.02", "0.02~0.1", "0.1~0.4", "0.4~1.0"]

# bins = [0.0, 0.4, 1.0]
# labels = ["0~0.4", "0.4~1.0"]

df["Damage Range"] = pd.cut(df["Damage Scale"], bins=bins, labels=labels, include_lowest=True, right=False)

damage_industry_counts = df.groupby(['Damage Range', 'Target Industry'], observed=False).size().unstack(fill_value=0)
damage_industry_pct = damage_industry_counts.div(damage_industry_counts.sum(axis=1), axis=0)

damage_industry_pct.plot(
    kind='bar',
    stacked=True,
    figsize=(18, 10),
    colormap='Set2',
)

plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y * 100)}%'))

plt.title("피해 규모 구간별 산업군 분포 비율", fontsize=36, pad=20)
plt.xlabel("피해 규모 범위", fontsize=30)
plt.ylabel("비율 (%)", fontsize=30)
plt.gca().xaxis.labelpad = 10
plt.gca().yaxis.labelpad = 10
plt.legend(title="산업군", bbox_to_anchor=(1.05, 1), fontsize=22, loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar_index, (idx, row) in enumerate(damage_industry_pct.iterrows()):
    cumulative = 0
    for col_index, value in enumerate(row):
        plt.text(
            bar_index, cumulative + value / 2,
            f"{value * 100:.1f}%",
            ha='center', va='center', fontsize=22
        )
        cumulative += value
plt.xticks(rotation=0, fontsize=24)
plt.yticks(fontsize=24)

plt.tight_layout()
plt.show()

# 피해 구간끼리 tv distance -> 유사도 분석
ranges = damage_industry_pct.index.tolist()
distance_matrix = pd.DataFrame(np.zeros((len(ranges), len(ranges))), index=ranges, columns=ranges)

for i in range(len(ranges)):
    for j in range(i):
        dist = tv_distance(damage_industry_pct.iloc[i], damage_industry_pct.iloc[j])
        distance_matrix.iloc[i, j] = dist

plt.figure(figsize=(15, 10))
mask = np.triu(np.ones_like(distance_matrix, dtype=bool))
ax = sns.heatmap(
    distance_matrix,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    vmin=0,
    vmax=0.2,
    mask=mask,
    linewidths=0.5,
    cbar_kws={'label': 'TV Distance'},
    annot_kws={"size": 20},
    xticklabels=distance_matrix.columns,
    yticklabels=distance_matrix.index
)

plt.title("피해 규모 범위 간 유사도 분석 (TV Distance)", fontsize=36, pad=20)
plt.xticks(fontsize=26, rotation=0)
plt.yticks(fontsize=26, rotation=0)

cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=20)
cbar.set_label("TV Distance", size=20, labelpad=20)

plt.tight_layout()
plt.show()