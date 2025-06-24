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

# minmax 정규화
df_subset["Loss_scaling"] = ((df_subset["Loss"] - df_subset["Loss"].min()) / (df_subset["Loss"].max() - df_subset["Loss"].min())).round(3)
df_subset["Users_scaling"] = ((df_subset["Users"] - df_subset["Users"].min()) / (df_subset["Users"].max() - df_subset["Users"].min())).round(3)

# 피해 점수 컬럼 추가
df["Damage Score"] = ((df_subset["Loss_scaling"] * 0.5 + df_subset["Users_scaling"] * 0.5) / df_subset["Time"]).round(3)

df.drop(columns=[
    "Financial Loss (in Million $)",
    "Number of Affected Users",
    "Incident Resolution Time (in Hours)"
], inplace=True)

output_path = os.path.join(os.path.dirname(file_path), "main_data_with_damage_scores.csv")
df.to_csv(output_path, index=False)