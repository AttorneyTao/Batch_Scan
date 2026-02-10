"""
License scanning script using scancode-toolkit.
Scans multiple files in parallel and extracts SPDX license information.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import pandas as pd


class ProgressManager:
    """进度管理器 - 用于断点接续功能"""

    def __init__(self, progress_file: str, logger: logging.Logger):
        """
        初始化进度管理器

        Args:
            progress_file: 进度文件路径
            logger: 日志记录器
        """
        self.progress_file = progress_file
        self.logger = logger
        self.progress = {}
        self.load()

    def load(self):
        """从文件加载进度"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, "r", encoding="utf-8") as f:
                    self.progress = json.load(f)
                self.logger.info(
                    f"[OK] 已加载进度文件，包含 {len(self.progress)} 个已扫描文件"
                )
            except Exception as e:
                self.logger.warning(f"加载进度文件失败: {str(e)}，将从头开始")
                self.progress = {}
        else:
            self.logger.info("开始全新扫描，未找到进度文件")

    def save(self):
        """保存进度到文件"""
        try:
            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(self.progress, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存进度文件失败: {str(e)}")

    def get_completed(self) -> dict:
        """获取已完成的扫描结果"""
        return self.progress.copy()

    def add(self, idx: int, result: dict):
        """添加扫描结果"""
        self.progress[str(idx)] = result
        self.save()

    def get(self, idx: int) -> dict:
        """获取指定的扫描结果"""
        return self.progress.get(str(idx))

    def exists(self, idx: int) -> bool:
        """检查是否已扫描"""
        return str(idx) in self.progress

    def reset(self):
        """重置进度"""
        self.progress = {}
        if os.path.exists(self.progress_file):
            os.remove(self.progress_file)
            self.logger.info("[OK] 进度文件已重置")

    def count(self) -> int:
        """获取已完成的扫描数"""
        return len(self.progress)


def setup_logging(log_dir: str = ".") -> logging.Logger:
    """设置日志记录"""
    log_file = os.path.join(
        log_dir,
        f"scan_licenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    logger = logging.getLogger(__name__)
    # 为 StreamHandler 设置 UTF-8 编码错误处理
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            # 设置编码错误处理为替换不可编码的字符
            if hasattr(handler.stream, 'buffer'):
                import io
                handler.stream = io.TextIOWrapper(
                    handler.stream.buffer, encoding='utf-8', errors='replace'
                )
    logger.info(f"日志文件已保存到: {log_file}")
    return logger


def scan_file_with_scancode(
    file_path: str, temp_json_path: str, logger: logging.Logger, debug_dir: str = None
) -> dict:
    """
    使用scancode扫描单个文件 (通过命令行)

    Args:
        file_path: 文件的完整路径
        temp_json_path: 临时JSON文件的路径
        logger: 日志记录器
        debug_dir: 调试目录，若提供则保存 JSON 结果

    Returns:
        包含扫描结果的字典
    """
    result = {"file_path": file_path, "license_expression_spdx": None, "error": None}

    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            error_msg = f"文件不存在: {file_path}"
            logger.warning(error_msg)
            result["error"] = error_msg
            return result

        logger.info(f"开始扫描文件: {file_path}")

        # 构建 scancode 命令 - 使用 python -m scancode 以确保正确的模块加载
        cmd = [
            sys.executable,
            "-m",
            "scancode.cli",
            "--license",
            "--json-pp",
            temp_json_path,
            file_path,
        ]
        logger.debug(f"执行命令: {' '.join(cmd)}")

        # 执行scancode
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5分钟超时
        )

        if process.returncode != 0:
            error_msg = f"scancode扫描失败: {process.stderr}"
            logger.error(f"文件 {file_path}: {error_msg}")
            result["error"] = error_msg
            return result

        # 读取JSON结果
        if not os.path.exists(temp_json_path):
            error_msg = f"JSON输出文件未生成: {temp_json_path}"
            logger.error(f"文件 {file_path}: {error_msg}")
            result["error"] = error_msg
            return result

        with open(temp_json_path, "r", encoding="utf-8") as f:
            scan_result = json.load(f)

        # 如果提供了调试目录，保存 JSON 结果用于调试
        if debug_dir:
            try:
                os.makedirs(debug_dir, exist_ok=True)
                # 使用文件名作为调试文件名
                safe_filename = Path(file_path).name.replace(" ", "_").replace(".", "_")
                debug_json_path = os.path.join(debug_dir, f"{safe_filename}.json")
                with open(debug_json_path, "w", encoding="utf-8") as f:
                    json.dump(scan_result, f, ensure_ascii=False, indent=2)
                logger.debug(f"调试 JSON 已保存: {debug_json_path}")
            except Exception as e:
                logger.warning(f"保存调试 JSON 失败: {str(e)}")

        # 提取license_expression_spdx
        license_spdx = None
        if "files" in scan_result and len(scan_result["files"]) > 0:
            file_result = scan_result["files"][0]
            
            # 方案1: 首先尝试从 detected_license_expression_spdx 获取（最直接）
            license_spdx = file_result.get("detected_license_expression_spdx")
            
            # 方案2: 如果没有，从 license_detections 中获取
            if not license_spdx and "license_detections" in file_result:
                if file_result["license_detections"]:
                    license_spdx = file_result["license_detections"][0].get(
                        "license_expression_spdx"
                    )

        result["license_expression_spdx"] = license_spdx
        logger.info(
            f"文件 {file_path} 扫描完成，检测到license: {license_spdx or '无'}"
        )

        return result

    except subprocess.TimeoutExpired:
        error_msg = f"扫描超时 (5分钟)"
        logger.error(f"文件 {file_path}: {error_msg}")
        result["error"] = error_msg
        return result
    except Exception as e:
        error_msg = f"扫描出错: {str(e)}"
        logger.error(f"文件 {file_path}: {error_msg}")
        result["error"] = error_msg
        return result
    finally:
        # 清理临时JSON文件
        if os.path.exists(temp_json_path):
            try:
                os.remove(temp_json_path)
            except Exception as e:
                logger.warning(f"删除临时文件失败 {temp_json_path}: {str(e)}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="使用scancode扫描Excel文件中列出的文件并提取SPDX license信息"
    )
    parser.add_argument(
        "prefix",
        type=str,
        help="相对路径的前缀（例如: C:\\path\\to\\project）",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default="input.xlsx",
        help="输入Excel文件路径 (default: input.xlsx)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.xlsx",
        help="输出Excel文件路径 (default: output.xlsx)",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=4,
        help="并行扫描的线程数 (default: 4)",
    )
    parser.add_argument(
        "-c",
        "--column",
        type=str,
        default="path",
        help="包含文件路径的列名 (default: path)",
    )
    parser.add_argument(
        "-p",
        "--progress-file",
        type=str,
        default="scan_progress.json",
        help="进度文件路径 (default: scan_progress.json)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=True,
        help="启用断点接续 (default: True)",
    )
    parser.add_argument(
        "--skip-resume",
        action="store_true",
        help="跳过断点接续，重新扫描所有文件",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="重置进度文件并退出",
    )

    args = parser.parse_args()

    # 确保 logs 目录存在
    os.makedirs("logs", exist_ok=True)
    
    # 设置日志
    logger = setup_logging("logs")
    logger.info("=" * 60)
    logger.info("开始license扫描任务")
    logger.info(f"输入文件: {args.input}")
    logger.info(f"输出文件: {args.output}")
    logger.info(f"路径前缀: {args.prefix}")
    logger.info(f"并行线程数: {args.threads}")
    logger.info(f"进度文件: {args.progress_file}")
    logger.info("=" * 60)

    # 初始化进度管理器
    progress_mgr = ProgressManager(args.progress_file, logger)

    # 处理重置选项
    if args.reset:
        progress_mgr.reset()
        logger.info("进度已重置，请重新运行扫描")
        sys.exit(0)

    # 确定是否启用断点接续
    use_resume = args.resume and not args.skip_resume
    if args.skip_resume:
        logger.info("[WARN] 跳过断点接续，将重新扫描所有文件")
        progress_mgr.reset()
    elif use_resume:
        logger.info(f"[OK] 启用断点接续功能（进度文件: {args.progress_file}）")

    try:
        # 检查input.xlsx是否存在
        if not os.path.exists(args.input):
            logger.error(f"输入文件不存在: {args.input}")
            sys.exit(1)

        # 读取input.xlsx
        logger.info(f"读取输入文件: {args.input}")
        df_input = pd.read_excel(args.input)

        # 检查path列是否存在
        if args.column not in df_input.columns:
            logger.error(f"输入文件中不存在'{args.column}'列")
            sys.exit(1)

        # 构建完整文件路径
        logger.info(f"准备扫描 {len(df_input)} 个文件")
        files_to_scan = []
        files_skip_count = 0
        for idx, relative_path in enumerate(df_input[args.column]):
            if pd.isna(relative_path):
                logger.warning(f"第 {idx + 2} 行的path列为空")
                continue
            # 规范化路径：将正斜杠转换为反斜杠（Windows）并移除路径混淆
            normalized_path = str(relative_path).replace('/', os.sep)
            full_path = os.path.normpath(os.path.join(args.prefix, normalized_path))

            # 检查是否已扫描（断点接续）
            if use_resume and progress_mgr.exists(idx):
                files_skip_count += 1
                logger.debug(f"跳过已扫描文件: {full_path}")
                continue

            files_to_scan.append((idx, full_path, relative_path))

        if use_resume and files_skip_count > 0:
            logger.info(f"[OK] 跳过了 {files_skip_count} 个已扫描文件，本次需扫描 {len(files_to_scan)} 个")
        else:
            logger.info(f"需要扫描的文件数: {len(files_to_scan)}")

        # 创建调试目录以保存 scancode 的 JSON 输出
        debug_dir = os.path.join(".", "scancode_debug_json")
        try:
            os.makedirs(debug_dir, exist_ok=True)
            logger.info(f"[OK] 调试模式已启用，JSON 结果将保存到: {debug_dir}")
        except Exception as e:
            logger.warning(f"无法创建调试目录: {str(e)}")
            debug_dir = None

        # 并行扫描文件
        scan_results = {}
        with tempfile.TemporaryDirectory() as temp_dir:
            with ThreadPoolExecutor(max_workers=args.threads) as executor:
                futures = {}
                for idx, full_path, relative_path in files_to_scan:
                    temp_json = os.path.join(temp_dir, f"result_{idx}.json")
                    future = executor.submit(
                        scan_file_with_scancode, full_path, temp_json, logger, debug_dir
                    )
                    futures[future] = idx

                # 收集结果
                completed = 0
                for future in as_completed(futures):
                    idx = futures[future]
                    try:
                        result = future.result()
                        scan_results[idx] = result
                        # 实时保存进度
                        progress_mgr.add(idx, result)
                        completed += 1
                        logger.info(
                            f"进度: {completed}/{len(files_to_scan)} (总已扫描: {progress_mgr.count()})"
                        )
                    except Exception as e:
                        logger.error(f"处理第 {idx + 2} 行出错: {str(e)}")
                        error_result = {
                            "file_path": files_to_scan[idx][1],
                            "license_expression_spdx": None,
                            "error": str(e),
                        }
                        scan_results[idx] = error_result
                        progress_mgr.add(idx, error_result)

        # 加载完整的扫描结果（包括之前扫描的）
        all_results = progress_mgr.get_completed()

        # 添加结果到DataFrame
        logger.info("将扫描结果添加到DataFrame")
        df_output = df_input.copy()
        df_output["license_expression_spdx_scancode"] = None

        for idx_str, result in all_results.items():
            idx = int(idx_str)
            if idx < len(df_output):
                df_output.loc[idx, "license_expression_spdx_scancode"] = result.get(
                    "license_expression_spdx"
                )

        # 保存结果到output.xlsx
        logger.info(f"保存输出文件: {args.output}")
        df_output.to_excel(args.output, index=False)
        logger.info("[OK] 输出文件已保存")

        # 统计信息
        detected_count = df_output["license_expression_spdx_scancode"].notna().sum()
        total_scanned = progress_mgr.count()
        total_files = len(df_input)
        logger.info("=" * 60)
        logger.info(f"总文件数: {total_files}")
        logger.info(f"已扫描文件数: {total_scanned}")
        logger.info(f"本次新扫描: {len(files_to_scan)}")
        logger.info(f"检测到license的文件数: {detected_count}")
        logger.info(f"未检测到license的文件数: {total_scanned - detected_count}")
        if total_scanned < total_files:
            logger.info(f"[WARN] 还有 {total_files - total_scanned} 个文件未扫描")
            logger.info(f"   继续扫描: python scan_licenses.py \"{args.prefix}\" -i {args.input} -o {args.output}")
        else:
            logger.info("[OK] 所有文件扫描完成！")
        logger.info("=" * 60)


    except Exception as e:
        logger.error(f"任务执行出错: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
