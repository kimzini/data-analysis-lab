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

# 산업별 공격 유형 빈도 수
attack_cnt_by_industry = (
    df.groupby(["Target Industry", "Attack Type"])
    .agg(Cnt=("Attack Type", "size"), Damage_Score_Mean=("Damage Scale", "mean"))
    .round(4)
    .reset_index()
    .sort_values(by=["Target Industry", "Cnt"], ascending=[True, False])
)

# 산업별 보안 취약점 언급 수
vuln_cnt_by_industry = (
    df.groupby(["Target Industry", "Security Vulnerability Type"])
    .agg(Cnt=("Security Vulnerability Type", "size"), Damage_Score_Mean=("Damage Scale", "mean"))
    .round(4)
    .reset_index()
    .sort_values(by=["Target Industry", "Cnt"], ascending=[True, False])
)

# 산업별 공격 유형별 평균 피해 규모
damage_by_industry_attack = (
    df.groupby(["Target Industry", "Attack Type"])["Damage Scale"]
    .mean()
    .reset_index()
    .round(4)
)

base_dir = os.path.dirname(file_path)

attack_cnt_by_industry.to_csv(os.path.join(base_dir, "industry_attack_type_cnt.csv"), index=False)
vuln_cnt_by_industry.to_csv(os.path.join(base_dir, "industry_vulnerability_cnt.csv"), index=False)
damage_by_industry_attack.to_csv(os.path.join(base_dir, "industry_attack_type_damage.csv"), index=False)

# 산업별 공격 유형 빈도 수
plt.figure(figsize=(16, 8))
sns.barplot(data=attack_cnt_by_industry, x="Target Industry", y="Cnt", hue="Attack Type")
plt.title("산업별 공격 유형 빈도 수", fontsize=28)
plt.xlabel("Target Industry", fontsize=22)
plt.ylabel("Cnt", fontsize=22)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(title="Attack Type", title_fontsize=18, fontsize=16, bbox_to_anchor=(1, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 산업별 보안 취약점 언급 수
plt.figure(figsize=(16, 8))
sns.barplot(data=vuln_cnt_by_industry, x="Target Industry", y="Cnt", hue="Security Vulnerability Type")
plt.title("산업별 보안 취약점 언급 수", fontsize=28)
plt.xlabel("Target Industry", fontsize=22)
plt.ylabel("Cnt", fontsize=22)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(title="Security Vulnerability Type", title_fontsize=18, fontsize=16, bbox_to_anchor=(1, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 산업별 공격 유형별 평균 피해 규모 비교
plt.figure(figsize=(16, 8))
sns.barplot(data=damage_by_industry_attack, x="Target Industry", y="Damage Scale", hue="Attack Type")
plt.title("산업별 공격 유형 평균 피해 점수 비교", fontsize=28)
plt.xlabel("Target Industry", fontsize=22)
plt.ylabel("Cnt", fontsize=22)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(title="Attack Type", title_fontsize=18, fontsize=16, bbox_to_anchor=(1, 1), loc='upper left')
plt.tight_layout()
plt.show()


# 산업별 보안 취약점 언급 수 중에서 가장 많은 항목만 추출
top_vuln_by_industry = (
    vuln_cnt_by_industry.sort_values(by=["Target Industry", "Cnt"], ascending=[True, False])
    .groupby("Target Industry")
    .first()
    .reset_index()[["Target Industry", "Security Vulnerability Type", "Cnt"]]
)

top_vuln_by_industry.to_csv(os.path.join(base_dir, "vulnerability_max_cnt.csv"), index=False)

# 산업별 공격 유형 빈도 수 중에서 가장 많은 항목만 추출
top_attack_by_industry = (
    attack_cnt_by_industry.sort_values(by=["Target Industry", "Cnt"], ascending=[True, False])
    .groupby("Target Industry")
    .first()
    .reset_index()[["Target Industry", "Attack Type", "Cnt"]]
)

top_attack_by_industry.to_csv(os.path.join(base_dir, "attack_type_max_cnt.csv"), index=False)