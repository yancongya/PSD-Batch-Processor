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
                self.logger.info("尝试连接已运行的 Photoshop...")
                self._photoshop = win32com.client.Dispatch("Photoshop.Application")
                self._is_connected = True
                self.logger.info("已连接到已运行的 Photoshop")
                return True, "成功连接到 Photoshop"

            except Exception as e:
                self.logger.warning(f"连接已运行Photoshop失败: {e}，尝试启动...")
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
                max_wait = 60
                for i in range(max_wait):
                    time.sleep(1)
                    try:
                        self._photoshop = win32com.client.Dispatch("Photoshop.Application")
                        self._is_connected = True
                        self.logger.success(f"Photoshop 启动成功 (等待 {i+1} 秒)")
                        return True, f"Photoshop 启动成功"
                    except Exception as connect_err:
                        self.logger.info(f"等待 Photoshop 响应... ({i+1}/{max_wait})")
                        if i == max_wait - 1:
                            return False, f"等待 Photoshop 启动超时: {connect_err}"

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

    def get_scratch_disks_info(self) -> Tuple[bool, str]:
        """获取Photoshop暂存盘信息"""
        if not self.is_connected():
            return False, "未连接到 Photoshop"

        try:
            import shutil
            self.logger.info("正在获取暂存盘信息...")
            
            # 使用更安全的JavaScript方法获取暂存盘信息
            js_code = """
            try {
                var prefs = app.preferences;
                var disks = new Array();
                
                // 尝试多种方式获取暂存盘
                if (typeof prefs.scratchDisks !== 'undefined' && prefs.scratchDisks) {
                    for (var i = 0; i < prefs.scratchDisks.length; i++) {
                        disks.push(prefs.scratchDisks[i]);
                    }
                } else if (typeof prefs.ScratchDisks !== 'undefined' && prefs.ScratchDisks) {
                    for (var i = 0; i < prefs.ScratchDisks.length; i++) {
                        disks.push(prefs.ScratchDisks[i]);
                    }
                } else {
                    // 尝试通过获取首选项文件路径
                    var tempFolder = Folder.temp;
                    disks.push(tempFolder.fsName);
                }
                
                disks.join('|');
            } catch (e) {
                'ERROR:' + e.toString();
            }
            """
            
            try:
                result = self._photoshop.DoJavaScript(js_code)
                self.logger.info(f"JavaScript返回: {result}")
                
                if result and not result.startswith("ERROR:"):
                    disk_paths = result.split('|')
                    info_parts = []
                    
                    for disk_path in disk_paths:
                        if disk_path and disk_path.strip():
                            try:
                                path = disk_path.strip()
                                if not path.endswith('\\'):
                                    path += '\\'
                                
                                self.logger.info(f"检查暂存盘: {path}")
                                
                                # 获取磁盘空间
                                total, used, free = shutil.disk_usage(path)
                                
                                total_gb = total / (1024**3)
                                free_gb = free / (1024**3)
                                used_percent = (used / total) * 100
                                
                                info_parts.append(f"{path}: {free_gb:.1f}GB 可用 / 共 {total_gb:.1f}GB ({used_percent:.0f}%已用)")
                            except Exception as e:
                                self.logger.warning(f"无法获取磁盘 {disk_path} 的信息: {e}")
                                info_parts.append(f"{disk_path}: 无法获取信息")
                    
                    if info_parts:
                        result_str = " | ".join(info_parts)
                        self.logger.success(f"暂存盘信息: {result_str}")
                        return True, result_str
                    else:
                        return False, "未设置暂存盘"
                else:
                    self.logger.error(f"JavaScript错误: {result}")
                    # 如果无法获取暂存盘信息，返回系统主盘信息作为备选
                    import os
                    main_drive = os.getenv('SystemDrive', 'C:')
                    try:
                        total, used, free = shutil.disk_usage(main_drive + '\\')
                        total_gb = total / (1024**3)
                        free_gb = free / (1024**3)
                        used_percent = (used / total) * 100
                        result_str = f"{main_drive}\\: {free_gb:.1f}GB 可用 / 共 {total_gb:.1f}GB ({used_percent:.0f}%已用) [系统主盘]"
                        self.logger.info(f"使用系统主盘信息: {result_str}")
                        return True, result_str
                    except:
                        return False, "无法获取暂存盘信息"
                    
            except Exception as e:
                self.logger.error(f"JavaScript执行失败: {e}")
                # 返回系统主盘信息作为备选
                import os
                try:
                    main_drive = os.getenv('SystemDrive', 'C:')
                    total, used, free = shutil.disk_usage(main_drive + '\\')
                    total_gb = total / (1024**3)
                    free_gb = free / (1024**3)
                    used_percent = (used / total) * 100
                    result_str = f"{main_drive}\\: {free_gb:.1f}GB 可用 / 共 {total_gb:.1f}GB ({used_percent:.0f}%已用) [系统主盘]"
                    return True, result_str
                except:
                    return False, f"JavaScript执行失败: {e}"
                
        except Exception as e:
            self.logger.error(f"获取暂存盘信息时发生异常: {e}")
            return False, f"获取失败: {e}"

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
            
            # 检查连接是否仍然有效
            if not self.is_connected():
                self.logger.warning("脚本执行后连接已断开")
            
            return False, error_msg

    def purge_cache(self) -> Tuple[bool, str]:
        """
        清理Photoshop缓存

        Returns:
            (是否成功, 消息)
        """
        if not self.is_connected():
            return False, "未连接到 Photoshop"

        try:
            # 执行清理缓存的JavaScript
            js_code = "app.purge(PurgeTarget.ALL_CACHES);"
            self._photoshop.DoJavaScript(js_code)
            self.logger.info("已清理 Photoshop 缓存")
            return True, "缓存清理成功"
        except Exception as e:
            error_msg = f"清理缓存失败: {e}"
            self.logger.warning(error_msg)
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
