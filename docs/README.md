# License Double-Check

使用 ScanCode 工具包进行开源许可证合规性检查的自动化脚本。

## 功能特性

- ✅ 批量扫描Excel中列出的文件
- ✅ 自动提取SPDX许可证信息
- ✅ 多线程并行扫描，提高效率
- ✅ 详细的日志记录，跟踪扫描过程
- ✅ 结果保存到新的Excel文件

## 环境要求

- Python 3.13+
- ScanCode-toolkit 已安装并配置到系统PATH
- UV 包管理器

## 安装依赖

```bash
# 如果还未初始化项目
uv init

# 安装依赖
uv add pandas openpyxl
```

## 使用方法

### 基础用法

```bash
# 方法1：使用main.py
python main.py "D:\path\to\project" -i input.xlsx -o output.xlsx

# 方法2：直接使用scan_licenses.py
python scan_licenses.py "D:\path\to\project" -i input.xlsx -o output.xlsx
```

### 命令行参数

```
位置参数:
  path_prefix              相对路径的前缀（必需）

可选参数:
  -i, --input FILE         输入Excel文件路径 (默认: input.xlsx)
  -o, --output FILE        输出Excel文件路径 (默认: output.xlsx)
  -t, --threads NUM        并行扫描的线程数 (默认: 4)
  -c, --column NAME        包含文件路径的列名 (默认: path)
  -h, --help              显示帮助信息
```

### 使用示例

#### 示例1：基础扫描
```bash
python main.py "D:\OneDrive\文档\0工作资料\国浩工作资料\自有案件\开源合规专项——理想汽车\haloosspace"
```

#### 示例2：自定义输入输出文件和线程数
```bash
python scan_licenses.py "C:\project" -i files_to_scan.xlsx -o results.xlsx -t 8
```

#### 示例3：自定义路径列名
```bash
python main.py "D:\project" -c file_path -i input.xlsx -o output.xlsx
```

## 输入文件格式 (input.xlsx)

Excel文件应包含以下内容：

| Column 1 | Column 2 | path | ... |
|----------|----------|------|-----|
| data1    | data2    | relative/path/to/file1.cpp | ... |
| data3    | data4    | relative/path/to/file2.hpp | ... |

- `path` 列包含相对于提供的前缀的文件相对路径
- 支持其他任意列，会原样复制到输出文件

## 输出文件格式 (output.xlsx)

输出文件包含输入文件的所有列，加上新增的 `license_expression_spdx_scancode` 列：

| Column 1 | Column 2 | path | ... | license_expression_spdx_scancode |
|----------|----------|------|-----|----------------------------------|
| data1    | data2    | relative/path/to/file1.cpp | ... | BSL-1.0 |
| data3    | data4    | relative/path/to/file2.hpp | ... | Apache-2.0 OR MIT |

## 日志文件

扫描过程中会生成详细的日志文件，位置为：
- `scan_licenses_YYYYMMDD_HHMMSS.log`

日志包含以下信息：
- 扫描开始/完成时间
- 每个文件的扫描状态
- 错误信息和警告
- 最终统计摘要

## 输出示例

```
2026-02-10 15:30:45,123 - INFO - ============================================================
2026-02-10 15:30:45,124 - INFO - 开始license扫描任务
2026-02-10 15:30:45,125 - INFO - 输入文件: input.xlsx
2026-02-10 15:30:45,126 - INFO - 输出文件: output.xlsx
2026-02-10 15:30:45,127 - INFO - 路径前缀: D:\project\path
2026-02-10 15:30:45,128 - INFO - 并行线程数: 4
2026-02-10 15:30:45,129 - INFO - ============================================================
2026-02-10 15:30:45,130 - INFO - 读取输入文件: input.xlsx
2026-02-10 15:30:45,200 - INFO - 准备扫描 100 个文件
2026-02-10 15:30:50,300 - INFO - 开始扫描文件: D:\project\path\file1.cpp
...
2026-02-10 15:45:20,500 - INFO - ✓ 扫描完成！
2026-02-10 15:45:20,501 - INFO - ============================================================
2026-02-10 15:45:20,502 - INFO - 总扫描文件数: 100
2026-02-10 15:45:20,503 - INFO - 检测到license的文件数: 95
2026-02-10 15:45:20,504 - INFO - 未检测到license的文件数: 5
2026-02-10 15:45:20,505 - INFO - ============================================================
```

## 常见问题

### Q: ScanCode命令找不到？
A: 请确保ScanCode-toolkit已正确安装并配置到系统PATH中。运行 `scancode.bat --version` 测试。

### Q: 扫描速度太慢？
A: 可以增加 `-t` 参数中的线程数，例如 `-t 16`。但要注意系统资源限制。

### Q: 某些文件扫描失败如何处理？
A: 查看生成的日志文件了解具体错误信息。常见原因包括：
- 文件路径错误
- 文件不存在
- 文件权限不足
- scancode超时（可增加超时时间或检查文件大小）

### Q: 如何只扫描特定类型的文件？
A: 在输入Excel中只包含那些文件的行。

## 技术实现

- **并行处理**: 使用 `ThreadPoolExecutor` 实现多线程并行扫描
- **临时文件**: 每个扫描任务使用独立的临时JSON文件
- **错误处理**: 完整的异常捕获和日志记录
- **资源清理**: 自动清理临时文件

## 许可证

本项目用于开源合规性检查。
