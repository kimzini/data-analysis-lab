import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

matplotlib.use("TkAgg")
mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH2")

df = pd.read_csv(file_path)

bins = [round(x, 1) for x in np.arange(0, 1.1, 0.1)]
labels = [f"{bins[i]} ~ {bins[i+1]}" for i in range(len(bins)-1)]

df["Damage Scale"] = pd.cut(df["Damage Scale"], bins=bins, labels=labels, include_lowest=True, right=False)

damage_bin_counts = df["Damage Scale"].value_counts().sort_index()

print("피해 규모 범위별 빈도 수")
print(damage_bin_counts)

plt.figure(figsize=(10, 6))
sns.barplot(x=damage_bin_counts.index, y=damage_bin_counts.values, palette="Blues_d")

plt.title("Damage Scale 구간별 빈도 수", fontsize=14)
plt.xlabel("Damage Scale 구간", fontsize=12)
plt.ylabel("건수", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()