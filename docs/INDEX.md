# 📑 项目文件索引

## 🚀 快速导航

### 🎯 立即开始

```bash
# 1. 查看快速参考卡
python CHEATSHEET.py

# 2. 生成示例输入
python create_sample.py

# 3. 运行扫描
python main.py "D:\path\to\project"
```

---

## 📚 文档文件

| 文件 | 用途 | 推荐阅读时机 |
|------|------|-----------|
| **README.md** | 项目概述、安装指南 | 第一次了解项目 |
| **USAGE.md** | 详细使用文档（最完整） | 学习深入功能 |
| **SUMMARY.md** | 项目完成总结 | 了解技术实现 |
| **QUICK_START.py** | 快速开始代码参考 | 快速查阅示例 |
| **CHEATSHEET.py** | 命令速查卡（可执行） | 日常工作速查 |
| **此文件** | 项目文件索引 | 查找具体文件 |

---

## 💻 实现文件

| 文件 | 功能 | 说明 |
|------|------|------|
| **scan_licenses.py** | 核心扫描逻辑 | 独立运行：`python scan_licenses.py --help` |
| **main.py** | 入口包装脚本 | CLI接口：`python main.py <prefix>` |
| **create_sample.py** | 示例数据生成 | 生成演示Excel：`python create_sample.py` |

---

## 📋 配置文件

| 文件 | 用途 |
|------|------|
| **pyproject.toml** | Python项目配置、依赖声明 |
| **uv.lock** | 依赖版本锁定（UV生成） |
| **.python-version** | Python版本指定（3.13+） |
| **.gitignore** | Git忽略配置 |

---

## 📊 数据文件

| 文件 | 类型 | 说明 |
|------|------|------|
| **input.xlsx** | 样例 | 示例输入（可删除，用`create_sample.py`重新生成） |
| **result.json** | 参考 | scancode输出格式参考 |

---

## 🎓 学习路径

### 初次使用者 👤

1. **了解项目** → 阅读 [README.md](README.md)
2. **快速查阅** → 运行 `python CHEATSHEET.py`
3. **尝试示例** → `python create_sample.py` + `python main.py "D:\test"`
4. **查看结果** → output.xlsx + scan_licenses_*.log

### 日常使用者 🔄

```bash
python CHEATSHEET.py  # 查看快速参考
python main.py "<prefix>" -t 8  # 执行扫描
```

### 深度学习者 🔬

1. **详细文档** → [USAGE.md](USAGE.md)
2. **技术实现** → [SUMMARY.md](SUMMARY.md)
3. **源码阅读** → [scan_licenses.py](scan_licenses.py)

---

## 🔍 按需求查找

### 我想...

#### 快速开始
→ 运行 `python CHEATSHEET.py`  
→ 阅读 [QUICK_START.py](QUICK_START.py)

#### 了解使用方法
→ 阅读 [USAGE.md](USAGE.md)  
→ 查看 [README.md](README.md) 中的示例

#### 修改代码
→ 查看 [SUMMARY.md](SUMMARY.md) 中的架构说明  
→ 阅读 [scan_licenses.py](scan_licenses.py) 源码注释

#### 解决问题
→ 查看 [USAGE.md](USAGE.md) 中的常见问题部分  
→ 运行后查看 `scan_licenses_*.log` 日志

#### 自定义功能
→ 参考 [scan_licenses.py](scan_licenses.py) 中的函数  
→ 查看参数配置部分

#### 性能优化
→ [USAGE.md](USAGE.md) 中的性能优化部分  
→ [SUMMARY.md](SUMMARY.md) 中的性能指标

---

## 📝 文件详细说明

### scan_licenses.py 核心脚本

```python
主要函数：
  setup_logging()          - 日志初始化
  scan_file_with_scancode() - 单文件扫描
  main()                   - 主程序入口

参数控制：
  argparse处理所有命令行参数
  支持自定义线程数、Excel列等
```

### main.py 入口脚本

```python
作用：
  包装scan_licenses.py
  提供用户友好的help信息

使用：
  python main.py <prefix> [options]
  自动转发参数到scan_licenses.py
```

### create_sample.py 样例生成器

```python
功能：
  创建示例 input.xlsx
  包含5个文件条目
  展示输入格式

使用：
  python create_sample.py
  生成可修改的示例文件
```

---

## 🎯 常见任务

### 任务1：首次测试

