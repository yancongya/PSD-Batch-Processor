"""
Photoshop COM 控制器
通过 win32com 控制 Photoshop，执行 JSX 脚本
"""

import os
import time
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

try:
    import win32com.client
    import pythoncom
except ImportError:
    win32com = None
    pythoncom = None

from utils.logger import get_logger
from app.core.script_args import get_script_args_manager


class PhotoshopController:
    """Photoshop COM 控制器"""

    def __init__(self, photoshop_path: Optional[str] = None):
        """
        初始化控制器

        Args:
            photoshop_path: Photoshop 可执行文件路径
        """
        self.logger = get_logger()
        self.photoshop_path = photoshop_path
        self._photoshop = None
        self._is_connected = False

    def connect(self, launch_if_needed: bool = True) -> Tuple[bool, str]:
        """
        连接到 Photoshop

        Args:
            launch_if_needed: 如果未运行是否启动 Photoshop

        Returns:
            (是否成功, 消息)
        """
        if win32com is None or pythoncom is None:
            return False, "pywin32 未安装，请运行: pip install pywin32"

        try:
            # 初始化 COM
            pythoncom.CoInitialize()

            # 尝试连接到已运行的 Photoshop
            try:
                self._photoshop = win32com.client.Dispatch("Photoshop.Application")
                self._is_connected = True
                self.logger.info("已连接到 Photoshop")
                return True, "成功连接到 Photoshop"

            except Exception as e:
                if not launch_if_needed:
                    return False, f"无法连接到 Photoshop: {e}"

                # 尝试启动 Photoshop
                if not self.photoshop_path:
                    return False, "未指定 Photoshop 路径，无法启动"

                ps_path = Path(self.photoshop_path)
                if not ps_path.exists():
                    return False, f"Photoshop 可执行文件不存在: {ps_path}"

                self.logger.info(f"正在启动 Photoshop: {ps_path}")
                os.startfile(str(ps_path))

                # 等待 Photoshop 启动
                max_wait = 30
                for i in range(max_wait):
                    time.sleep(1)
                    try:
                        self._photoshop = win32com.client.Dispatch("Photoshop.Application")
                        self._is_connected = True
                        self.logger.success(f"Photoshop 启动成功 (等待 {i+1} 秒)")
                        return True, f"Photoshop 启动成功"
                    except:
                        if i == max_wait - 1:
                            return False, f"等待 Photoshop 启动超时 ({max_wait} 秒)"

                return False, "启动 Photoshop 失败"

        except Exception as e:
            self.logger.error(f"连接 Photoshop 时出错: {e}")
            return False, f"连接错误: {e}"

    def disconnect(self):
        """断开与 Photoshop 的连接"""
        if self._photoshop:
            try:
                # 不关闭 Photoshop，只断开 COM 连接
                self._photoshop = None
                pythoncom.CoUninitialize()
                self._is_connected = False
                self.logger.info("已断开 Photoshop 连接")
            except Exception as e:
                self.logger.warning(f"断开连接时出错: {e}")

    def is_connected(self) -> bool:
        """检查是否已连接到 Photoshop"""
        if not self._is_connected:
            return False

        try:
            # 尝试访问一个属性来验证连接
            _ = self._photoshop.Name
            return True
        except:
            self._is_connected = False
            return False

    def run_jsx_script(self, jsx_path: str) -> Tuple[bool, str]:
        """
        执行 JSX 脚本

        Args:
            jsx_path: JSX 脚本文件路径

        Returns:
            (是否成功, 消息)
        """
        if not self.is_connected():
            return False, "未连接到 Photoshop"

        jsx_file = Path(jsx_path)
        if not jsx_file.exists():
            return False, f"JSX 脚本不存在: {jsx_path}"

        try:
            # 转换为绝对路径并确保使用正斜杠
            abs_path = jsx_file.resolve().as_posix()

            self.logger.info(f"执行 JSX 脚本: {jsx_file.name}")

            # 执行脚本
            result = self._photoshop.DoJavaScriptFile(abs_path)

            # 检查执行结果
            if result is None or result == "":
                self.logger.success(f"JSX 脚本执行成功: {jsx_file.name}")
                return True, "脚本执行成功"
            else:
                # 脚本返回了结果
                self.logger.info(f"JSX 脚本返回: {result}")

                # 检查是否包含错误信息
                result_str = str(result).lower()
                if "error" in result_str or "错误" in result_str:
                    return False, f"脚本执行出错: {result}"

                return True, f"脚本执行成功: {result}"

        except Exception as e:
            error_msg = f"执行 JSX 脚本失败: {e}"
            self.logger.error(error_msg)
            return False, error_msg

    def run_jsx_script_with_args(self, jsx_path: str, args_dict: Dict[str, Any]) -> Tuple[bool, str]:
        """
        执行 JSX 脚本（带自定义参数）

        Args:
            jsx_path: JSX 脚本文件路径
            args_dict: 自定义参数字典

        Returns:
            (是否成功, 消息)
        """
        if not self.is_connected():
            return False, "未连接到 Photoshop"

        jsx_file = Path(jsx_path)
        if not jsx_file.exists():
            return False, f"JSX 脚本不存在: {jsx_path}"

        try:
            abs_path = jsx_file.resolve().as_posix()

            # 创建参数文件
            args_manager = get_script_args_manager()
            args_file = args_manager.create_args_file(args_dict)

            self.logger.info(f"执行 JSX 脚本 (自定义参数): {jsx_file.name}")
            self.logger.info(f"参数: {args_dict}")

            # 执行脚本
            result = self._photoshop.DoJavaScriptFile(abs_path, [args_file])

            # 清理参数文件
            try:
                Path(args_file).unlink()
            except:
                pass

            # 检查执行结果
            if result is None or result == "":
                self.logger.success(f"JSX 脚本执行成功: {jsx_file.name}")
                return True, "脚本执行成功"
            else:
                result_str = str(result).lower()
                if "error" in result_str or "错误" in result_str:
                    return False, f"脚本执行出错: {result}"
                return True, f"脚本执行成功: {result}"

        except Exception as e:
            error_msg = f"执行 JSX 脚本失败: {e}"
            self.logger.error(error_msg)
            return False, error_msg

    def open_document(self, file_path: str) -> Tuple[bool, str]:
        """
        打开 PSD 文档

        Args:
            file_path: PSD 文件路径

        Returns:
            (是否成功, 消息)
        """
        if not self.is_connected():
            return False, "未连接到 Photoshop"

        psd_file = Path(file_path)
        if not psd_file.exists():
            return False, f"文件不存在: {file_path}"

        try:
            # 转换为绝对路径
            abs_path = str(psd_file.resolve())

            self.logger.info(f"打开文档: {psd_file.name}")

            # 打开文档
            doc = self._photoshop.Open(abs_path)

            if doc:
                self.logger.success(f"文档已打开: {psd_file.name}")
                return True, "文档打开成功"
            else:
                return False, "打开文档失败"

        except Exception as e:
            error_msg = f"打开文档失败: {e}"
            self.logger.error(error_msg)
            return False, error_msg

    def close_document(self, save: bool = False) -> Tuple[bool, str]:
        """
        关闭当前文档

        Args:
            save: 是否保存更改

        Returns:
            (是否成功, 消息)
        """
        if not self.is_connected():
            return False, "未连接到 Photoshop"

        try:
            # 获取当前活动文档
            doc = self._photoshop.ActiveDocument

            if not doc:
                return True, "没有活动文档"

            self.logger.info(f"关闭文档 (保存: {save})")

            if save:
                doc.Save()
                self.logger.info("文档已保存")

            doc.Close()
            self.logger.success("文档已关闭")

            return True, "文档关闭成功"

        except Exception as e:
            error_msg = f"关闭文档失败: {e}"
            self.logger.error(error_msg)
            return False, error_msg

    def get_photoshop_version(self) -> str:
        """获取 Photoshop 版本"""
        if not self.is_connected():
            return "未连接"

        try:
            version = self._photoshop.Version
            return str(version)
        except:
            return "未知版本"

    def __del__(self):
        """析构函数"""
        self.disconnect()
