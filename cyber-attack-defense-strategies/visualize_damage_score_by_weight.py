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

file_path = os.getenv("CSV_FILE_PATH")

df = pd.read_csv(file_path)

df = df[[
    "Financial Loss (in Million $)",
    "Number of Affected Users",
    "Incident Resolution Time (in Hours)"
]]

df.columns = ["Loss", "Users", "Time"]

df["Loss_scaling"] = ((df["Loss"] - df["Loss"].min()) / (df["Loss"].max() - df["Loss"].min())).round(3)
df["Users_scaling"] = ((df["Users"] - df["Users"].min()) / (df["Users"].max() - df["Users"].min())).round(3)

# 각 컬럼별 가중치 다르게 넣어서 비교
df["Damage1"] = ((df["Loss_scaling"] * 0.7 + df["Users_scaling"] * 0.3) / df["Time"]).round(4)  # 재정적 피해 0.7
df["Damage2"] = ((df["Loss_scaling"] * 0.5 + df["Users_scaling"] * 0.5) / df["Time"]).round(4)  # 각각 0.5
df["Damage3"] = ((df["Loss_scaling"] * 0.3 + df["Users_scaling"] * 0.7) / df["Time"]).round(4)  # 영향 받은 사용자 수 0.7

# 페어 플롯
sns.pairplot(df[["Damage1", "Damage2", "Damage3"]])
plt.suptitle("가중치 비율별 피해 점수 분포 비교", y=1.02)
plt.show()

# 히트맵
plt.figure(figsize=(6, 4))
sns.heatmap(
    df[["Damage1", "Damage2", "Damage3"]].corr(),
    annot=True,
    cmap="coolwarm",
    vmin=0,
    vmax=1
)
plt.title("가중치 비율별 피해 점수 유사도 분석")
plt.tight_layout()
plt.show()