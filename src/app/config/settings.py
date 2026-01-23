"""
配置管理模块
负责读取和保存用户配置，支持持久化

配置文件存储位置：
- 开发环境：程序目录下的 config.json
- 单文件EXE：用户数据目录下的 PSDBatchProcessor/config.json
  Windows: %APPDATA%/PSDBatchProcessor/config.json
"""

import json
import os
import sys
import shutil
from pathlib import Path
from typing import Optional, Dict, Any


class Settings:
    """配置管理类"""

    # 默认配置
    DEFAULT_CONFIG = {
        "photoshop_path": r"C:\Program Files\Adobe\Adobe Photoshop 2025\Photoshop.exe",
        "script_dir": "scripts",
        "backup_dir": "backups",
        "last_script": "",
        "max_workers": 1,  # 并发数，建议 1-2
        "theme": "dark",  # dark 或 light
        "include_subfolders": True,
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径，如果为 None 则使用默认位置
        """
        if config_path is None:
            # 检测是否为单文件打包模式
            if self._is_frozen():
                # 单文件EXE：使用用户数据目录
                self.config_path = self._get_user_data_dir() / "config.json"
            else:
                # 开发环境：使用程序目录
                self.config_path = Path(__file__).parent.parent.parent / "config.json"
        else:
            self.config_path = Path(config_path)

        # 确保配置文件目录存在
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # 当前配置
        self._config = self.DEFAULT_CONFIG.copy()

        # 加载配置
        self.load()

    @staticmethod
    def _is_frozen() -> bool:
        """
        检测是否为打包后的单文件EXE

        Returns:
            是否为打包模式
        """
        return getattr(sys, 'frozen', False)

    @staticmethod
    def _get_user_data_dir() -> Path:
        """
        获取用户数据目录（用于单文件EXE配置存储）

        Returns:
            用户数据目录路径
        """
        # Windows: %APPDATA%/PSDBatchProcessor
        if sys.platform == "win32":
            appdata = os.getenv("APPDATA")
            if appdata:
                return Path(appdata) / "PSDBatchProcessor"

        # Fallback: 使用程序所在目录
        return Path(__file__).parent.parent.parent

    def load(self) -> bool:
        """
        从文件加载配置

        Returns:
            是否成功加载
        """
        if not self.config_path.exists():
            print(f"[INFO] 配置文件不存在，使用默认配置: {self.config_path}")
            return False

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)

            # 合并配置（保留默认配置中不存在的键）
            self._config.update(loaded_config)
            print(f"[OK] 配置已加载: {self.config_path}")
            return True

        except json.JSONDecodeError as e:
            print(f"[ERROR] 配置文件格式错误: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] 加载配置失败: {e}")
            return False

    def save(self) -> bool:
        """
        保存配置到文件

        Returns:
            是否成功保存
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            print(f"[OK] 配置已保存: {self.config_path}")
            return True
        except Exception as e:
            print(f"[ERROR] 保存配置失败: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键名
            default: 默认值

        Returns:
            配置值
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        设置配置值

        Args:
            key: 配置键名
            value: 配置值
        """
        self._config[key] = value

    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.copy()

    # 属性访问器
    @property
    def photoshop_path(self) -> str:
        return self.get("photoshop_path", self.DEFAULT_CONFIG["photoshop_path"])

    @photoshop_path.setter
    def photoshop_path(self, value: str):
        self.set("photoshop_path", value)

    @property
    def script_dir(self) -> str:
        return self.get("script_dir", self.DEFAULT_CONFIG["script_dir"])

    @script_dir.setter
    def script_dir(self, value: str):
        self.set("script_dir", value)

    @property
    def backup_dir(self) -> str:
        return self.get("backup_dir", self.DEFAULT_CONFIG["backup_dir"])

    @backup_dir.setter
    def backup_dir(self, value: str):
        self.set("backup_dir", value)

    @property
    def last_script(self) -> str:
        return self.get("last_script", "")

    @last_script.setter
    def last_script(self, value: str):
        self.set("last_script", value)

    @property
    def max_workers(self) -> int:
        return self.get("max_workers", 1)

    @max_workers.setter
    def max_workers(self, value: int):
        self.set("max_workers", value)

    @property
    def theme(self) -> str:
        return self.get("theme", "dark")

    @theme.setter
    def theme(self, value: str):
        self.set("theme", value)

    @property
    def include_subfolders(self) -> bool:
        return self.get("include_subfolders", True)

    @include_subfolders.setter
    def include_subfolders(self, value: bool):
        self.set("include_subfolders", value)

    def validate_paths(self) -> tuple[bool, str]:
        """
        验证关键路径是否存在

        Returns:
            (是否有效, 错误信息)
        """
        # 检查 Photoshop 路径
        ps_path = Path(self.photoshop_path)
        if not ps_path.exists():
            return False, f"Photoshop 可执行文件不存在: {self.photoshop_path}"

        # 检查脚本目录（支持相对路径和绝对路径）
        script_dir = Path(self.script_dir)
        if not script_dir.is_absolute():
            # 如果是相对路径，尝试相对于程序目录
            if self._is_frozen():
                # 单文件EXE：相对于EXE所在目录
                script_dir = Path(sys.executable).parent / self.script_dir
            else:
                # 开发环境：相对于程序目录
                script_dir = Path(__file__).parent.parent.parent / self.script_dir

        if not script_dir.exists():
            return False, f"脚本目录不存在: {script_dir}"

        # 检查备份目录（不存在则创建）
        backup_dir = Path(self.backup_dir)
        if not backup_dir.is_absolute():
            # 如果是相对路径，尝试相对于程序目录
            if self._is_frozen():
                # 单文件EXE：相对于EXE所在目录
                backup_dir = Path(sys.executable).parent / self.backup_dir
            else:
                # 开发环境：相对于程序目录
                backup_dir = Path(__file__).parent.parent.parent / self.backup_dir

        if not backup_dir.exists():
            try:
                backup_dir.mkdir(parents=True, exist_ok=True)
                print(f"[INFO] 创建备份目录: {backup_dir}")
            except Exception as e:
                return False, f"无法创建备份目录: {e}"

        return True, "路径验证通过"

    def get_script_dir_path(self) -> Path:
        """
        获取脚本目录的完整路径（处理相对路径）

        Returns:
            脚本目录路径
        """
        script_dir = Path(self.script_dir)
        if script_dir.is_absolute():
            return script_dir

        # 相对路径处理
        if self._is_frozen():
            # 单文件EXE：相对于EXE所在目录
            return Path(sys.executable).parent / self.script_dir
        else:
            # 开发环境：相对于项目根目录（src/app/config的父目录的父目录的父目录）
            # src/app/config/settings.py -> src -> 项目根目录
            return Path(__file__).parent.parent.parent.parent / self.script_dir

    def get_backup_dir_path(self) -> Path:
        """
        获取备份目录的完整路径（处理相对路径）

        Returns:
            备份目录路径
        """
        backup_dir = Path(self.backup_dir)
        if backup_dir.is_absolute():
            return backup_dir

        # 相对路径处理
        if self._is_frozen():
            # 单文件EXE：相对于EXE所在目录
            return Path(sys.executable).parent / self.backup_dir
        else:
            # 开发环境：相对于项目根目录
            return Path(__file__).parent.parent.parent.parent / self.backup_dir

    def ensure_script_dir_exists(self) -> bool:
        """
        确保脚本目录存在（单文件EXE时从打包资源中提取脚本）

        Returns:
            是否成功创建/提取脚本
        """
        script_dir = self.get_script_dir_path()

        if script_dir.exists():
            return True

        try:
            script_dir.mkdir(parents=True, exist_ok=True)
            print(f"[INFO] 创建脚本目录: {script_dir}")

            # 如果是单文件EXE，尝试从打包资源中提取脚本
            if self._is_frozen():
                self._extract_scripts_to_dir(script_dir)

            return True
        except Exception as e:
            print(f"[ERROR] 无法创建脚本目录: {e}")
            return False

    def _extract_scripts_to_dir(self, target_dir: Path):
        """
        从打包资源中提取脚本文件到指定目录

        Args:
            target_dir: 目标目录
        """
        try:
            import sys
            if getattr(sys, 'frozen', False):
                # 单文件EXE模式
                # PyInstaller会将数据文件打包到 sys._MEIPASS
                bundle_dir = getattr(sys, '_MEIPASS', Path(__file__).parent)

                # 定义要提取的脚本目录
                script_dirs = ['scripts/production', 'scripts/templates', 'scripts/examples']

                for script_subdir in script_dirs:
                    source_dir = Path(bundle_dir) / script_subdir
                    dest_dir = target_dir / Path(script_subdir).name

                    if source_dir.exists():
                        dest_dir.mkdir(parents=True, exist_ok=True)

                        for file_path in source_dir.glob('*.jsx'):
                            dest_file = dest_dir / file_path.name
                            shutil.copy2(file_path, dest_file)
                            print(f"[INFO] 提取脚本: {file_path.name} -> {dest_file}")

        except Exception as e:
            print(f"[WARNING] 提取脚本失败: {e}")


# 全局配置实例
_settings = None


def get_settings() -> Settings:
    """获取全局配置实例"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def init_settings(config_path: Optional[str] = None) -> Settings:
    """初始化全局配置"""
    global _settings
    _settings = Settings(config_path)
    return _settings
