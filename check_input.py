import pandas as pd
import sys

df = pd.read_excel('input.xlsx')
print("列名:")
for i, col in enumerate(df.columns):
    print(f"  {i}: {col}")

print(f"\n原始行数: {len(df)}")
print("\n前2行:")
print(df.head(2).to_string())

# 查找类似 path 的列
path_cols = [col for col in df.columns if 'path' in col.lower() or 'file' in col.lower() or 'source' in col.lower()]
print(f"\n潜在的路径列: {path_cols}")
