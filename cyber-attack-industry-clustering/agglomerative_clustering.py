import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import gower
from matplotlib.ticker import FuncFormatter
from sklearn.cluster import AgglomerativeClustering

matplotlib.use("TkAgg")
mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH2")

df = pd.read_csv(file_path)

# 나중에 산업을 붙여줘야 돼서 따로 저장
target_industries = df["Target Industry"]

# 산업, 피해 규모 제외하고 gower's distance 계산
columns = df.drop(columns=["Target Industry", "Damage Scale"])

# gower's distance 계산 기반 거리 행렬 생성
gower_dist = gower.gower_matrix(columns)

# 실루엣 계수 결과 클러스터 개수 5가 제일 적합
n_clusters=5

# agglomerative clustering 수행
cluster_model = AgglomerativeClustering(
    n_clusters=n_clusters,
    # gower's distance 거리 행렬 그대로 전달
    metric='precomputed',
    # 평균 거리 방식으로
    linkage='average'
)

cluster_labels = cluster_model.fit_predict(gower_dist)
df["Cluster"] = cluster_labels

categorical_cols = ["Attack Type", "Security Vulnerability Type", "Defense Mechanism Used"]

# 클러스터별 산업군 비율
cluster_industry_counts = df.groupby(["Cluster", "Target Industry"]).size().unstack(fill_value=0)
cluster_industry_pct = cluster_industry_counts.div(cluster_industry_counts.sum(axis=1), axis=0)

cluster_industry_pct.plot(
    kind="bar",
    stacked=True,
    figsize=(14, 6),
    colormap="Set2"
)
plt.title("클러스터별 산업군 비율", fontsize=24, pad=20)
plt.xlabel("클러스터", fontsize=18)
plt.ylabel("비율 (%)", fontsize=18)
plt.gca().xaxis.labelpad = 10
plt.gca().yaxis.labelpad = 10
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y * 100)}%'))
plt.legend(title="산업군", bbox_to_anchor=(1.05, 1), fontsize=16, loc='upper left')
plt.grid(axis="y", linestyle="--", alpha=0.5)

for bar_index, (idx, row) in enumerate(cluster_industry_pct.iterrows()):
    cumulative = 0
    for col_index, value in enumerate(row):
        plt.text(
            bar_index, cumulative + value / 2,
            f"{value * 100:.1f}%",
            ha='center', va='center', fontsize=14
        )
        cumulative += value
plt.xticks(rotation=0, fontsize=16)
plt.yticks(fontsize=16)

plt.tight_layout()
plt.show()

cluster_industry_pct.to_csv("cluster_industry_ratio.csv", index=False)


# 클러스터별 공격 유형, 보안 취약점, 방어 전략 각각 비율 비교
categories = ["Attack Type", "Security Vulnerability Type", "Defense Mechanism Used"]
clusters = sorted(df["Cluster"].unique())

for cluster_id in clusters:
    cluster_df = df[df["Cluster"] == cluster_id]

    fig, axs = plt.subplots(1, len(categories), figsize=(20, 7), sharey=True)
    fig.suptitle(f"클러스터 {cluster_id} - 공격 특성 비율", fontsize=30)

    for i, col in enumerate(categories):
        ax = axs[i]
        labels = sorted(df[col].dropna().unique())
        ratios = []

        for label in labels:
            ratio = (cluster_df[col] == label).mean() * 100
            ratios.append(ratio)

        ax.plot(labels, ratios, marker='o', linestyle='-', linewidth=2)

        for x, y in zip(labels, ratios):
            ax.text(x, y + 2, f"{y:.1f}%", ha='center', va='bottom', fontsize=14)

        ax.set_title(col, fontsize=18)
        ax.set_ylabel("비율 (%)", fontsize=22)
        ax.set_ylim(0, 115)
        ax.tick_params(axis='x', labelsize=18, rotation=30)
        ax.tick_params(axis='y', labelsize=18)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.show()


# 클러스터별 주요 공격 특성 & 비율
cluster_feature_ratios = {}
cluster_feature_labels = {}

for cluster_id in clusters:
    cluster_df = df[df["Cluster"] == cluster_id]
    ratios = []
    labels = []
    for col in categories:
        top_value = cluster_df[col].mode().iloc[0]
        ratio = (cluster_df[col] == top_value).mean() * 100
        labels.append(top_value)
        ratios.append(ratio)
    cluster_feature_labels[cluster_id] = labels
    cluster_feature_ratios[cluster_id] = ratios

clusters = list(cluster_feature_ratios.keys())
features = ["Attack Type", "Security Vulnerability Type", "Defense Mechanism Used"]

data = np.array(list(cluster_feature_ratios.values()))
labels = list(cluster_feature_labels.values())

x = np.arange(len(clusters))
width = 0.25

plt.figure(figsize=(20, 8))
set2_colors = plt.get_cmap('Set2').colors[:3]

for i in range(3):
    bars = plt.bar(x + i * width, data[:, i], width=width, label=features[i], color=set2_colors[i])

    for j, bar in enumerate(bars):
        height = bar.get_height()
        label_text = f"{labels[j][i]}\n({height:.1f}%)"
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1.0,
            label_text,
            ha='center', va='bottom', fontsize=16
        )

xtick_positions = x + width
plt.xticks(xtick_positions, [f"{c}" for c in clusters], fontsize=22)

plt.title("클러스터별 대표 공격 특성", fontsize=36, pad=20)
plt.ylabel("비율 (%)", fontsize=22)
plt.xlabel("클러스터", fontsize=22)
plt.legend(
    title=None,
    fontsize=16,
    loc='center left',
    bbox_to_anchor=(1.02, 0.5)
)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.yticks(fontsize=22)
plt.gca().xaxis.labelpad = 10
plt.gca().yaxis.labelpad = 10
plt.ylim(0, 115)
plt.tight_layout()
plt.show()


# 표준편차
clusters = sorted(df["Cluster"].unique())

# 클러스터별 산업군 비율 가져오기
cluster_data = {}
for cluster_id in clusters:
    if cluster_id in cluster_industry_pct.index:
        values = cluster_industry_pct.loc[cluster_id].fillna(0).values
        cluster_data[cluster_id] = values
    else:
        # 클러스터가 industry_pct에 없으면 0으로 채움
        cluster_data[cluster_id] = np.zeros(cluster_industry_pct.shape[1])

std_devs = [np.std(cluster_data[c]) for c in clusters]

plt.figure(figsize=(12, 8))
plt.plot(clusters, std_devs, marker='o', linestyle='-', linewidth=2)

for x, y in zip(clusters, std_devs):
    plt.text(x, y + 0.1, f'{y:.2f}', ha='center', va='bottom', fontsize=24)

plt.title("클러스터별 산업군 분포 비율의 표준편차", fontsize=30, pad=20)
plt.xlabel("클러스터", fontsize=26)
plt.ylabel("표준편차", fontsize=26)
plt.gca().xaxis.labelpad = 20
plt.gca().yaxis.labelpad = 20
plt.xticks(clusters, fontsize=24)
plt.yticks(fontsize=24)
plt.grid(True)
max_std = max(std_devs)
plt.ylim(0, max_std + 0.05)
plt.tight_layout()
plt.show()
