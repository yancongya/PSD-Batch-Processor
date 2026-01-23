"""
文件项数据模型
表示单个待处理的 PSD 文件及其状态
"""

from pathlib import Path
from typing import Optional
from enum import Enum


class FileStatus(Enum):
    """文件处理状态"""
    PENDING = "待处理"
    BACKUP_COMPLETED = "备份完成"
    PROCESSING = "处理中"
    SUCCESS = "成功"
    FAILED = "失败"


class FileItem:
    """文件项类"""

    def __init__(self, file_path: str):
        """
        初始化文件项

        Args:
            file_path: PSD 文件完整路径
        """
        self.path = Path(file_path)
        self.status = FileStatus.PENDING
        self.backup_path: Optional[Path] = None
        self.error_message: Optional[str] = None
        self.process_time: Optional[float] = None  # 处理耗时（秒）

    @property
    def file_name(self) -> str:
        """获取文件名"""
        return self.path.name

    @property
    def full_path(self) -> str:
        """获取完整路径"""
        return str(self.path.resolve())

    @property
    def status_text(self) -> str:
        """获取状态文本"""
        return self.status.value

    @property
    def size(self) -> int:
        """获取文件大小（字节）"""
        return self.path.stat().st_size if self.path.exists() else 0

    @property
    def size_mb(self) -> float:
        """获取文件大小（MB）"""
        return self.size / (1024 * 1024)

    def set_status(self, status: FileStatus, error_msg: Optional[str] = None):
        """
        设置文件状态

        Args:
            status: 状态
            error_msg: 错误信息（仅在失败时）
        """
        self.status = status
        if error_msg:
            self.error_message = error_msg

    def set_backup_path(self, backup_path: Path):
        """设置备份路径"""
        self.backup_path = backup_path

    def to_dict(self) -> dict:
        """转换为字典（用于 UI 显示）"""
        return {
            "file_name": self.file_name,
            "full_path": self.full_path,
            "status": self.status_text,
            "size_mb": f"{self.size_mb:.2f} MB",
            "error": self.error_message or "",
        }

    def __repr__(self) -> str:
        return f"FileItem(path='{self.file_name}', status='{self.status_text}')"


class FileList:
    """文件列表管理类"""

    def __init__(self):
        self._items: list[FileItem] = []

    def add_file(self, file_path: str) -> Optional[FileItem]:
        """
        添加文件

        Args:
            file_path: 文件路径

        Returns:
            添加的 FileItem，如果已存在则返回 None
        """
        path = Path(file_path)

        # 检查是否已存在
        for item in self._items:
            if item.path.resolve() == path.resolve():
                return None

        item = FileItem(file_path)
        self._items.append(item)
        return item

    def add_files(self, file_paths: list[str]) -> list[FileItem]:
        """
        批量添加文件

        Args:
            file_paths: 文件路径列表

        Returns:
            添加的 FileItem 列表
        """
        added = []
        for path in file_paths:
            item = self.add_file(path)
            if item:
                added.append(item)
        return added

    def add_folder(self, folder_path: str, recursive: bool = True) -> list[FileItem]:
        """
        添加文件夹中的所有 PSD 文件

        Args:
            folder_path: 文件夹路径
            recursive: 是否递归扫描子文件夹

        Returns:
            添加的 FileItem 列表
        """
        folder = Path(folder_path)
        if not folder.is_dir():
            return []

        pattern = "**/*.psd" if recursive else "*.psd"
        psd_files = list(folder.glob(pattern))

        added = []
        for psd_file in psd_files:
            item = self.add_file(str(psd_file))
            if item:
                added.append(item)

        return added

    def remove_file(self, file_path: str) -> bool:
        """
        移除文件

        Args:
            file_path: 文件路径

        Returns:
            是否成功移除
        """
        path = Path(file_path).resolve()
        for i, item in enumerate(self._items):
            if item.path.resolve() == path:
                self._items.pop(i)
                return True
        return False

    def remove_item(self, item: FileItem) -> bool:
        """
        移除文件项

        Args:
            item: 文件项

        Returns:
            是否成功移除
        """
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def clear(self):
        """清空所有文件"""
        self._items.clear()

    def get_all(self) -> list[FileItem]:
        """获取所有文件项"""
        return self._items.copy()

    def get_pending(self) -> list[FileItem]:
        """获取待处理的文件"""
        return [item for item in self._items if item.status == FileStatus.PENDING]

    def get_by_index(self, index: int) -> Optional[FileItem]:
        """
        通过索引获取文件项

        Args:
            index: 索引

        Returns:
            FileItem 或 None
        """
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def count(self) -> int:
        """获取文件总数"""
        return len(self._items)

    def count_pending(self) -> int:
        """获取待处理文件数"""
        return len(self.get_pending())

    def count_success(self) -> int:
        """获取成功文件数"""
        return sum(1 for item in self._items if item.status == FileStatus.SUCCESS)

    def count_failed(self) -> int:
        """获取失败文件数"""
        return sum(1 for item in self._items if item.status == FileStatus.FAILED)

    def update_status(self, file_path: str, status: FileStatus, error_msg: Optional[str] = None):
        """
        更新文件状态

        Args:
            file_path: 文件路径
            status: 新状态
            error_msg: 错误信息
        """
        path = Path(file_path).resolve()
        for item in self._items:
            if item.path.resolve() == path:
                item.set_status(status, error_msg)
                break

    def __repr__(self) -> str:
        return f"FileList(count={self.count()})"
