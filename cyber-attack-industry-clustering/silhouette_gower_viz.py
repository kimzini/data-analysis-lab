# 실루엣 계수 시각화

import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import gower
from utils.silhouette_gower import silhouette_gower

matplotlib.use("TkAgg")
mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH2")

df = pd.read_csv(file_path)

target_industries = df["Target Industry"]

columns = df.drop(columns=["Target Industry", "Damage Scale"])
gower_dist = gower.gower_matrix(columns)

range_n = range(2, 10)
silhouette_scores = []

for n in range_n:
    score = silhouette_gower(gower_dist, n)
    silhouette_scores.append(score)

plt.figure(figsize=(14, 8))
plt.plot(range_n, silhouette_scores, marker='o')

plt.title("Gower's distance 기반 실루엣 계수", fontsize=40, pad=30)
plt.xlabel("클러스터 개수", fontsize=34)
plt.ylabel("실루엣 계수", fontsize=34)
plt.gca().xaxis.labelpad = 20
plt.gca().yaxis.labelpad = 20
plt.xticks(range_n, fontsize=28)
plt.yticks(fontsize=28)

plt.grid(True)
plt.tight_layout()
plt.show()
