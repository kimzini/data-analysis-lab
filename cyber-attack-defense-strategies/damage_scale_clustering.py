import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter

matplotlib.use("TkAgg")
mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH2")

df = pd.read_csv(file_path)

bins = [0.0, 0.02, 0.1, 0.4, 1.0]
labels = ["0~0.02", "0.02~0.1", "0.1~0.4", "0.4~1.0"]

df["Damage Range"] = pd.cut(df["Damage Scale"], bins=bins, labels=labels, include_lowest=True, right=False)

damage_industry_counts = df.groupby(['Damage Range', 'Target Industry']).size().unstack(fill_value=0)
damage_industry_pct = damage_industry_counts.div(damage_industry_counts.sum(axis=1), axis=0)

damage_industry_pct.plot(
    kind='bar',
    stacked=True,
    figsize=(14, 6),
    colormap='Set2',
)

plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y * 100)}%'))

plt.title("피해 규모 구간별 산업군 비율")
plt.xlabel("피해 규모 범위")
plt.ylabel("비율 (%)")
plt.legend(title="산업군", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for bar_index, (idx, row) in enumerate(damage_industry_pct.iterrows()):
    cumulative = 0
    for col_index, value in enumerate(row):
        plt.text(
            bar_index, cumulative + value / 2,
            f"{value * 100:.1f}%",
            ha='center', va='center', fontsize=9
        )
        cumulative += value
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()