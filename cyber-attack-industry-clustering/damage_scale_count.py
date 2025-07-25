import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl

matplotlib.use("TkAgg")
mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH2")

df = pd.read_csv(file_path)

# 피해 구간별 공격 건수
bins = [0.0, 0.01, 0.02, 0.1, 0.4, 1.0]
labels = ["0~0.01", "0.01~0.02", "0.02~0.1", "0.1~0.4", "0.4~1.0"]

df["Damage Range"] = pd.cut(df["Damage Scale"], bins=bins, labels=labels, include_lowest=True, right=False)

damage_range_counts = df["Damage Range"].value_counts().sort_index()

plt.figure(figsize=(14, 10))
plt.plot(damage_range_counts.index, damage_range_counts.values, marker='o', linestyle='-')

for i, (label, count) in enumerate(damage_range_counts.items()):
    plt.text(i, count + 80, str(count), ha='center', va='bottom', fontsize=24)

plt.title("Damage Scale 구간별 건수", fontsize=45, pad=30)
plt.xlabel("피해 규모 범위", fontsize=36)
plt.ylabel("건수", fontsize=36)
plt.gca().xaxis.labelpad = 20
plt.gca().yaxis.labelpad = 20
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.ylim(0, 1200)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()