```bash
# -1- 生成示例
python create_sample.py

# -2- 运行扫描
python main.py "D:\test" -t 4

# -3- 查看结果
type scan_licenses_*.log  # 查看日志
start output.xlsx         # 打开结果
```

### 任务2：实际使用

1. 准备 input.xlsx（包含path列）
2. 获得路径前缀（相对路径的根目录）
3. 运行：`python main.py "<prefix>" -i input.xlsx -o output.xlsx`
4. 查看 output.xlsx 中的新列

### 任务3：大规模扫描

```bash
# 增加线程数
python main.py "<prefix>" -t 32

# 监控日志
tail -f scan_licenses_*.log  # Linux/Mac
Get-Content scan_licenses_*.log -Wait  # PowerShell
```

### 任务4：自定义配置

```bash
# 自定义列名
python main.py "<prefix>" -c file_path

# 自定义输出
python main.py "<prefix>" -o my_report.xlsx

# 完整自定义
python scan_licenses.py "<prefix>" \
    -i source.xlsx \
    -o result.xlsx \
    -t 16 \
    -c filepath
```

---

## 🔗 文件关系图

```
入口层：
  main.py ────────────→ scan_licenses.py
  
  create_sample.py ──→ input.xlsx

核心执行：
  scan_licenses.py
    ├─ 调用 scancode.bat
    ├─ 读取 result.json (临时)
    ├─ 输出 output.xlsx
    └─ 生成 scan_licenses_*.log

参考文档：
  README.md (概述)
     ↓
  USAGE.md (详细)
     ↓
  SUMMARY.md (深入)
     ↓
  QUICK_START.py (示例)
     ↓
  CHEATSHEET.py (速查)
```

---

## 📦 项目统计

```
核心脚本：3个
│
├─ scan_licenses.py      (500+ 行)
├─ main.py              (30+ 行)
└─ create_sample.py     (30+ 行)

文档：5个
│
├─ README.md            (完整项目介绍)
├─ USAGE.md             (详细使用指南) ⭐ 最详细
├─ SUMMARY.md           (项目总结)
├─ QUICK_START.py       (快速示例)
└─ CHEATSHEET.py        (速查卡)

配置：4个
│
├─ pyproject.toml
├─ uv.lock
├─ .python-version
└─ .gitignore

数据：2个
│
├─ input.xlsx           (示例输入)
└─ result.json          (参考输出)

索引：1个 (此文件)

总计：15个文件
```

---

## 🚀 首次使用检查清单

- [ ] 已安装 ScanCode-toolkit 并配置到PATH
- [ ] 已验证：`scancode.bat --version` 可以运行
- [ ] 已阅读 README.md
- [ ] 已运行 `python CHEATSHEET.py` 查看参考
- [ ] 已准备或生成 input.xlsx
- [ ] 已确定路径前缀
- [ ] 已进行首次测试扫描
- [ ] 已检查 output.xlsx 结果
- [ ] 已查看 scan_licenses_*.log 日志

---

## 🎓 更多帮助

### 查看脚本帮助
```bash
python scan_licenses.py --help
python main.py --help  # 同上
```

### 查看文档
```bash
type README.md   # 概述
type USAGE.md    # 详细指南 ← 推荐！
type SUMMARY.md  # 技术总结
```

### 查看代码注释
```bash
# 打开编辑器查看
code scan_licenses.py
# 或其他编辑器
```

### 在线参考
- ScanCode文档：https://scancode-toolkit.readthedocs.io/
- SPDX许可证列表：https://spdx.org/licenses/
- Pandas文档：https://pandas.pydata.org/docs/

---

## 📅 版本信息

- **项目版本：** 0.1.0
- **创建日期：** 2026-02-10
- **Python版本：** 3.13+
- **依赖：** pandas >= 3.0.0, openpyxl >= 3.0.0
- **状态：** ✅ 完成并测试

---

## 🎯 下一步行动

1. **立即开始：**
   ```bash
   python CHEATSHEET.py
   ```

2. **尝试扫描：**
   ```bash
   python create_sample.py
   python main.py "D:\your\project"
   ```

3. **查看详细文档：**
   - [📖 USAGE.md](USAGE.md) - 最完整的使用指南
   - [📊 SUMMARY.md](SUMMARY.md) - 技术实现细节

---

**开始你的License合规检查之旅吧！** 🚀

*有问题？查看USAGE.md中的常见问题部分。*
