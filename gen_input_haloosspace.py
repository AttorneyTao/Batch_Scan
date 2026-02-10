"""
生成理想汽车项目的输入文件示例
"""

import pandas as pd
from pathlib import Path


def create_input_file():
    """创建包含 haloosspace 项目文件的输入 Excel"""
    
    # 理想汽车项目的相对路径示例
    # 这些是常见的源代码文件类型
    data = {
        "path": [
            "vbs/vbspro/thirdparty/boost/include/boost/config/abi/msvc_prefix.hpp",
            "vbs/vbspro/thirdparty/boost/include/boost/config/compiler/msvc.hpp",
            "vbs/vbspro/thirdparty/boost/include/boost/version.hpp",
            "vbs/vbspro/thirdparty/openssl/include/openssl/ssl.h",
            "vbs/vbspro/thirdparty/openssl/include/openssl/crypto.h",
            "vbs/vbspro/src/main.cpp",
            "vbs/vbspro/src/utils/helper.h",
            "vbs/vbspro/include/config.hpp",
            "vbs/vbspro/CMakeLists.txt",
            "vbs/vbspro/README.md",
        ],
        "file_name": [
            "msvc_prefix.hpp",
            "msvc.hpp",
            "version.hpp",
            "ssl.h",
            "crypto.h",
            "main.cpp",
            "helper.h",
            "config.hpp",
            "CMakeLists.txt",
            "README.md",
        ],
    }
    
    df = pd.DataFrame(data)
    df.to_excel("input.xlsx", index=False)
    print("✓ input.xlsx 已创建")
    print(f"  包含 {len(df)} 个文件条目")
    print("\n文件列表预览：")
    print(df.to_string(index=False))


if __name__ == "__main__":
    create_input_file()
