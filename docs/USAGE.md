# 使用指南

## 📋 快速开始

### 第1步：准备输入文件

创建 `input.xlsx` 文件，包含 `path` 列，每行是一个相对于某个前缀的文件路径：

```
path
vbs/vbspro/thirdparty/boost/include/boost/config/abi/msvc_prefix.hpp
vbs/vbspro/thirdparty/boost/include/boost/config/abi/msvc_suffix.hpp
...
```

**或者**，运行示例生成脚本：
```bash
python create_sample.py
```

### 第2步：运行扫描

假设你的文件相对路径前缀是 `D:\OneDrive\文档\0工作资料\国浩工作资料\自有案件\开源合规专项——理想汽车\haloosspace`

```bash
python main.py "D:\OneDrive\文档\0工作资料\国浩工作资料\自有案件\开源合规专项——理想汽车\haloosspace"
```

### 第3步：查看结果

- 输出文件：`output.xlsx` （包含新增 `license_expression_spdx_scancode` 列）
- 日志文件：`scan_licenses_20260210_xxxxxx.log` （扫描过程的详细记录）

---

## 🔧 命令参数详解

### 基础命令格式

```bash
python scan_licenses.py <path_prefix> [options]
```

### 参数说明

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `path_prefix` | **必需** - 文件路径前缀 | - | `D:\project` |
| `-i, --input` | 输入Excel文件 | `input.xlsx` | `-i source.xlsx` |
| `-o, --output` | 输出Excel文件 | `output.xlsx` | `-o results.xlsx` |
| `-t, --threads` | 并行线程数 | `4` | `-t 8` |
| `-c, --column` | 路径列名 | `path` | `-c file_path` |
| `-h, --help` | 显示帮助 | - | `-h` |

---

## 📝 使用示例

### 示例1：最简单的用法
```bash
python main.py "D:\project"
```
- 读取：`input.xlsx`
- 写入：`output.xlsx`
- 线程数：4
- 路径列：`path`

### 示例2：自定义所有参数
```bash
python scan_licenses.py "D:\my_project" \
  -i files_to_scan.xlsx \
  -o license_results.xlsx \
  -t 16 \
  -c file_path
```

### 示例3：中文路径前缀
```bash
python main.py "D:\OneDrive\文档\项目\代码审查"
```

### 示例4：快速高效的链式扫描
```bash
# 创建示例 -> 扫描 -> 查看结果
python create_sample.py && python main.py "C:\my_project" -t 8
```

---

## 📊 输入输出格式

### 输入文件格式 (input.xlsx)

```
| path | file_name | department | notes |
|------|-----------|------------|-------|
| src/main.cpp | main.cpp | core | Main entry point |
| include/config.h | config.h | core | Configuration |
| lib/util.cpp | util.cpp | library | Utilities |
```

**要求：**
- 必须有 `path` 列（或通过 `-c` 参数指定）
- 其他列任意，原样复制到output.xlsx

### 输出文件格式 (output.xlsx)

```
| path | file_name | department | notes | license_expression_spdx_scancode |
|------|-----------|------------|-------|----------------------------------|
| src/main.cpp | main.cpp | core | Main entry point | MIT |
| include/config.h | config.h | core | Configuration | Apache-2.0 |
| lib/util.cpp | util.cpp | library | Utilities | (empty) |
```

**新增列：** `license_expression_spdx_scancode`
- 包含SPDX格式的许可证表达式
- 如果未检测到许可证，该项为空

---

## 📋 SPDX许可证格式说明

输出中的 `license_expression_spdx_scancode` 可能包含：

- **单个许可证**
  - `MIT`
  - `Apache-2.0`
  - `GPL-3.0-only`
  - `BSL-1.0` (Boost Software License)

- **组合许可证**
  - `MIT OR Apache-2.0` (选择其一)
  - `Apache-2.0 AND MIT` (同时应用)
  - `(Apache-2.0 OR MIT) AND Apache-2.0`

---

## 📝 日志文件说明

每次运行都会生成日志文件：`scan_licenses_YYYYMMDD_HHMMSS.log`

### 日志包含信息

```
2026-02-10 15:30:45,123 - INFO - ============================================================
2026-02-10 15:30:45,124 - INFO - 开始license扫描任务
2026-02-10 15:30:45,125 - INFO - 输入文件: input.xlsx
2026-02-10 15:30:45,126 - INFO - 输出文件: output.xlsx
2026-02-10 15:30:45,127 - INFO - 路径前缀: D:\project
2026-02-10 15:30:45,128 - INFO - 并行线程数: 4
2026-02-10 15:30:50,300 - INFO - 开始扫描文件: D:\project\file1.cpp
2026-02-10 15:30:55,400 - INFO - 文件 D:\project\file1.cpp 扫描完成，检测到license: BSL-1.0
...
2026-02-10 15:45:20,500 - INFO - ✓ 扫描完成！
2026-02-10 15:45:20,501 - INFO - ============================================================
2026-02-10 15:45:20,502 - INFO - 总扫描文件数: 100
2026-02-10 15:45:20,503 - INFO - 检测到license的文件数: 95
2026-02-10 15:45:20,504 - INFO - 未检测到license的文件数: 5
2026-02-10 15:45:20,505 - INFO - ============================================================
```

