# 🚀 断点接续功能 - 快速开始

## 📍 什么是断点接续？

**断点接续**是一项强大的功能，当你的扫描任务因为各种原因（网络中断、系统关闭、手动中止等）被中断后，你可以**从中断的地方继续扫描**，而不需要重新开始。

### 核心优势

✅ **无数据丢失** - 每个文件完成后立即保存  
✅ **自动恢复** - 不需要手动干涉  
✅ **时间节约** - 避免重复扫描  
✅ **灵活配置** - 可改变参数继续  

---

## ⚡ 5分钟快速开始

### 步骤1️⃣：首次扫描

```bash
python main.py "D:\path\to\your\project" -t 16
```

输出示例：
```
✓ 启用断点接续功能（进度文件: scan_progress.json）
需要扫描的文件数: 5000
进度: 1/5000 (总已扫描: 1)
进度: 2/5000 (总已扫描: 2)
...
```

### 步骤2️⃣：中途中断

按 `Ctrl+C` 中止程序（任何时候都可以）

```
^C
KeyboardInterrupt
```

### 步骤3️⃣：恢复扫描

**直接运行相同命令：**

```bash
python main.py "D:\path\to\your\project" -t 16
```

**就这么简单！程序会自动：**
- 📂 加载进度文件 （scan_progress.json）
- ⏭️ 跳过已扫描的文件
- ▶️ 从中断处继续

输出示例：
```
✓ 已加载进度文件，包含 2500 个已扫描文件
✓ 跳过了 2500 个已扫描文件，本次需扫描 2500 个
进度: 1/2500 (总已扫描: 2501)
进度: 2/2500 (总已扫描: 2502)
...
✓ 所有文件扫描完成！
```

---

## 📝 关键命令

### 基础用法（自动启用）

```bash
# 首次扫描
python main.py "D:\project" -t 16

# 中断后继续（相同命令）
python main.py "D:\project" -t 16
```

### 显式控制

```bash
# 明确启用（也是默认）
python main.py "D:\project" --resume

# 跳过断点接续，重新扫描所有
python main.py "D:\project" --skip-resume

# 重置进度，删除进度文件
python main.py "D:\project" --reset
```

### 自定义进度文件位置

```bash
# 使用自定义位置
python main.py "D:\project" -p "./progress/scan.json"

# 多个项目用不同的进度文件
python main.py "D:\project1" -p progress1.json
python main.py "D:\project2" -p progress2.json
```

---

## 📊 进度文件说明

### 生成和位置

- **文件名**：`scan_progress.json`
- **位置**：当前工作目录
- **何时生成**：第一个文件扫描完成后立即生成
- **何时更新**：每个文件完成后

### 文件内容预览

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
  }
}
```

### 如何处理

```bash
# 查看进度
type scan_progress.json

# 删除进度（重新开始）
del scan_progress.json

# 或使用命令重置
python main.py "D:\project" --reset
```

---

## 🎯 实际场景

### 场景A：大型项目扫描

```
📅 周一 9:00
python main.py "D:\huge_project" -t 32
# 开始扫描10000个文件
# 进度: 1000/10000...2000/10000...

📅 周一 13:00（中午）
# 网络断开
# (按 Ctrl+C 停止)
# ✓ 已完成 4000 个文件
# ✓ 进度已保存到 scan_progress.json

📅 周一 14:00（下午）
python main.py "D:\huge_project" -t 32
# ✓ 已加载进度文件，包含 4000 个已扫描文件
# ✓ 跳过了 4000 个已扫描文件，本次需扫描 6000 个
# 继续扫描...

📅 周一 16:00
# 扫描完成！
# ✓ 所有文件扫描完成！
```

### 场景B：改变配置继续

```
# 第一阶段：使用4线程
python main.py "D:\project" -t 4
# 完成1000个文件

