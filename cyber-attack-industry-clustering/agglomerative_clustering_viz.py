# 각 산업군 클러스터별 비율 변화

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
df = df * 100

for industry in df.columns:
    plt.figure(figsize=(16, 8))
    plt.plot(df.index, df[industry], marker='o')
    plt.title(f"{industry} 산업군 클러스터별 비율 변화", fontsize=36, pad=20)
    plt.xlabel("클러스터", fontsize=26)
    plt.ylabel("비율 (%)", fontsize=26)
    plt.xticks(df.index, fontsize=24)
    plt.yticks(fontsize=24)
    plt.gca().xaxis.labelpad = 10
    plt.gca().yaxis.labelpad = 10
    min_y = df[industry].min() - 1
    max_y = df[industry].max() + 1
    plt.ylim(min_y, max_y)
    plt.grid(True, linestyle='--', alpha=0.6)

    for i, value in enumerate(df[industry]):
        plt.text(df.index[i], value + 0.5, f"{value:.1f}%", ha='center', va='bottom', fontsize=26)

    plt.tight_layout()
    plt.show()