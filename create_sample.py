"""
创建示例input.xlsx文件的脚本
"""

import pandas as pd


def create_sample_input():
    """创建示例input.xlsx文件"""
    # 示例数据
    data = {
        "path": [
            "vbs/vbspro/thirdparty/boost/include/boost/config/abi/msvc_prefix.hpp",
            "vbs/vbspro/thirdparty/boost/include/boost/config/abi/msvc_suffix.hpp",
            "src/main.cpp",
            "src/utils/helper.h",
            "include/config.hpp",
        ],
        "file_name": [
            "msvc_prefix.hpp",
            "msvc_suffix.hpp",
            "main.cpp",
            "helper.h",
            "config.hpp",
        ],
        "description": [
            "Boost MSVC prefix configuration",
            "Boost MSVC suffix configuration",
            "Main source file",
            "Helper utilities",
            "Configuration header",
        ],
    }

    df = pd.DataFrame(data)
    df.to_excel("input.xlsx", index=False)
    print("✓ 示例文件 input.xlsx 已创建")
    print(f"  包含 {len(df)} 个文件条目")
    print("\n内容预览:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    create_sample_input()
