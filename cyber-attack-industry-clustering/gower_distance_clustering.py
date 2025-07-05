import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import gower
from matplotlib.ticker import FuncFormatter
from sklearn.cluster import AgglomerativeClustering
from utils.silhouette_gower import silhouette_gower

matplotlib.use("TkAgg")
mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH2")

df = pd.read_csv(file_path)

target_industries = df["Target Industry"]

columns = df.drop(columns=["Target Industry"])
gower_dist = gower.gower_matrix(columns)

range_n = range(2, 9)
silhouette_scores = []

for n in range_n:
    score = silhouette_gower(gower_dist, n)
    silhouette_scores.append(score)

plt.figure(figsize=(10, 6))
plt.plot(range_n, silhouette_scores, marker='o')
plt.xticks(range_n)
plt.xlabel("클러스터 개수")
plt.ylabel("실루엣 계수")
plt.title("Gower's distance 기반 실루엣 계수")
plt.grid(True)
plt.tight_layout()
plt.show()

n_clusters=7

cluster_model = AgglomerativeClustering(
    n_clusters=n_clusters,
    metric='precomputed',
    linkage='average'
)
cluster_labels = cluster_model.fit_predict(gower_dist)

df["Cluster"] = cluster_labels
df["Target Industry"] = target_industries

df.to_csv("agglomerative_clustered_data.csv", index=False)

categorical_cols = ["Attack Type", "Security Vulnerability Type", "Defense Mechanism Used"]

for cluster_id in sorted(df["Cluster"].unique()):
    cluster_df = df[df["Cluster"] == cluster_id]
    print(f"\n[클러스터 {cluster_id}]")

    for col in categorical_cols:
        top_value = cluster_df[col].mode().iloc[0]
        count = cluster_df[col].value_counts().iloc[0]
        total = len(cluster_df)
        ratio = count / total
        print(f" - {col}: {top_value} (비율: {ratio:.1%})")

    mean_damage = cluster_df["Damage Scale"].mean()
    print(f" - Damage Scale: {mean_damage:.4f}")

cluster_industry_counts = df.groupby(["Cluster", "Target Industry"]).size().unstack(fill_value=0)
cluster_industry_pct = cluster_industry_counts.div(cluster_industry_counts.sum(axis=1), axis=0)

cluster_industry_pct.plot(
    kind="bar",
    stacked=True,
    figsize=(14, 6),
    colormap="Set2"
)

plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y * 100)}%'))

plt.title("클러스터별 산업군 비율")
plt.xlabel("클러스터")
plt.ylabel("비율 (%)")
plt.legend(title="산업군", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis="y", linestyle="--", alpha=0.5)
for bar_index, (idx, row) in enumerate(cluster_industry_pct.iterrows()):
    cumulative = 0
    for col_index, value in enumerate(row):
        if value > 0.03:
            plt.text(
                bar_index, cumulative + value / 2,
                f"{value * 100:.1f}%",
                ha='center', va='center', fontsize=9
            )
        cumulative += value
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()