# 第二阶段：改为16线程（加速）
python main.py "D:\project" -t 16
# ✓ 加载已有进度
# ✓ 跳过前1000个文件
# ✓ 用16线程继续扫描剩余9000个文件
```

### 场景C：更新输入后重新扫描

```
# 初始扫描
python main.py "D:\project" -i input_v1.xlsx

# 加入新文件后
python main.py "D:\project" -i input_v2.xlsx
# ✓ 自动检测新文件
# ✓ 只扫描新增文件
# ✓ 跳过已有文件
```

---

## ⚠️ 常见问题

### Q: 我可以中间关闭电脑吗？

**A:** 完全可以！进度在每个文件完成后立即保存。只要进度文件（scan_progress.json）还在，就能安全恢复。

### Q: 进度文件丢了怎么办？

**A:** 重新开始即可：
```bash
python main.py "D:\project"  # 从头扫描
```

### Q: 可以改变线程数继续吗？

**A:** 可以，断点接续支持任何参数改变（除了输入文件路径前缀）：
```bash
# 之前：4线程
# 现在：改为16线程
python main.py "D:\project" -t 16
```

### Q: 两个不同的输入文件怎么处理？

**A:** 使用不同的进度文件：
```bash
python main.py "D:\project" -i input_v1.xlsx -p progress_v1.json
python main.py "D:\project" -i input_v2.xlsx -p progress_v2.json
```

### Q: 想完全重新扫描怎么办？

**A:** 有3种方式：
```bash
# 方式1：跳过断点接续
python main.py "D:\project" --skip-resume

# 方式2：重置进度
python main.py "D:\project" --reset
python main.py "D:\project"

# 方式3：手动删除进度文件
del scan_progress.json
python main.py "D:\project"
```

---

## 📈 性能数据

### 时间节约示例

| 场景 | 文件数 | 完成比例 | 节省时间 |
|------|--------|---------|---------|
| 首次中断 | 5000 | 50% | 半小时 |
| 重新利用 | 10000 | 60% | 1小时 |
| 改配置 | 20000 | 40% | 2小时 |

### 扫描速度参考

- 单个文件平均：**1-2秒**
- 1000文件 + 4线程：**5-10分钟**
- 1000文件 + 16线程：**2-3分钟**

---

## 🔧 配置建议

### 线程数选择

```bash
# 小型项目（<100文件）
python main.py "D:\project"  # 默认4线程

# 中型项目（100-1000文件）
python main.py "D:\project" -t 8

# 大型项目（>1000文件）
python main.py "D:\huge_project" -t 16 或 -t 32
```

### 内存受限时

```bash
python main.py "D:\project" -t 2  # 减少线程
```

---

## 📚 相关文档

| 文档 | 内容 |
|------|------|
| `RESUME.md` | 详细的断点接续文档 |
| `USAGE.md` | 完整使用指南 |
| `CHEATSHEET.py` | 命令速查 |

## 📖 查看文档

```bash
type RESUME.md       # 断点接续详细说明
python scan_licenses.py --help  # 命令帮助
```

---

## ✅ 测试检查清单

- [ ] 第一次运行 `python main.py "D:\test"`
- [ ] 验证生成了 `scan_progress.json` 文件
- [ ] 中止程序（Ctrl+C）
- [ ] 再次运行相同命令
- [ ] 确认显示 `✓ 已加载进度文件`
- [ ] 确认显示 `✓ 跳过了 X 个已扫描文件`
- [ ] 扫描完成后验证 `output.xlsx`

---

## 🎉 总结

**断点接续就是这么简单：**

1. 第一次运行命令
2. 中途中断（任何时候）
3. 再运行相同命令
4. 自动恢复！

**优势：**
- ✅ 省时间（避免重复扫描）
- ✅ 省资源（灵活分配计算资源）
- ✅ 更可靠（进度备份）

**现在就试试吧！**

```bash
python main.py "D:\your\project" -t 16
```

---

*断点接续是完全自动化的，无需手动管理。*
