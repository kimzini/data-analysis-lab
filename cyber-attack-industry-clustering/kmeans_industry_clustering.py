import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
# from utils.silhouetteViz import silhouetteViz

matplotlib.use("TkAgg")
mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH2")

df = pd.read_csv(file_path)

# 산업별 빈도 수가 가장 높은 공격 유형
top_attack = (
    df.groupby(["Target Industry", "Attack Type"])
    .size()
    .reset_index(name="Cnt")
    .sort_values(["Target Industry", "Cnt"], ascending=[True, False])
    .drop_duplicates("Target Industry")
    .set_index("Target Industry")
)
top_attack_onehot = pd.get_dummies(top_attack["Attack Type"], prefix="TopAttack")

# 산업별 빈도 수가 가장 높은 보안 취약점
top_vuln = (
    df.groupby(["Target Industry", "Security Vulnerability Type"])
    .size()
    .reset_index(name="Cnt")
    .sort_values(["Target Industry", "Cnt"], ascending=[True, False])
    .drop_duplicates("Target Industry")
    .set_index("Target Industry")
)
top_vuln_onehot = pd.get_dummies(top_vuln["Security Vulnerability Type"], prefix="TopVuln")

# 산업별 피해 규모가 가장 큰 공격 유형
top_damage = (
    df.groupby(["Target Industry", "Attack Type"])["Damage Scale"]
    .mean()
    .reset_index()
    .sort_values(["Target Industry", "Damage Scale"], ascending=[True, False])
    .drop_duplicates("Target Industry")
    .set_index("Target Industry")
)
max_damage_onehot = pd.get_dummies(top_damage["Attack Type"], prefix="MaxDamage")

combined = top_attack_onehot.join(top_vuln_onehot, how="outer")
combined = combined.join(max_damage_onehot, how="outer")
combined = combined.fillna(0)

scaler = StandardScaler()
scaled = scaler.fit_transform(combined)

wcss = []
K_range = range(1, len(combined) + 1)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(scaled)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(K_range, wcss, marker='o')
plt.title("Elbow Method")
plt.xlabel("클러스터 개수(k)")
plt.ylabel("WCSS")
plt.grid(True)
plt.tight_layout()
plt.show()

# silhouetteViz(2, scaled)
# silhouetteViz(3, scaled)
# silhouetteViz(4, scaled)
# silhouetteViz(5, scaled)

# K-means 클러스터링
n_clusters =4
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=30)
labels = kmeans.fit_predict(scaled)
combined["Cluster"] = labels

for c in range(n_clusters):
    print(f"\n클러스터 {c}")

    industries_in_cluster = combined[combined["Cluster"] == c].index.tolist()
    print(f"산업: {', '.join(industries_in_cluster)}")

    cluster_data = combined[combined["Cluster"] == c].drop(columns="Cluster")
    mean_features = cluster_data.mean().sort_values(ascending=False)
    print(mean_features.head(3).to_string())


# 개별 공격 사례에 클러스터 추가 -> 방어 메커니즘 피해 규모 시각화
df_clustered = df.merge(combined["Cluster"], left_on="Target Industry", right_index=True)

g = sns.catplot(
    data=df_clustered,
    x="Defense Mechanism Used", y="Damage Scale",
    col="Cluster",
    kind="box",
    col_wrap=4,
    height=6,
    aspect=1,
    sharey=True
)
g.fig.subplots_adjust(top=0.85)
g.fig.suptitle("클러스터별 방어 메커니즘 피해 규모", fontsize=14)
for ax in g.axes.flatten():
    ax.tick_params(axis='x', labelrotation=30)
plt.show()