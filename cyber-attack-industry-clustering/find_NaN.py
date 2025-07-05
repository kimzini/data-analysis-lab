# 결측치 확인
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

file_path = os.getenv("CSV_FILE_PATH")

df = pd.read_csv(file_path)

# NaN이 하나라도 있는 행은 nan_rows에 저장
nan_rows = df[df.isnull().any(axis=1)]

if not nan_rows.empty:
    print(nan_rows)
else:
    print("No NaN")