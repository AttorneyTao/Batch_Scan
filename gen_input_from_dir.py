"""
从指定目录生成 input.xlsx，包含所有文件的相对路径
"""

import os
import sys
import argparse
from pathlib import Path
import pandas as pd


def generate_input_xlsx(source_dir: str, output_file: str = "input.xlsx", max_files: int = None):
    """
    从源目录生成 input.xlsx
    
    Args:
        source_dir: 源目录路径
        output_file: 输出 Excel 文件名
        max_files: 最大文件数量（用于测试），None 表示所有文件
    """
    source_path = Path(source_dir).resolve()
    
    if not source_path.exists():
        print(f"错误: 目录不存在: {source_dir}")
        sys.exit(1)
    
    if not source_path.is_dir():
        print(f"错误: 不是目录: {source_dir}")
        sys.exit(1)
    
    print(f"扫描目录: {source_path}")
    
    # 发现所有文件（使用 glob 以提高效率）
    files = []
    count = 0
    try:
        for file_path in source_path.rglob("*"):
            if file_path.is_file():
                # 获取相对路径
                rel_path = file_path.relative_to(source_path)
                files.append({
                    "path": str(rel_path),
                    "file_name": file_path.name
                })
                count += 1
                
                # 进度提示（每100个文件打印一次）
                if count % 100 == 0:
                    print(f"  已扫描 {count} 个文件...")
                
                # 检查是否达到最大文件数
                if max_files and count >= max_files:
                    files = files[:max_files]
                    print(f"达到最大文件数限制: {max_files}")
                    break
    except KeyboardInterrupt:
        print(f"\n已中断，已扫描 {len(files)} 个文件")
    
    # 创建 DataFrame
    df = pd.DataFrame(files)
    
    print(f"发现文件数: {len(df)}")
    if len(df) > 0:
        print("\n前 5 个文件:")
        print(df.head())
    
    # 保存到 Excel
    df.to_excel(output_file, index=False)
    print(f"\n已保存到: {output_file}")
    
    return output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从指定目录生成 input.xlsx")
    parser.add_argument("source_dir", type=str, help="源目录路径")
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="input.xlsx",
        help="输出Excel文件名 (default: input.xlsx)"
    )
    parser.add_argument(
        "-m", "--max",
        type=int,
        default=None,
        help="最大文件数量 (用于测试，default: None，表示全部)"
    )
    
    args = parser.parse_args()
    generate_input_xlsx(args.source_dir, args.output, args.max)