---

## ⚙️ 性能优化

### 线程数选择建议

| 场景 | 推荐线程数 | 说明 |
|------|----------|------|
| CPU 密集型 | CPU核心数 | 例如：8核CPU用 -t 8 |
| 网络I/O型 | CPU核心数 × 2 | 例如：8核CPU用 -t 16 |
| 内存受限 | 2-4 | 避免内存溢出 |
| 默认适中 | 4 | 平衡性能和资源 |

### 估算扫描时间

- 单个小文件（<100KB）：约1-2秒
- 单个大文件（>1MB）：约3-10秒
- 100个文件 + 4线程：约5-10分钟
- 100个文件 + 16线程：约2-3分钟

---

## ❌ 常见问题排查

### Q: 命令执行提示找不到 scancode.bat
```
错误: 'scancode.bat' is not recognized as an internal or external command
```

**解决方案：**
1. 确认ScanCode-toolkit已安装
2. 运行 `scancode.bat --version` 测试
3. 如果失败，重新添加到系统PATH

### Q: 提示找不到输入文件
```
错误: 输入文件不存在: input.xlsx
```

**解决方案：**
1. 确认 `input.xlsx` 在当前目录
2. 或使用完整路径：`-i C:\path\to\input.xlsx`

### Q: Excel文件打不开
```
错误: openpyxl.utils.exceptions.InvalidFileExtension
```

**解决方案：**
1. 确保文件是 .xlsx 格式（不是 .xls）
2. 文件未损坏，可用Excel正常打开

### Q: 文件扫描超时
```
警告: 扫描超时 (5分钟)
```

**解决方案：**
1. 该文件被跳过（记录到日志）
2. 检查文件大小是否过大
3. 修改脚本中的timeout参数（当前300秒）

### Q: 内存占用过高
```
警告: Python进程占用超过 50% 内存
```

**解决方案：**
1. 减少线程数：`-t 2`
2. 分批处理大的文件列表
3. 关闭其他应用程序

---

## 🎯 工作流示例

### 流程1：完整的合规检查流程

```bash
# 1. 创建示例输入文件
python create_sample.py

# 2. 定义路径前缀（修改为你的实际路径）
PREFIX="D:\OneDrive\文档\0工作资料\国浩工作资料\自有案件\开源合规专项——理想汽车\haloosspace"

# 3. 运行扫描（8个并行线程）
python main.py "$PREFIX" -t 8

# 4. 查看日志
type scan_licenses_*.log  # Windows
# cat scan_licenses_*.log  # Linux/Mac

# 5. 打开output.xlsx检查结果
start output.xlsx  # Windows
# open output.xlsx  # Mac
```

### 流程2：多项目批量检查

```bash
# 项目1
python main.py "D:\project1" -i input1.xlsx -o output1.xlsx

# 项目2
python main.py "D:\project2" -i input2.xlsx -o output2.xlsx

# 合并所有结果
# (可使用Excel或pandas脚本)
```

---

## 📚 相关文件说明

| 文件 | 描述 |
|------|------|
| `scan_licenses.py` | 主脚本（核心功能） |
| `main.py` | 入口脚本 |
| `create_sample.py` | 生成示例输入文件 |
| `pyproject.toml` | 项目配置和依赖 |
| `README.md` | 完整文档 |
| `QUICK_START.py` | 快速开始指南 |
| `USAGE.md` | 本文件 |
| `input.xlsx` | 输入数据（用户提供） |
| `output.xlsx` | 扫描结果（脚本生成） |
| `scan_licenses_*.log` | 扫描日志（脚本生成） |

---

## 🔗 技术细节

### 脚本特点

✅ **多线程并行处理** - ThreadPoolExecutor 管理线程池  
✅ **临时文件自动清理** - 使用 TemporaryDirectory  
✅ **错误恢复** - 单个文件失败不影响整体  
✅ **详细日志** - 同时输出到文件和控制台  
✅ **超时保护** - 防止单个文件扫描卡死  
✅ **路径灵活** - 支持中文路径和长路径  
✅ **框架中立** - 纯 subprocess 调用 scancode.bat  

### 依赖库

- `pandas` - Excel读写
- `openpyxl` - 底层Excel引擎
- Python标准库：`subprocess`, `threading`, `json`, `logging`, `pathlib`

---

## 📞 获取帮助

查看详细文档：
```bash
# 查看README
type README.md

# 查看快速开始
python QUICK_START.py

# 查看脚本帮助
python scan_licenses.py --help
```

---

*最后更新：2026-02-10*
