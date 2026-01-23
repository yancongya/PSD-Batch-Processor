"""
批量处理核心逻辑
负责协调备份、执行脚本、更新状态等
"""

import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.core.photoshop_controller import PhotoshopController
from app.models.file_item import FileItem, FileList, FileStatus
from app.config.settings import get_settings
from utils.logger import get_logger


class BatchProcessor:
    """批量处理器"""

    def __init__(self):
        self.logger = get_logger()
        self.settings = get_settings()
        self.controller = PhotoshopController(self.settings.photoshop_path)
        self.file_list = FileList()

        # 回调函数
        self._on_progress: Optional[Callable[[int, int, str], None]] = None
        self._on_status_update: Optional[Callable[[str, str], None]] = None
        self._on_finished: Optional[Callable[[int, int, float], None]] = None

        # 处理状态
        self.is_processing = False
        self.total_processed = 0
        self.total_success = 0
        self.total_failed = 0

    def set_callbacks(self, on_progress=None, on_status_update=None, on_finished=None):
        """设置回调函数"""
        if on_progress is not None:
            self._on_progress = on_progress
        if on_status_update is not None:
            self._on_status_update = on_status_update
        if on_finished is not None:
            self._on_finished = on_finished

    def _notify_progress(self, current: int, total: int, message: str):
        """通知进度更新"""
        if self._on_progress:
            self._on_progress(current, total, message)

    def _notify_status(self, file_name: str, status: str):
        """通知状态更新"""
        if self._on_status_update:
            self._on_status_update(file_name, status)

    def _notify_finished(self, success: int, failed: int, elapsed: float):
        """通知处理完成"""
        if self._on_finished:
            self._on_finished(success, failed, elapsed)

    def create_backup_folder(self) -> Tuple[bool, Path]:
        """
        创建本次备份文件夹

        Returns:
            (是否成功, 备份文件夹路径)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 使用新的路径处理方法，支持单文件EXE
        backup_root = self.settings.get_backup_dir_path()
        backup_folder = backup_root / timestamp

        try:
            backup_folder.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"创建备份文件夹: {backup_folder}")
            return True, backup_folder
        except Exception as e:
            self.logger.error(f"创建备份文件夹失败: {e}")
            return False, Path()

    def backup_file(self, file_item: FileItem, backup_folder: Path) -> Tuple[bool, str]:
        """
        备份单个文件

        Args:
            file_item: 文件项
            backup_folder: 备份文件夹

        Returns:
            (是否成功, 消息)
        """
        try:
            # 目标备份路径
            dest_path = backup_folder / file_item.file_name

            # 如果同名文件已存在，添加序号
            counter = 1
            original_dest = dest_path
            while dest_path.exists():
                name_stem = original_dest.stem
                name_suffix = original_dest.suffix
                dest_path = original_dest.parent / f"{name_stem}_{counter}{name_suffix}"
                counter += 1

            # 复制文件（保留元数据）
            shutil.copy2(file_item.path, dest_path)

            # 记录备份路径
            file_item.set_backup_path(dest_path)

            self.logger.info(f"备份完成: {file_item.file_name} -> {dest_path.name}")
            return True, "备份成功"

        except Exception as e:
            error_msg = f"备份失败: {e}"
            self.logger.error(f"{file_item.file_name}: {error_msg}")
            return False, error_msg

    def process_single_file(self, file_item: FileItem, backup_folder: Path,
                           script_path: str) -> Tuple[bool, str]:
        """
        处单个文件

        Args:
            file_item: 文件项
            backup_folder: 备份文件夹
            script_path: JSX 脚本路径

        Returns:
            (是否成功, 消息)
        """
        start_time = time.time()

        try:
            # 1. 备份文件
            self._notify_status(file_item.file_name, "正在备份...")
            backup_success, backup_msg = self.backup_file(file_item, backup_folder)
            if not backup_success:
                return False, backup_msg

            file_item.set_status(FileStatus.BACKUP_COMPLETED)
            self._notify_status(file_item.file_name, "备份完成")

            # 2. 打开文件并执行脚本
            self._notify_status(file_item.file_name, "正在处理...")
            file_item.set_status(FileStatus.PROCESSING)

            # 确保连接到 Photoshop
            if not self.controller.is_connected():
                self.logger.warning(f"Photoshop 连接断开，尝试重新连接...")
                connect_success, connect_msg = self.controller.connect(launch_if_needed=True)
                if not connect_success:
                    error_msg = f"Photoshop 连接失败: {connect_msg}"
                    self.logger.error(error_msg)
                    # 标记所有剩余文件为失败
                    file_item.set_status(FileStatus.FAILED, error_msg)
                    self._notify_status(file_item.file_name, f"❌ {error_msg}")
                    return False, error_msg

            # 打开 PSD 文件
            open_success, open_msg = self.controller.open_document(str(file_item.path))
            if not open_success:
                error_msg = f"无法打开文件: {open_msg}"
                file_item.set_status(FileStatus.FAILED, error_msg)
                self._notify_status(file_item.file_name, f"❌ {error_msg}")
                self.logger.error(f"打开文件失败: {file_item.file_name} - {open_msg}")
                return False, error_msg

            # 执行 JSX 脚本
            exec_success, exec_msg = self.controller.run_jsx_script(script_path)

            # 关闭文档（保存更改）
            close_success, close_msg = self.controller.close_document(save=True)
            if not close_success:
                self.logger.warning(f"关闭文档时出现问题: {close_msg}")

            elapsed = time.time() - start_time
            file_item.process_time = elapsed

            if exec_success:
                file_item.set_status(FileStatus.SUCCESS)
                self._notify_status(file_item.file_name, "✅ 处理成功")
                self.logger.success(f"处理完成: {file_item.file_name} ({elapsed:.2f}s)")
                return True, exec_msg
            else:
                file_item.set_status(FileStatus.FAILED, exec_msg)
                self._notify_status(file_item.file_name, f"❌ 处理失败: {exec_msg}")
                self.logger.error(f"处理失败: {file_item.file_name} - {exec_msg}")
                return False, exec_msg

        except Exception as e:
            elapsed = time.time() - start_time
            file_item.process_time = elapsed
            error_msg = f"处理异常: {e}"
            file_item.set_status(FileStatus.FAILED, error_msg)
            self._notify_status(file_item.file_name, f"❌ {error_msg}")
            self.logger.error(f"处理异常: {file_item.file_name} - {e}")
            return False, error_msg

    def process_batch(self, script_path: str, max_workers: Optional[int] = None) -> Tuple[int, int, float]:
        """
        批量处理文件

        Args:
            script_path: JSX 脚本路径
            max_workers: 最大并发数

        Returns:
            (成功数, 失败数, 总耗时)
        """
        if self.is_processing:
            self.logger.warning("处理正在进行中...")
            return 0, 0, 0

        start_time = time.time()
        self.is_processing = True
        self.total_processed = 0
        self.total_success = 0
        self.total_failed = 0

        try:
            # 验证脚本路径
            script_file = Path(script_path)
            if not script_file.exists():
                self.logger.error(f"JSX 脚本不存在: {script_path}")
                return 0, 0, 0

            # 获取待处理文件
            pending_files = self.file_list.get_pending()
            if not pending_files:
                self.logger.warning("没有待处理的文件")
                return 0, 0, 0

            total_files = len(pending_files)
            self.logger.info(f"开始批量处理 {total_files} 个文件")

            # 创建备份文件夹
            backup_success, backup_folder = self.create_backup_folder()
            if not backup_success:
                self.logger.error("无法创建备份文件夹，停止处理")
                return 0, 0, 0

            # 设置并发数
            if max_workers is None:
                max_workers = self.settings.max_workers
            max_workers = max(1, min(max_workers, 2))  # 限制为 1-2

            self.logger.info(f"使用 {max_workers} 个并发线程")

            # 连接到 Photoshop
            self.logger.info("正在连接 Photoshop...")
            connect_success, connect_msg = self.controller.connect(launch_if_needed=True)
            if not connect_success:
                self.logger.error(f"无法连接 Photoshop: {connect_msg}")
                return 0, 0, 0

            # 单线程处理（推荐，避免 Photoshop 内存问题）
            if max_workers == 1:
                for i, file_item in enumerate(pending_files, 1):
                    self._notify_progress(i, total_files, f"处理中 ({i}/{total_files})")

                    success, msg = self.process_single_file(file_item, backup_folder, script_path)

                    self.total_processed += 1
                    if success:
                        self.total_success += 1
                    else:
                        self.total_failed += 1
                        # 如果是Photoshop连接失败，停止整个处理
                        if "Photoshop 连接失败" in msg or "无法连接 Photoshop" in msg:
                            self.logger.error(f"Photoshop 连接失败，停止批量处理")
                            # 标记剩余文件为失败
                            for remaining_file in pending_files[i:]:
                                remaining_file.set_status(FileStatus.FAILED, "Photoshop 连接失败，处理中止")
                                self.total_failed += 1
                                self.total_processed += 1
                            break

            # 多线程处理（实验性）
            else:
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # 提交所有任务
                    future_to_file = {
                        executor.submit(self.process_single_file, item, backup_folder, script_path): item
                        for item in pending_files
                    }

                    # 处理完成的任务
                    completed = 0
                    for future in as_completed(future_to_file):
                        completed += 1
                        file_item = future_to_file[future]

                        self._notify_progress(completed, total_files, f"处理中 ({completed}/{total_files})")

                        try:
                            success, msg = future.result()
                            self.total_processed += 1
                            if success:
                                self.total_success += 1
                            else:
                                self.total_failed += 1
                        except Exception as e:
                            self.logger.error(f"任务异常: {file_item.file_name} - {e}")
                            file_item.set_status(FileStatus.FAILED, str(e))
                            self.total_processed += 1
                            self.total_failed += 1

            # 处理完成
            elapsed = time.time() - start_time
            self.is_processing = False

            # 断开 Photoshop 连接
            self.controller.disconnect()

            # 发送完成通知
            self._notify_finished(self.total_success, self.total_failed, elapsed)

            # 输出总结
            self.logger.info("=" * 60)
            self.logger.info(f"批量处理完成!")
            self.logger.info(f"总文件数: {total_files}")
            self.logger.info(f"成功: {self.total_success}")
            self.logger.info(f"失败: {self.total_failed}")
            self.logger.info(f"耗时: {elapsed:.2f} 秒")
            self.logger.info(f"备份位置: {backup_folder}")
            self.logger.info("=" * 60)

            return self.total_success, self.total_failed, elapsed

        except Exception as e:
            self.logger.error(f"批量处理异常: {e}")
            self.is_processing = False
            self.controller.disconnect()
            return 0, 0, 0

    def stop_processing(self):
        """停止处理"""
        if self.is_processing:
            self.logger.warning("正在停止处理...")
            self.is_processing = False
            self.controller.disconnect()

    def get_backup_folder(self) -> Optional[Path]:
        """获取最近的备份文件夹"""
        backup_root = Path(self.settings.backup_dir)
        if not backup_root.exists():
            return None

        folders = [f for f in backup_root.iterdir() if f.is_dir()]
        if not folders:
            return None

        # 返回最新的文件夹
        folders.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return folders[0]
