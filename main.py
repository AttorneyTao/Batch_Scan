"""License double-check main entry point."""

import subprocess
import sys


def main():
    """Main entry point - runs the scan_licenses script."""
    if len(sys.argv) < 2:
        print("用法: python main.py <path_prefix> [options]")
        print("\n参数说明:")
        print("  path_prefix: 必需，文件的相对路径前缀")
        print("\n可选参数:")
        print("  -i/--input FILE: 输入Excel文件 (默认: input.xlsx)")
        print("  -o/--output FILE: 输出Excel文件 (默认: output.xlsx)")
        print("  -t/--threads NUM: 并行线程数 (默认: 4)")
        print("  -c/--column NAME: 路径列名 (默认: path)")
        print("\n示例:")
        print('  python main.py "D:\\project\\path" -i input.xlsx -o output.xlsx -t 8')
        sys.exit(1)

    # 调用scan_licenses脚本
    result = subprocess.run(
        [sys.executable, "scan_licenses.py"] + sys.argv[1:],
        cwd=".",
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
