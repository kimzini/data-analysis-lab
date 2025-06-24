# 공격 유형, 공격 원천, 산업, 보안 취약점, 방어 메커니즘 중복 제거 고유 값 추출

import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH")

output_file = "attack_values.csv"
output_path = os.path.join(os.path.dirname(file_path), output_file)

columns_to_extract = [
    "Attack Type",
    "Target Industry",
    "Security Vulnerability Type",
    "Defense Mechanism Used"
]

df = pd.read_csv(file_path)

# 중복 제거 -> 고유 값 추출
attack_values = {
    col: sorted(df[col].dropna().unique().tolist())
    for col in columns_to_extract
}

# 제일 많은 고유 값을 가진 컬럼 행 개수에 맞게 다른 컬럼도 빈칸으로 채움
max_len = max(len(vals) for vals in attack_values.values())
for col in attack_values:
    attack_values[col] += [''] * (max_len - len(attack_values[col]))

result_df = pd.DataFrame(attack_values)

result_df.to_csv(output_path, index=False)