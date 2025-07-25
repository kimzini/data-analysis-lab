# 각 클러스터별 산업군 분포 비율 표준편차

import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl

matplotlib.use("TkAgg")
mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH3")

df = pd.read_csv(file_path)

std_devs = df.std(axis=1)

plt.figure(figsize=(12, 8))
plt.plot(std_devs.index, std_devs.values, marker='o', linestyle='-', linewidth=2)

for x, y in zip(std_devs.index, std_devs.values):
    plt.text(x, y + 0.001, f'{y:.3f}', ha='center', va='bottom', fontsize=18)

plt.title("클러스터별 산업군 분포 비율의 표준편차", fontsize=26, pad=20)
plt.xlabel("클러스터", fontsize=22)
plt.ylabel("표준편차", fontsize=22)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()