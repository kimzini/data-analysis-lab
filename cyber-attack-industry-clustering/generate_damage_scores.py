import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH")

df = pd.read_csv(file_path)

df_subset = df[[
    "Financial Loss (in Million $)",
    "Number of Affected Users",
    "Incident Resolution Time (in Hours)"
]].copy()

df_subset.columns = ["Loss", "Users", "Time"]

# minmax 정규화 -> 최소값 0으로 설정
df_subset["Loss_scaling"] = (df_subset["Loss"] / df_subset["Loss"].max()).round(4)
df_subset["Users_scaling"] = (df_subset["Users"] / df_subset["Users"].max()).round(4)

# 피해 수치 컬럼 추가
df["Damage Scale"] = ((df_subset["Loss_scaling"] * 0.5 + df_subset["Users_scaling"] * 0.5) / df_subset["Time"]).round(3)

df.drop(columns=[
    "Financial Loss (in Million $)",
    "Number of Affected Users",
    "Incident Resolution Time (in Hours)"
], inplace=True)

df_sorted = df.sort_values(
    by=["Target Industry", "Attack Type", "Security Vulnerability Type", "Defense Mechanism Used"]
).reset_index(drop=True)

output_path = os.path.join(os.path.dirname(file_path), "main_data_with_damage_scales.csv")
df_sorted.to_csv(output_path, index=False)