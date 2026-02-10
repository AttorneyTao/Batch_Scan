# 断点接续功能说明

## 📍 功能概述

**断点接续**是一个强大的功能，允许你在扫描中断后继续进行，而不需要重新扫描已完成的文件。这对大规模项目非常有用。

### 主要特点

✅ **自动保存进度** - 每个文件扫描完成立即保存  
✅ **中断安全** - 即使崩溃也不会丢失数据  
✅ **跳过已扫描** - 自动跳过已扫描的文件  
✅ **智能统计** - 显示总进度和增量进度  
✅ **灵活控制** - 支持恢复、重置等操作  

---

## 🚀 快速开始

### 基础用法（自动启用断点接续）

```bash
python main.py "D:\project"
```

首次扫描时：
```
✓ 启用断点接续功能（进度文件: scan_progress.json）
需要扫描的文件数: 1000
```

中途中断后重新运行相同命令：
```
✓ 已加载进度文件，包含 500 个已扫描文件
✓ 跳过了 500 个已扫描文件，本次需扫描 500 个
```

---

## 📋 命令参数

### 专用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p, --progress-file` | 进度文件路径 | `scan_progress.json` |
| `--resume` | 启用断点接续 | True（默认启用） |
| `--skip-resume` | 跳过断点接续，重新扫描 | False |
| `--reset` | 重置进度文件并退出 | False |

---

## 💡 使用场景

### 场景1：大项目首次扫描（中途中断）

```bash
# 首次运行，扫描5000个文件
python main.py "D:\huge_project" -t 16

# 运行2小时后网络故障，中断了
# 重新运行相同命令，自动从第2500个文件继续

python main.py "D:\huge_project" -t 16

# 输出：
# ✓ 已加载进度文件，包含 2500 个已扫描文件
# ✓ 跳过了 2500 个已扫描文件，本次需扫描 2500 个
```

### 场景2：分批处理项目

```bash
# 第一天：扫描前1000个文件
python main.py "D:\project" -t 8

# 第二天：继续扫描剩余的文件
python main.py "D:\project" -t 16  # 可以改变线程数

# 输出：
# ✓ 已加载进度文件，包含 1000 个已扫描文件
# ✓ 跳过了 1000 个已扫描文件，本次需扫描 N 个
```

### 场景3：更新输入文件后重新扫描

```bash
# 原始扫描
python main.py "D:\project" -i files_v1.xlsx

# 加入新文件后重新扫描（自动检测新增文件）
python main.py "D:\project" -i files_v2.xlsx

# 只扫描新增的文件，之前的跳过
```

### 场景4：完全重新扫描

```bash
# 重置进度，删除进度文件
python main.py "D:\project" --reset

# 或跳过断点接续，强制重新扫描
python main.py "D:\project" --skip-resume
```

---

## 🔍 进度文件详解

### 文件格式（scan_progress.json）

```json
{
  "0": {
    "file_path": "D:\\project\\file1.cpp",
    "license_expression_spdx": "MIT",
    "error": null
  },
  "1": {
    "file_path": "D:\\project\\file2.h",
    "license_expression_spdx": "Apache-2.0",
    "error": null
  },
  "5": {
    "file_path": "D:\\project\\file6.hpp",
    "license_expression_spdx": null,
    "error": "文件不存在: ..."
  }
}
```

### 文件特点

- **紧凑格式** - 每个文件的结果保存一次
- **完整信息** - 包含扫描结果、错误信息
- **实时更新** - 每个文件扫描完成立即保存
- **可读性强** - 使用缩进JSON格式

### 自定义位置

```bash
# 使用自定义进度文件位置
python main.py "D:\project" -p "./progress/scan_v1.json"

# 多个独立的扫描进度
python main.py "D:\project1" -p "progress_p1.json"
python main.py "D:\project2" -p "progress_p2.json"
```

---

## 📊 进度显示

### 进度日志示例

```
============================================================
开始license扫描任务
输入文件: input.xlsx
输出文件: output.xlsx
路径前缀: D:\project
并行线程数: 16
进度文件: scan_progress.json
============================================================

✓ 已加载进度文件，包含 2500 个已扫描文件
✓ 启用断点接续功能（进度文件: scan_progress.json）
✓ 跳过了 2500 个已扫描文件，本次需扫描 2500 个

开始扫描文件: D:\project\file2501.cpp
文件 D:\project\file2501.cpp 扫描完成，检测到license: MIT
进度: 1/2500 (总已扫描: 2501)

...

============================================================
总文件数: 5000
已扫描文件数: 5000
本次新扫描: 2500
检测到license的文件数: 4800
未检测到license的文件数: 200
✓ 所有文件扫描完成！
============================================================
```

