#!/usr/bin/env python
"""
快速开始脚本 - 一键执行完整的许可证扫描
"""

import os
import sys
from pathlib import Path

# 确保在项目目录中运行
project_dir = Path(__file__).parent
os.chdir(project_dir)

print("=" * 70)
print("理想汽车 haloosspace 项目 License 扫描工具")
print("=" * 70)
print()

# 步骤 1: 生成输入文件
print("[步骤 1/3] 从 haloosspace 目录生成 input.xlsx...")
print("  (如果已有 input.xlsx，将跳过此步骤)")

input_file = "input.xlsx"
if not os.path.exists(input_file):
    import subprocess
    result = subprocess.run(
        [sys.executable, "gen_input_from_dir.py", "../haloosspace", "-m", "100", "-o", input_file],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"  ✅ 已生成 {input_file}")
    else:
        print(f"  ❌ 生成失败: {result.stderr}")
        sys.exit(1)
else:
    print(f"  ✅ {input_file} 已存在，使用现有文件")

# 步骤 2: 执行扫描
print()
print("[步骤 2/3] 执行许可证扫描...")
print("  (扫描所有文件，使用 4 个并行线程)")
print()

import subprocess
result = subprocess.run(
    [sys.executable, "scan_licenses.py", "../haloosspace", "-i", input_file, "-o", "output_final.xlsx", "-t", "4", "--skip-resume"],
    capture_output=False,
    text=True
)

if result.returncode != 0:
    print("❌ 扫描失败")
    sys.exit(1)

# 步骤 3: 显示结果摘要
print()
print("[步骤 3/3] 显示结果摘要...")

import pandas as pd
df = pd.read_excel("output_final.xlsx")

print()
print("扫描结果统计:")
print(f"  总行数: {len(df)}")
print(f"  列数: {len(df.columns)}")
print(f"  检测到 License 的文件数: {df['license_expression_spdx_scancode'].notna().sum()}")
print()

# 显示前几行
print("前 5 行结果:")
print(df[['component_name', 'path', 'license_expression_spdx_scancode']].head(10).to_string())
print()

print("=" * 70)
print("✅ 扫描完成！结果已保存到 output_final.xlsx")
print("=" * 70)
