"""
日志工具模块
支持 GUI 日志显示和文件日志双输出
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable


class Logger:
    """日志管理类"""

    def __init__(self, log_dir: str = "logs", log_name: Optional[str] = None):
        """
        初始化日志器

        Args:
            log_dir: 日志目录
            log_name: 日志文件名（不含扩展名），默认使用时间戳
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 生成日志文件名
        if log_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_name = f"psd_batch_{timestamp}"

        self.log_file = self.log_dir / f"{log_name}.log"

        # 配置日志
        self.logger = logging.getLogger("PSDBatchProcessor")
        self.logger.setLevel(logging.DEBUG)

        # 避免重复添加 handler
        if not self.logger.handlers:
            # 文件处理器
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)

            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # 日志格式
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        # GUI 回调函数
        self._gui_callback: Optional[Callable[[str, str], None]] = None

    def set_gui_callback(self, callback: Callable[[str, str], None]):
        """
        设置 GUI 日志回调函数

        Args:
            callback: 回调函数，接收 (level, message) 参数
        """
        self._gui_callback = callback

    def _log_to_gui(self, level: str, message: str):
        """将日志发送到 GUI"""
        if self._gui_callback:
            try:
                self._gui_callback(level, message)
            except Exception:
                pass  # GUI 回调失败不影响日志记录

    def info(self, message: str):
        """记录 INFO 级别日志"""
        self.logger.info(message)
        self._log_to_gui("info", message)

    def success(self, message: str):
        """记录成功日志（自定义级别）"""
        # 使用 INFO 级别但标记为成功
        self.logger.info(f"[SUCCESS] {message}")
        self._log_to_gui("success", message)

    def warning(self, message: str):
        """记录 WARNING 级别日志"""
        self.logger.warning(message)
        self._log_to_gui("warning", message)

    def error(self, message: str):
        """记录 ERROR 级别日志"""
        self.logger.error(message)
        self._log_to_gui("error", message)

    def debug(self, message: str):
        """记录 DEBUG 级别日志"""
        self.logger.debug(message)
        self._log_to_gui("debug", message)

    def get_log_file(self) -> Path:
        """获取日志文件路径"""
        return self.log_file

    def clear(self):
        """清空日志文件"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write('')
            self.info("日志已清空")
        except Exception as e:
            self.error(f"清空日志失败: {e}")


# 全局日志实例
_logger = None


def get_logger(log_dir: str = "logs", log_name: Optional[str] = None) -> Logger:
    """获取全局日志实例"""
    global _logger
    if _logger is None:
        _logger = Logger(log_dir, log_name)
    return _logger


def init_logger(log_dir: str = "logs", log_name: Optional[str] = None) -> Logger:
    """初始化全局日志"""
    global _logger
    _logger = Logger(log_dir, log_name)
    return _logger


# 便捷函数
def log_info(message: str):
    """记录 INFO 日志"""
    get_logger().info(message)


def log_success(message: str):
    """记录成功日志"""
    get_logger().success(message)


def log_warning(message: str):
    """记录 WARNING 日志"""
    get_logger().warning(message)


def log_error(message: str):
    """记录 ERROR 日志"""
    get_logger().error(message)


def log_debug(message: str):
    """记录 DEBUG 日志"""
    get_logger().debug(message)