### 进度指标说明

| 指标 | 含义 |
|------|------|
| `总文件数` | input.xlsx 中的所有文件 |
| `已扫描文件数` | 进度文件中已完成的文件 |
| `本次新扫描` | 这次运行新扫描的文件数 |
| `检测到license` | 找到许可证信息的文件 |
| `未检测到license` | 没有找到许可证的文件 |

---

## ⚙️ 高级用法

### 多并发扫描

```bash
# 使用不同的进度文件，同时扫描不同的项目
python main.py "D:\project1" -p progress1.json -t 8 &
python main.py "D:\project2" -p progress2.json -t 8 &
```

### 继续上次中断的扫描（明确指定）

```bash
# 自动继续（默认行为）
python main.py "D:\project"

# 显式启用（也是默认）
python main.py "D:\project" --resume
```

### 强制重新扫描所有文件

```bash
# 方法1：跳过断点接续
python main.py "D:\project" --skip-resume

# 方法2：先重置再扫描
python main.py "D:\project" --reset
python main.py "D:\project"

# 方法3：手动删除进度文件
del scan_progress.json
python main.py "D:\project"
```

### 自定义进度文件名

```bash
# 为不同阶段使用不同的进度文件
python main.py "D:\project" -p scan_progress_phase1.json
python main.py "D:\project" -p scan_progress_phase2.json

# 最终合并结果时只使用最后的output.xlsx
```

---

## 🛡️ 故障恢复

### 进度文件损坏

如果 `scan_progress.json` 损坏或无效：

```bash
# 重置并重新开始
python main.py "D:\project" --reset
python main.py "D:\project"
```

### 输出文件损坏

如果 `output.xlsx` 损坏但进度文件完好：

```bash
# 只重新生成输出文件（无需重新扫描）
python main.py "D:\project" -o output_new.xlsx

# 进度文件中的所有数据会用来重建output.xlsx
```

### 部分文件扫描失败

```bash
# 进度文件记录了所有错误信息
# 可用记事本或JSON查看器查看 scan_progress.json

# 修复问题后继续扫描
python main.py "D:\project"  # 失败的文件会重新尝试
```

---

## 📈 性能建议

### 大型项目建议

对于超过1000个文件的项目：

```bash
# 第一次扫描：使用较多线程
python main.py "D:\huge_project" -t 32

# 如果中断，继续扫描即可
python main.py "D:\huge_project" -t 32
```

### 断点设计

```bash
# 每隔一段时间运行一次检查
# 例如每小时检查一次进度

# 脚本会自动：
# 1. 加载已有进度
# 2. 跳过已扫描文件
# 3. 扫描剩余文件
# 4. 保存进度
```

---

## 📝 常见问题

### Q: 可以同时修改progress文件吗？

**A:** 不建议。脚本每个文件完成后会立即保存，修改可能导致数据冲突。

### Q: progress文件能手动编辑吗？

**A:** 可以，但不建议。格式必须是有效的JSON，否则脚本会重新开始。

### Q: 如何在不同机器上继续扫描？

**A:** 复制 `scan_progress.json` 到新机器，确保输入文件路径一致。

### Q: progress文件能删除吗？

**A:** 可以，删除后脚本会从头开始（相当于 `--reset`）。

### Q: 如何查看已扫描的文件结果？

**A:** 
- 查看进度文件：`type scan_progress.json`
- 查看输出：打开 `output.xlsx`

### Q: 断点接续对性能有影响吗？

**A:** 几乎没有。只是在每个文件完成后多保存一次JSON数据。

---

## 🎯 典型工作流

```bash
# 第1天：开始大规模扫描
python main.py "D:\huge_project" -t 16
# 运行4小时，完成2000个文件

# 中断（网络问题/计划维护）
# (按 Ctrl+C 中断)

# 第2天：恢复扫描
python main.py "D:\huge_project" -t 16
# 自动跳过2000个已扫描文件，继续剩余的

# 完成后
python main.py "D:\huge_project" --reset  # 清理进度文件，保留output.xlsx
```

---

## 📚 参考

相关文件：
- [USAGE.md](USAGE.md) - 使用指南
- [README.md](README.md) - 项目文档
- [CHEATSHEET.py](CHEATSHEET.py) - 命令速查

命令帮助：
```bash
python scan_licenses.py --help
```

---

*断点接续功能完全透明，脚本自动管理，用户无需手动干预。*
