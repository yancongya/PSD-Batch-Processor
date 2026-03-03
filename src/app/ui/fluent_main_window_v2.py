"""
PyQt-Fluent-Widgets 版主窗口 V2
重新设计的 UI，功能分离更清晰
- 主页: 文件处理
- 脚本管理: 脚本浏览和管理
- 设置: 配置选项
- 日志: 日志查看
"""

import sys
from pathlib import Path
from typing import List, Optional

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QMimeData
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QFileDialog, QMessageBox, QTreeWidgetItem, QSplitter, QMenu, QAction,
                             QTreeWidget, QSizePolicy)
from PyQt5.QtGui import QDrag, QIcon
from qfluentwidgets import (
    FluentWindow, NavigationInterface, CardWidget, SubtitleLabel, BodyLabel,
    PrimaryPushButton, PushButton, LineEdit, ComboBox, SpinBox, CheckBox,
    TextEdit, TreeWidget, ProgressRing, InfoBar, InfoBarPosition, MessageBox,
    StrongBodyLabel, PrimaryToolButton, ToolButton, FluentIcon, NavigationItemPosition,
    TableWidget, HorizontalSeparator, VerticalSeparator, ScrollArea, setTheme, Theme,
    SearchLineEdit
)

from app.config.settings import get_settings, init_settings
from app.core.processor import BatchProcessor
from app.models.file_item import FileItem, FileStatus
from utils.logger import get_logger, init_logger


FILE_STATUS_ICON = {
    'pending': FluentIcon.PHOTO,
    'processing': FluentIcon.SYNC,
    'success': FluentIcon.ACCEPT,
    'error': FluentIcon.CANCEL,
}


class DroppableTreeWidget(TreeWidget):
    """支持拖放的树形控件"""
    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(False)
        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        self._normal_style = ""
        self._drag_style = ""

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._drag_style = """
                TreeWidget {
                    font-size: 12px;
                    border: 3px dashed #0078d7;
                    border-radius: 8px;
                    background-color: rgba(0, 120, 215, 0.08);
                }
            """
            self.setStyleSheet(self._drag_style)

    def dragLeaveEvent(self, event):
        self._restore_normal_style()

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path:
                files.append(path)
        
        if files:
            self.files_dropped.emit(files)
        
        self._restore_normal_style()

    def _restore_normal_style(self):
        """恢复正常样式"""
        self.setStyleSheet("""
            TreeWidget {
                font-size: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #fafafa;
                alternate-background-color: #f0f0f0;
            }
            TreeWidget::item {
                padding: 8px 10px;
                height: 32px;
                border-bottom: 1px solid #e8e8e8;
            }
            TreeWidget::item:hover {
                background-color: rgba(0, 120, 215, 0.1);
            }
            TreeWidget::item:selected {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0078d7, stop:1 #005a9e);
                color: white;
                border-radius: 0;
            }
        """)


class ProcessingThread(QThread):
    """处理线程 - 避免UI卡顿"""

    progress_signal = pyqtSignal(str, int, int, int)  # status, current, total, total_files
    log_signal = pyqtSignal(str, str)  # level, message
    finished_signal = pyqtSignal(bool, str, int, int)  # success, message, size_before, size_after

    def __init__(self, processor, files, script_path, settings, parent=None):
        super().__init__(parent)
        self.processor = processor
        self.files = files
        self.script_path = script_path
        self.settings = settings

    def run(self):
        """执行处理"""
        try:
            # 设置回调
            self.processor.set_callbacks(
                on_progress=self._on_progress,
                on_status_update=self._on_status_update,
                on_finished=self._on_finished  # 让callback触发finished_signal
            )

            # 将文件添加到处理器的文件列表
            self.processor.file_list.clear()
            for file_path in self.files:
                self.processor.file_list.add_file(file_path)

            # 执行批量处理 - 结果通过callback的_on_finished传递
            self.processor.process_batch(self.script_path)

        except Exception as e:
            self.log_signal.emit("error", f"处理异常: {str(e)}")
            self.finished_signal.emit(False, f"异常: {str(e)}", 0, 0)

    def _on_progress(self, current, total, message="", total_files=0):
        """进度回调"""
        self.progress_signal.emit(message, current, total, total_files)

    def _on_status_update(self, filename, status):
        """状态更新回调"""
        self.log_signal.emit("info", f"{filename}: {status}")

    def _on_finished(self, success, failed, elapsed, size_before=0, size_after=0):
        """完成回调"""
        if success > 0:
            self.finished_signal.emit(True, f"处理完成: 成功 {success} 个, 失败 {failed} 个, 耗时 {elapsed:.2f}s", size_before, size_after)
        else:
            self.finished_signal.emit(False, f"处理失败: 成功 {success} 个, 失败 {failed} 个, 耗时 {elapsed:.2f}s", size_before, size_after)


class FluentMainWindowV2(FluentWindow):
    """PyQt-Fluent-Widgets 主窗口 V2"""

    def __init__(self):
        super().__init__()

        # 初始化配置和日志
        self.settings = init_settings()
        self.logger = init_logger()

        # 批量处理器
        self.processor = BatchProcessor()

        # 数据存储
        self.file_list: List[str] = []
        self.script_path_map = {}  # 显示名 -> 完整路径

        # 处理线程
        self.processing_thread: Optional[ProcessingThread] = None

        # 窗口配置
        self.setWindowTitle("PSD Batch Processor - PSD 批量处理器")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)

        # 创建界面
        self._create_interfaces()
        self._setup_navigation()

        # 加载配置
        self._load_settings()

        # 确保目录存在
        self._ensure_directories()

        # 初始刷新脚本
        QTimer.singleShot(500, self._refresh_scripts)

        # 设置键盘快捷键
        self._setup_keyboard_shortcuts()


    def _setup_keyboard_shortcuts(self):
        """设置键盘快捷键"""
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QKeySequence

        # Ctrl+O: 添加文件
        self.process_interface.addAction(
            self._create_action("添加文件", self._add_files, "Ctrl+O")
        )

        # Ctrl+D: 添加文件夹
        self.process_interface.addAction(
            self._create_action("添加文件夹", self._add_folder, "Ctrl+D")
        )

        # Ctrl+Delete: 清空列表
        self.process_interface.addAction(
            self._create_action("清空列表", self._clear_files, "Ctrl+Delete")
        )

        # Ctrl+R: 开始处理
        self.process_interface.addAction(
            self._create_action("开始处理", self._start_processing, "Ctrl+R")
        )

        # Esc: 停止处理
        self.process_interface.addAction(
            self._create_action("停止处理", self._stop_processing, "Esc")
        )

        # F5: 刷新脚本
        self.process_interface.addAction(
            self._create_action("刷新脚本", self._refresh_scripts, "F5")
        )

    def _create_action(self, text, slot, shortcut):
        """创建带快捷键的动作"""
        from PyQt5.QtWidgets import QAction
        from PyQt5.QtGui import QKeySequence

        action = QAction(text, self)
        action.setShortcut(QKeySequence(shortcut))
        action.triggered.connect(slot)
        return action

    def _create_interfaces(self):
        """创建各个界面"""
        # 文件处理界面
        self.process_interface = QWidget()
        self.process_interface.setObjectName("ProcessInterface")
        self._setup_process_interface()

        # 脚本管理界面
        self.script_interface = QWidget()
        self.script_interface.setObjectName("ScriptInterface")
        self._setup_script_interface()

        # 设置界面
        self.settings_interface = QWidget()
        self.settings_interface.setObjectName("SettingsInterface")
        self._setup_settings_interface()

        # 日志界面
        self.log_interface = QWidget()
        self.log_interface.setObjectName("LogInterface")
        self._setup_log_interface()

    def _setup_navigation(self):
        """设置导航栏"""
        # 添加界面到导航
        self.addSubInterface(self.process_interface, FluentIcon.HOME, "文件处理")
        self.addSubInterface(self.script_interface, FluentIcon.CODE, "脚本管理")
        self.addSubInterface(self.settings_interface, FluentIcon.SETTING, "设置")
        self.addSubInterface(self.log_interface, FluentIcon.DOCUMENT, "日志")

    def _setup_process_interface(self):
        """设置文件处理界面 - 核心功能，文件列表为主"""
        # 使用自适应布局
        main_layout = QVBoxLayout(self.process_interface)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(12, 8, 12, 12)

        # 工具栏1 - 文件操作：搜索 + 添加 + 清空 + 统计
        toolbar1 = QHBoxLayout()
        toolbar1.setSpacing(8)

        # 搜索框（自适应缩放）
        self.file_search = SearchLineEdit()
        self.file_search.setPlaceholderText("搜索文件...")
        self.file_search.setFixedHeight(28)
        self.file_search.textChanged.connect(self._filter_files)
        self.file_search.setStyleSheet("SearchLineEdit { font-size: 12px; border-radius: 6px; }")
        toolbar1.addWidget(self.file_search, 1)

        # 添加文件
        add_file_btn = PushButton("添加文件")
        add_file_btn.setIcon(FluentIcon.DOCUMENT)
        add_file_btn.setFixedHeight(28)
        add_file_btn.setMinimumWidth(75)
        add_file_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_file_btn.setStyleSheet("PushButton { font-size: 12px; padding: 4px 12px; border-radius: 6px; }")
        add_file_btn.clicked.connect(self._add_files)
        add_file_btn.setToolTip("添加文件 (Ctrl+O)")
        toolbar1.addWidget(add_file_btn)

        # 添加文件夹
        add_folder_btn = PushButton("文件夹")
        add_folder_btn.setIcon(FluentIcon.FOLDER)
        add_folder_btn.setFixedHeight(28)
        add_folder_btn.setMinimumWidth(70)
        add_folder_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_folder_btn.setStyleSheet("PushButton { font-size: 12px; padding: 4px 12px; border-radius: 6px; }")
        add_folder_btn.clicked.connect(self._add_folder)
        add_folder_btn.setToolTip("添加文件夹 (Ctrl+D)")
        toolbar1.addWidget(add_folder_btn)

        # 清空
        clear_btn = PushButton("清空")
        clear_btn.setIcon(FluentIcon.DELETE)
        clear_btn.setFixedHeight(28)
        clear_btn.setMinimumWidth(60)
        clear_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        clear_btn.setStyleSheet("PushButton { font-size: 12px; padding: 4px 12px; border-radius: 6px; }")
        clear_btn.clicked.connect(self._clear_files)
        clear_btn.setToolTip("清空列表 (Ctrl+Delete)")
        toolbar1.addWidget(clear_btn)

        # 统计
        self.stats_label = BodyLabel("0 个文件")
        self.stats_label.setFixedHeight(28)
        self.stats_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stats_label.setStyleSheet("""
            BodyLabel {
                font-size: 12px;
                font-weight: 600;
                color: #0078d7;
                padding: 4px 12px;
                background-color: rgba(0, 120, 215, 0.1);
                border-radius: 6px;
            }
        """)
        toolbar1.addWidget(self.stats_label)

        main_layout.addLayout(toolbar1)

        # 工具栏2 - 处理操作：脚本 + 刷新 + 开始/停止 + 输出
        toolbar2 = QHBoxLayout()
        toolbar2.setSpacing(8)

        # 脚本选择（自适应缩放）
        self.script_combo = ComboBox()
        self.script_combo.setPlaceholderText("选择脚本...")
        self.script_combo.setFixedHeight(28)
        self.script_combo.setStyleSheet("ComboBox { font-size: 12px; padding: 4px 10px; border-radius: 6px; }")
        toolbar2.addWidget(self.script_combo, 1)

        # 刷新脚本
        refresh_btn = ToolButton()
        refresh_btn.setIcon(FluentIcon.SYNC)
        refresh_btn.setFixedSize(28, 28)
        refresh_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        refresh_btn.clicked.connect(self._refresh_scripts)
        refresh_btn.setToolTip("刷新脚本 (F5)")
        toolbar2.addWidget(refresh_btn)

        # 启动PS
        self.launch_ps_btn = PushButton("启动PS")
        self.launch_ps_btn.setIcon(FluentIcon.UPDATE)
        self.launch_ps_btn.setFixedHeight(28)
        self.launch_ps_btn.setMinimumWidth(70)
        self.launch_ps_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.launch_ps_btn.setStyleSheet("PushButton { font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 6px; }")
        self.launch_ps_btn.clicked.connect(self._launch_photoshop)
        self.launch_ps_btn.setToolTip("启动Photoshop并获取暂存盘信息")
        toolbar2.addWidget(self.launch_ps_btn)

        # 开始
        self.start_btn = PrimaryPushButton("开始处理")
        self.start_btn.setIcon(FluentIcon.PLAY)
        self.start_btn.setFixedHeight(28)
        self.start_btn.setMinimumWidth(80)
        self.start_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.start_btn.setStyleSheet("PrimaryPushButton { font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 6px; }")
        self.start_btn.clicked.connect(self._start_processing)
        self.start_btn.setToolTip("开始处理 (Ctrl+R)")
        toolbar2.addWidget(self.start_btn)

        # 停止
        self.stop_btn = PushButton("停止")
        self.stop_btn.setIcon(FluentIcon.PAUSE)
        self.stop_btn.setFixedHeight(28)
        self.stop_btn.setMinimumWidth(65)
        self.stop_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.stop_btn.setStyleSheet("PushButton { font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 6px; }")
        self.stop_btn.clicked.connect(self._stop_processing)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setToolTip("停止处理 (Esc)")
        toolbar2.addWidget(self.stop_btn)

        # 输出
        output_btn = PushButton("输出")
        output_btn.setIcon(FluentIcon.FOLDER)
        output_btn.setFixedHeight(28)
        output_btn.setMinimumWidth(60)
        output_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        output_btn.setStyleSheet("PushButton { font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 6px; }")
        output_btn.clicked.connect(self._open_output_folder)
        output_btn.setToolTip("打开备份文件夹")
        toolbar2.addWidget(output_btn)

        main_layout.addLayout(toolbar2)

        # 文件列表区域（占主要空间）
        file_card = self._create_file_card()
        main_layout.addWidget(file_card, 1)

        # 底部：进度显示区域
        progress_card = self._create_progress_card()
        main_layout.addWidget(progress_card)


    def _create_file_card(self):
        """创建文件列表卡片"""
        card = CardWidget()
        card.setStyleSheet("CardWidget { background-color: transparent; border: none; padding: 0px; }")
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)

        # 文件列表 - 拖放支持
        self.file_tree = DroppableTreeWidget()
        self.file_tree.setHeaderLabels(["文件名", "状态", "路径"])
        self.file_tree.setColumnWidth(0, 220)
        self.file_tree.setColumnWidth(1, 90)
        self.file_tree.setColumnWidth(2, 380)
        self.file_tree.setAlternatingRowColors(False)  # 禁用隔行变色
        self.file_tree.setStyleSheet("""
            TreeWidget {
                font-size: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #fafafa;
                gridline-color: #e0e0e0;
            }
            TreeWidget::header {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                border-radius: 6px 6px 0 0;
                font-weight: 600;
                color: #333;
            }
            TreeWidget::item {
                padding: 8px 10px;
                height: 32px;
                border-bottom: 1px solid #e8e8e8;
                background-color: #fafafa;
            }
            TreeWidget::item:hover {
                background-color: rgba(0, 120, 215, 0.1);
            }
            TreeWidget::item:selected {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0078d7, stop:1 #005a9e);
                color: white;
                border-radius: 0;
            }
            TreeWidget::item:selected:!active {
                background-color: #c7e0f4;
                color: #000;
            }
            TreeWidget::branch {
                background-color: transparent;
            }
        """)

        # 启用右键菜单
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self._show_file_context_menu)

        # 添加双击打开文件功能
        self.file_tree.itemDoubleClicked.connect(self._open_file_in_explorer)

        # 连接拖放信号
        self.file_tree.files_dropped.connect(self._handle_dropped_files)

        # 保存原始文件列表用于搜索过滤
        self._all_files = []

        layout.addWidget(self.file_tree)

        return card

    def _create_progress_card(self):
        """创建进度卡片 - 优化显示"""
        card = CardWidget()
        card.setStyleSheet("CardWidget { background-color: transparent; border: none; padding: 0px; }")
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # 进度条1 - 主进度条
        from PyQt5.QtWidgets import QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(28)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("等待开始... %p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                text-align: center;
                background-color: #fafafa;
                font-size: 12px;
                font-weight: 600;
                color: #333;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d7,
                    stop:0.5 #106ebe,
                    stop:1 #005a9e
                );
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # 进度条2 - 详细进度条（显示文件进度）
        self.progress_detail_bar = QProgressBar()
        self.progress_detail_bar.setMinimumHeight(20)
        self.progress_detail_bar.setMinimum(0)
        self.progress_detail_bar.setMaximum(100)
        self.progress_detail_bar.setValue(0)
        self.progress_detail_bar.setFormat("")
        self.progress_detail_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                text-align: center;
                background-color: #fafafa;
                font-size: 11px;
                color: #666;
            }
            QProgressBar::chunk {
                background-color: #6bcf7f;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_detail_bar)

        # 暂存盘信息 - 简化显示
        scratch_layout = QHBoxLayout()
        scratch_layout.setSpacing(10)
        
        self.scratch_progress_label = BodyLabel("暂存盘:")
        self.scratch_progress_label.setStyleSheet("BodyLabel { font-size: 11px; color: #666; font-weight: 600; }")
        scratch_layout.addWidget(self.scratch_progress_label)
        
        self.scratch_progress_bar = QProgressBar()
        self.scratch_progress_bar.setMinimumHeight(16)
        self.scratch_progress_bar.setMinimum(0)
        self.scratch_progress_bar.setMaximum(100)
        self.scratch_progress_bar.setValue(0)
        self.scratch_progress_bar.setFormat("")
        self.scratch_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                text-align: center;
                background-color: #fafafa;
                font-size: 10px;
                color: #666;
            }
            QProgressBar::chunk {
                background-color: #6bcf7f;
                border-radius: 3px;
            }
        """)
        scratch_layout.addWidget(self.scratch_progress_bar, 1)
        
        self.scratch_progress_text = BodyLabel("--")
        self.scratch_progress_text.setStyleSheet("BodyLabel { font-size: 11px; color: #888; }")
        scratch_layout.addWidget(self.scratch_progress_text)
        
        layout.addLayout(scratch_layout)

        return card

    def _setup_script_interface(self):
        """设置脚本管理界面"""
        # 使用滚动区域
        scroll = ScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = SubtitleLabel("📝 脚本管理")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # 脚本目录信息
        dir_card = self._create_script_dir_card()
        layout.addWidget(dir_card)

        # 脚本列表
        list_card = self._create_script_list_card()
        layout.addWidget(list_card)

        # 脚本说明
        info_card = self._create_script_info_card()
        layout.addWidget(info_card)

        layout.addStretch()
        scroll.setWidget(container)

        # 设置主布局
        main_layout = QVBoxLayout(self.script_interface)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _create_script_dir_card(self):
        """创建脚本目录卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        # 标题
        title = StrongBodyLabel("📂 脚本目录")
        layout.addWidget(title)

        # 目录路径
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(BodyLabel("当前目录:"))

        self.script_dir_display = BodyLabel("")
        self.script_dir_display.setStyleSheet("color: #666;")
        dir_layout.addWidget(self.script_dir_display)

        dir_layout.addStretch()
        layout.addLayout(dir_layout)

        # 操作按钮
        btn_layout = QHBoxLayout()

        refresh_btn = PushButton("刷新脚本列表")
        refresh_btn.setIcon(FluentIcon.SYNC)
        refresh_btn.clicked.connect(self._refresh_scripts)
        btn_layout.addWidget(refresh_btn)

        open_btn = PushButton("打开脚本目录")
        open_btn.setIcon(FluentIcon.FOLDER)
        open_btn.clicked.connect(self._open_script_dir)
        btn_layout.addWidget(open_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        return card

    def _create_script_list_card(self):
        """创建脚本列表卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # 标题
        title = StrongBodyLabel("📋 脚本列表")
        layout.addWidget(title)

        # 脚本列表 TreeWidget
        self.script_tree = TreeWidget()
        self.script_tree.setHeaderLabels(["脚本名称", "类型", "路径"])
        self.script_tree.setColumnWidth(0, 300)
        self.script_tree.setColumnWidth(1, 100)
        self.script_tree.setColumnWidth(2, 400)
        self.script_tree.setMinimumHeight(300)
        layout.addWidget(self.script_tree)

        # 统计信息
        self.script_stats_label = BodyLabel("就绪 - 0 个脚本")
        layout.addWidget(self.script_stats_label)

        return card

    def _create_script_info_card(self):
        """创建脚本说明卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        # 标题
        title = StrongBodyLabel("ℹ️ 脚本说明")
        layout.addWidget(title)

        # 说明文本
        info_text = BodyLabel("""
        • 脚本会自动扫描 scripts/ 目录及其子目录
        • 支持 .jsx 格式的 Photoshop 脚本
        • 脚本会自动处理确认对话框，实现无人值守运行
        • 在文件处理页面选择要执行的脚本
        """)
        info_text.setStyleSheet("color: #666; line-height: 1.5;")
        layout.addWidget(info_text)

        return card

    def _setup_settings_interface(self):
        """设置设置界面"""
        # 使用滚动区域
        scroll = ScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = SubtitleLabel("⚙️ 设置")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Photoshop 设置
        ps_card = self._create_photoshop_settings_card()
        layout.addWidget(ps_card)

        # 路径设置
        path_card = self._create_path_settings_card()
        layout.addWidget(path_card)

        # 主题设置
        theme_card = self._create_theme_settings_card()
        layout.addWidget(theme_card)

        # 保存按钮
        save_btn = PrimaryPushButton("保存设置")
        save_btn.setIcon(FluentIcon.SAVE)
        save_btn.setMinimumHeight(45)
        save_btn.setStyleSheet("font-size: 14px; font-weight: bold;")
        save_btn.clicked.connect(self._save_settings)
        layout.addWidget(save_btn)

        layout.addStretch()
        scroll.setWidget(container)

        # 设置主布局
        main_layout = QVBoxLayout(self.settings_interface)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _create_photoshop_settings_card(self):
        """创建 Photoshop 设置卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # 标题
        title = StrongBodyLabel("🎨 Photoshop 设置")
        layout.addWidget(title)

        # Photoshop 路径
        ps_layout = QHBoxLayout()
        ps_layout.addWidget(BodyLabel("Photoshop 路径:"))

        self.ps_path_edit = LineEdit()
        self.ps_path_edit.setPlaceholderText("选择 Photoshop.exe 路径")
        ps_layout.addWidget(self.ps_path_edit, 1)

        ps_browse_btn = PushButton("浏览...")
        ps_browse_btn.setIcon(FluentIcon.FOLDER)
        ps_browse_btn.clicked.connect(self._browse_photoshop_path)
        ps_layout.addWidget(ps_browse_btn)

        layout.addLayout(ps_layout)

        # 并发数
        worker_layout = QHBoxLayout()
        worker_layout.addWidget(BodyLabel("最大并发数:"))

        self.worker_spin_settings = SpinBox()
        self.worker_spin_settings.setRange(1, 8)
        self.worker_spin_settings.setValue(self.settings.max_workers)
        worker_layout.addWidget(self.worker_spin_settings)

        worker_layout.addStretch()
        layout.addLayout(worker_layout)

        # 缓存清理设置
        cache_layout = QHBoxLayout()
        cache_layout.addWidget(BodyLabel("缓存清理间隔:"))

        self.cache_clean_spin = SpinBox()
        self.cache_clean_spin.setRange(1, 20)
        self.cache_clean_spin.setValue(5)
        self.cache_clean_spin.setToolTip("每处理多少个文件后自动清理一次缓存")
        cache_layout.addWidget(self.cache_clean_spin)

        cache_label = BodyLabel("个文件清理一次")
        cache_label.setStyleSheet("color: #888;")
        cache_layout.addWidget(cache_label)

        cache_layout.addStretch()
        layout.addLayout(cache_layout)

        return card

    def _create_path_settings_card(self):
        """创建路径设置卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # 标题
        title = StrongBodyLabel("📂 路径设置")
        layout.addWidget(title)

        # 脚本目录
        script_dir_layout = QHBoxLayout()
        script_dir_layout.addWidget(BodyLabel("脚本目录:"))

        self.script_dir_edit = LineEdit()
        self.script_dir_edit.setText(self.settings.script_dir)
        script_dir_layout.addWidget(self.script_dir_edit, 1)

        script_dir_btn = PushButton("浏览...")
        script_dir_btn.clicked.connect(self._browse_script_dir)
        script_dir_layout.addWidget(script_dir_btn)

        layout.addLayout(script_dir_layout)

        # 备份目录
        backup_dir_layout = QHBoxLayout()
        backup_dir_layout.addWidget(BodyLabel("备份目录:"))

        self.backup_dir_edit = LineEdit()
        self.backup_dir_edit.setText(self.settings.backup_dir)
        backup_dir_layout.addWidget(self.backup_dir_edit, 1)

        backup_dir_btn = PushButton("浏览...")
        backup_dir_btn.clicked.connect(self._browse_backup_dir)
        backup_dir_layout.addWidget(backup_dir_btn)

        layout.addLayout(backup_dir_layout)

        return card

    def _create_theme_settings_card(self):
        """创建主题设置卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # 标题
        title = StrongBodyLabel("🎨 主题设置")
        layout.addWidget(title)

        # 主题选择
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(BodyLabel("外观主题:"))

        self.theme_combo = ComboBox()
        self.theme_combo.addItems(["深色", "浅色"])
        self.theme_combo.setCurrentText("深色" if self.settings.theme == "dark" else "浅色")
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        theme_layout.addWidget(self.theme_combo)

        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        return card

    def _setup_log_interface(self):
        """设置日志界面"""
        layout = QVBoxLayout(self.log_interface)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = SubtitleLabel("📋 处理日志")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # 控制按钮
        control_layout = QHBoxLayout()

        clear_btn = PushButton("清空日志")
        clear_btn.setIcon(FluentIcon.DELETE)
        clear_btn.clicked.connect(self._clear_log)
        control_layout.addWidget(clear_btn)

        save_btn = PushButton("保存日志")
        save_btn.setIcon(FluentIcon.SAVE)
        save_btn.clicked.connect(self._save_log)
        control_layout.addWidget(save_btn)

        control_layout.addStretch()
        layout.addLayout(control_layout)

        # 日志文本
        self.full_log_text = TextEdit()
        self.full_log_text.setReadOnly(True)
        self.full_log_text.setStyleSheet("""
            TextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, monospace;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.full_log_text)

    def _load_settings(self):
        """加载设置"""
        self.ps_path_edit.setText(self.settings.photoshop_path)
        self.worker_spin_settings.setValue(self.settings.max_workers)

        # 设置主题选择
        if self.settings.theme == "dark":
            self.theme_combo.setCurrentText("深色")
            self._set_dark_theme()
        else:
            self.theme_combo.setCurrentText("浅色")
            self._set_light_theme()

        # 应用主题到所有组件
        self._apply_theme_to_all_widgets()

        # 去掉顶部配置显示更新

        # 更新其他显示
        self.script_dir_display.setText(str(self.settings.get_script_dir_path()))

    def _ensure_directories(self):
        """确保目录存在"""
        try:
            # 确保脚本目录存在
            self.settings.ensure_script_dir_exists()

            # 确保备份目录存在
            backup_dir = self.settings.get_backup_dir_path()
            backup_dir.mkdir(parents=True, exist_ok=True)

            self._add_log("info", f"脚本目录: {self.settings.get_script_dir_path()}")
            self._add_log("info", f"备份目录: {backup_dir}")

            # 更新显示
            self.script_dir_display.setText(str(self.settings.get_script_dir_path()))

        except Exception as e:
            self._add_log("error", f"创建目录时出错: {e}")

    def _browse_photoshop_path(self):
        """浏览 Photoshop 路径"""
        path, _ = QFileDialog.getOpenFileName(
            self, "选择 Photoshop.exe",
            "C:/Program Files/Adobe",
            "Executable files (*.exe)"
        )
        if path:
            self.ps_path_edit.setText(path)
            self._add_log("info", f"Photoshop 路径已设置: {path}")

    def _refresh_scripts(self):
        """刷新脚本列表"""
        try:
            script_dir = self.settings.get_script_dir_path()

            if not script_dir.exists():
                self._show_warning("脚本目录不存在", f"目录不存在: {script_dir}")
                return

            # 递归扫描所有.jsx文件（包括子目录）
            jsx_files = list(script_dir.rglob("*.jsx"))

            if not jsx_files:
                self._show_warning("未找到脚本", "在脚本目录中未找到任何 .jsx 文件")
                return

            # 清空现有内容
            self.script_combo.clear()
            self.script_path_map.clear()
            self.script_tree.clear()

            # 创建相对路径显示，便于用户识别
            script_items = []
            for jsx_file in jsx_files:
                try:
                    # 计算相对于脚本目录的相对路径
                    rel_path = jsx_file.relative_to(script_dir)

                    # 如果在子目录中，显示为 "子目录/脚本名"
                    if rel_path.parent.name != ".":
                        display_name = str(rel_path)
                        script_type = str(rel_path.parent)
                    else:
                        display_name = rel_path.name
                        script_type = "根目录"

                    script_items.append({
                        'display': display_name,
                        'full_path': str(jsx_file),
                        'type': script_type
                    })

                except ValueError as e:
                    self._add_log("error", f"无法处理文件 {jsx_file}: {e}")

            # 按显示名称排序
            script_items.sort(key=lambda x: x['display'])

            # 添加到下拉框和树形列表
            for item in script_items:
                # 下拉框
                self.script_combo.addItem(item['display'], item['full_path'])
                self.script_path_map[item['display']] = item['full_path']

                # 树形列表
                tree_item = QTreeWidgetItem(self.script_tree)
                tree_item.setText(0, item['display'])
                tree_item.setText(1, item['type'])
                tree_item.setText(2, item['full_path'])
                tree_item.setIcon(0, FluentIcon.DOCUMENT.icon())

            # 更新统计
            self.script_stats_label.setText(f"找到 {len(script_items)} 个脚本")

            # 恢复上次选择的脚本
            if self.settings.last_script:
                index = self.script_combo.findText(self.settings.last_script)
                if index >= 0:
                    self.script_combo.setCurrentIndex(index)
                    self._add_log("info", f"已恢复上次选择的脚本: {self.settings.last_script}")

            self._add_log("info", f"找到 {len(script_items)} 个脚本文件")
            self._show_info("脚本刷新完成", f"找到 {len(script_items)} 个脚本")

        except Exception as e:
            self._add_log("error", f"刷新脚本时出错: {e}")
            self._show_error("错误", f"刷新脚本失败: {e}")

    def _open_script_dir(self):
        """打开脚本目录"""
        script_dir = self.settings.get_script_dir_path()
        if script_dir.exists():
            import os
            os.startfile(str(script_dir))
        else:
            self._show_warning("目录不存在", "脚本目录不存在")

    def _add_files(self):
        """添加文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择 PSD 文件",
            "",
            "PSD files (*.psd)"
        )

        if files:
            for file in files:
                if file not in self.file_list:
                    self.file_list.append(file)
                    self._add_file_to_tree(file)

            self._update_stats()
            self._add_log("info", f"添加了 {len(files)} 个文件")

    def _add_folder(self):
        """添加文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self, "选择文件夹"
        )

        if folder:
            self._add_folder_path(folder)

    def _add_folder_path(self, folder):
        """添加文件夹路径"""
        folder_path = Path(folder)
        psd_files = list(folder_path.rglob("*.psd"))

        if psd_files:
            for file in psd_files:
                if str(file) not in self.file_list:
                    self.file_list.append(str(file))
                    self._add_file_to_tree(str(file))

            self._update_stats()
            self._add_log("info", f"从文件夹添加了 {len(psd_files)} 个 PSD 文件")
        else:
            self._show_warning("未找到文件", "该文件夹中没有 PSD 文件")

    def _handle_dropped_files(self, file_paths):
        """处理拖放的文件"""
        added_count = 0
        for path in file_paths:
            path_obj = Path(path)
            if path_obj.is_dir():
                self._add_folder_path(path)
            elif path_obj.suffix.lower() == '.psd':
                if path not in self.file_list:
                    self.file_list.append(path)
                    self._add_file_to_tree(path)
                    added_count += 1
        
        if added_count > 0:
            self._update_stats()
            self._add_log("info", f"拖放添加了 {added_count} 个文件")
            self._show_info("文件已添加", f"成功添加 {added_count} 个文件")

    def _filter_files(self, text):
        """搜索过滤文件"""
        text = text.lower().strip()
        
        # 显示/隐藏匹配的行
        for i in range(self.file_tree.topLevelItemCount()):
            item = self.file_tree.topLevelItem(i)
            if not text:
                item.setHidden(False)
            else:
                file_name = item.text(0).lower()
                file_path = item.text(2).lower()
                item.setHidden(text not in file_name and text not in file_path)

    def _add_file_to_tree(self, file_path, status='pending'):
        """添加文件到树形列表"""
        path = Path(file_path)

        item = QTreeWidgetItem(self.file_tree)
        item.setText(0, path.name)
        item.setText(1, self._get_status_text(status))
        item.setText(2, str(path))
        item.setData(0, Qt.UserRole, {'path': str(path), 'status': status})
        item.setIcon(0, FILE_STATUS_ICON.get(status, FluentIcon.PHOTO).icon())

    def _get_status_text(self, status):
        """获取状态显示文本"""
        status_map = {
            'pending': '待处理',
            'processing': '处理中',
            'success': '成功',
            'error': '失败'
        }
        return status_map.get(status, '待处理')

    def _update_file_status(self, file_path, status):
        """更新文件状态"""
        for i in range(self.file_tree.topLevelItemCount()):
            item = self.file_tree.topLevelItem(i)
            data = item.data(0, Qt.UserRole)
            if data and data.get('path') == file_path:
                item.setText(1, self._get_status_text(status))
                item.setIcon(0, FILE_STATUS_ICON.get(status, FluentIcon.PHOTO).icon())
                data['status'] = status
                item.setData(0, Qt.UserRole, data)
                break

    def _show_file_context_menu(self, pos):
        """显示文件列表右键菜单"""
        item = self.file_tree.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)

        # 删除单个文件
        delete_action = QAction("删除此文件", self)
        delete_action.triggered.connect(lambda: self._delete_single_file(item))
        menu.addAction(delete_action)

        # 在文件资源管理器中显示
        show_action = QAction("在文件资源管理器中显示", self)
        show_action.triggered.connect(lambda: self._show_in_explorer(item))
        menu.addAction(show_action)

        menu.exec_(self.file_tree.mapToGlobal(pos))

    def _delete_single_file(self, item):
        """删除单个文件"""
        file_path = item.text(2)
        file_name = item.text(0)

        msg_box = MessageBox(
            "确认删除",
            f"确定要删除文件 '{file_name}' 吗？",
            self
        )
        reply = msg_box.exec()

        # qfluentwidgets 的 MessageBox 返回 True/False
        if reply:
            if file_path in self.file_list:
                self.file_list.remove(file_path)

            # 从树中移除
            index = self.file_tree.indexOfTopLevelItem(item)
            if index >= 0:
                self.file_tree.takeTopLevelItem(index)

            self._update_stats()
            self._add_log("info", f"已删除文件: {file_name}")

    def _open_file_in_explorer(self, item):
        """双击文件时在文件资源管理器中显示文件"""
        self._show_in_explorer(item)

    def _show_in_explorer(self, item):
        """在文件资源管理器中显示文件"""
        file_path = item.text(2)
        import os
        try:
            # 使用 explorer /select 参数高亮显示文件
            os.system(f'explorer /select,"{file_path}"')
        except Exception as e:
            self._show_error("打开失败", f"无法打开文件资源管理器: {e}")

    def _clear_files(self):
        """清空文件列表"""
        if not self.file_list:
            self._show_warning("列表为空", "文件列表已经是空的")
            return

        msg_box = MessageBox(
            "确认清空",
            f"确定要清空 {len(self.file_list)} 个文件吗？",
            self
        )
        reply = msg_box.exec()

        # qfluentwidgets 的 MessageBox 返回 True/False
        if reply:
            self.file_list.clear()
            self.file_tree.clear()
            self._update_stats()
            self._add_log("info", "文件列表已清空")

    def _update_stats(self):
        """更新统计信息"""
        total = len(self.file_list)
        self.stats_label.setText(f"{total} 个文件")

    def _launch_photoshop(self):
        """启动Photoshop并获取暂存盘信息"""
        photoshop_path = self.ps_path_edit.text()
        if not photoshop_path:
            self._show_warning("请设置 Photoshop 路径", "请先设置 Photoshop.exe 的路径")
            return

        if not Path(photoshop_path).exists():
            self._show_warning("Photoshop 路径无效", f"文件不存在: {photoshop_path}")
            return

        self._add_log("info", "正在启动 Photoshop...")
        
        # 尝试连接或启动Photoshop
        try:
            # 先尝试连接已运行的PS
            success, msg = self.processor.controller.connect(launch_if_needed=True)
            if success:
                self._add_log("success", f"Photoshop 已就绪: {msg}")
                
                # 测试基本连接
                try:
                    ps_name = self.processor.controller._photoshop.Name
                    self._add_log("info", f"Photoshop 版本: {ps_name}")
                except Exception as e:
                    self._add_log("warning", f"无法获取Photoshop名称: {e}")
                
                # 更新暂存盘信息
                self._update_scratch_disk_info()
                
                # 显示成功信息
                self._show_info("Photoshop 已启动", "Photoshop 已成功启动并连接")
            else:
                self._show_error("启动失败", f"无法启动 Photoshop: {msg}")
                self._add_log("error", f"启动 Photoshop 失败: {msg}")
        except Exception as e:
            self._show_error("启动失败", f"启动 Photoshop 时出错: {e}")
            self._add_log("error", f"启动 Photoshop 出错: {e}")

    def _update_scratch_disk_info(self):
        """更新暂存盘信息"""
        try:
            # 先检查是否已连接
            if not self.processor.controller.is_connected():
                self.scratch_progress_text.setText("未连接到 Photoshop")
                self.scratch_progress_bar.setValue(0)
                return
            
            success, info = self.processor.controller.get_scratch_disks_info()
            if success:
                self.logger.info(f"暂存盘信息: {info}")
                # 解析暂存盘信息，格式类似 "C:\: 45.2GB 可用 / 共 100.0GB (55%已用)"
                self.scratch_progress_text.setText(info)
                
                # 尝试提取百分比，格式是 "(55%已用)"
                import re
                match = re.search(r'\((\d+)%', info)
                if match:
                    percent = int(match.group(1))
                    self.scratch_progress_bar.setValue(percent)
                    
                    # 根据使用率设置颜色
                    if percent < 50:
                        color = "#6bcf7f"  # 绿色
                    elif percent < 80:
                        color = "#ffb84d"  # 橙色
                    else:
                        color = "#ff6b6b"  # 红色
                    
                    is_dark = self.settings.theme == "dark"
                    bg_color = "#252525" if is_dark else "#fafafa"
                    border_color = "#3d3d3d" if is_dark else "#e0e0e0"
                    
                    self.scratch_progress_bar.setStyleSheet(f"""
                        QProgressBar {{
                            border: 1px solid {border_color};
                            border-radius: 4px;
                            text-align: center;
                            background-color: {bg_color};
                            font-size: 10px;
                            color: #666;
                        }}
                        QProgressBar::chunk {{
                            background-color: {color};
                            border-radius: 3px;
                        }}
                    """)
                else:
                    # 如果无法提取百分比，显示默认值
                    self.scratch_progress_bar.setValue(0)
                    self.logger.warning(f"无法解析暂存盘百分比: {info}")
            else:
                self.scratch_progress_text.setText("无法获取暂存盘信息")
                self.scratch_progress_bar.setValue(0)
                self.logger.warning("获取暂存盘信息失败")
        except Exception as e:
            self.scratch_progress_text.setText(f"获取失败: {str(e)}")
            self.scratch_progress_bar.setValue(0)
            self.logger.error(f"更新暂存盘信息时出错: {e}")

    def _start_processing(self):
        """开始处理"""
        # 验证
        if not self.file_list:
            self._show_warning("请先添加文件", "请添加要处理的 PSD 文件")
            return

        photoshop_path = self.ps_path_edit.text()
        if not photoshop_path:
            self._show_warning("请设置 Photoshop 路径", "请先设置 Photoshop.exe 的路径")
            return

        if not Path(photoshop_path).exists():
            self._show_warning("Photoshop 路径无效", f"文件不存在: {photoshop_path}")
            return

        # 获取选中的脚本
        current_script = self.script_combo.currentText()
        if not current_script:
            self._show_warning("请选择脚本", "请先选择要执行的脚本")
            return

        script_path = self.script_path_map.get(current_script)
        if not script_path or not Path(script_path).exists():
            self._show_warning("脚本不存在", f"脚本文件不存在: {script_path}")
            return

        # 更新设置
        self.settings.photoshop_path = photoshop_path
        self.settings.last_script = current_script
        self.settings.save()

        # 保存当前脚本选择到配置，下次启动自动恢复
        self.settings.last_script = current_script
        self.settings.save()

        # 重置进度显示
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("准备开始... %p%")
        self.progress_detail_bar.setValue(0)
        self.progress_detail_bar.setFormat(f"共 {len(self.file_list)} 个文件待处理")

        # 禁用开始按钮，启用停止按钮
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        # 清空日志
        self.full_log_text.clear()

        self._add_log("info", f"开始处理 {len(self.file_list)} 个文件")
        self._add_log("info", f"使用脚本: {current_script}")
        self._add_log("info", f"并发数: {self.settings.max_workers}")

        # 创建并启动处理线程
        self.processing_thread = ProcessingThread(
            self.processor,
            self.file_list,
            script_path,
            self.settings,
            self
        )

        # 连接信号
        self.processing_thread.progress_signal.connect(self._on_progress_update)
        self.processing_thread.log_signal.connect(self._on_log_update)
        self.processing_thread.finished_signal.connect(self._on_processing_finished)

        # 启动线程
        self.processing_thread.start()

    def _stop_processing(self):
        """停止处理"""
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.terminate()
            self.processing_thread.wait()

            self._add_log("warning", "处理已手动停止")
            self._show_warning("已停止", "处理已手动停止")

            self._reset_processing_ui()

    def _on_progress_update(self, message, current, total, total_files):
        """进度更新 - 更新两个进度条
        
        Args:
            message: 进度消息
            current: 当前进度
            total: 当前阶段的总数（4表示文件阶段，total_files表示总体进度）
            total_files: 总文件数
        """
        # 每处理3个文件更新一次暂存盘信息
        if total == total_files and current % 3 == 0:
            self._update_scratch_disk_info()
        
        # 判断是总体进度还是单文件阶段
        is_file_stage = (total == 4 and total_files > 0)
        
        if is_file_stage:
            # 单文件处理阶段 (total=4)
            # current: 0=打开, 1=执行脚本, 2=保存, 3=完成
            # 需要知道当前是第几个文件
            # 从消息中提取文件名
            file_name = ""
            if " - " in message:
                file_name = message.split(" - ")[0]
            
            # 找到当前文件在列表中的索引
            current_file_index = -1
            if file_name:
                for i, f in enumerate(self.file_list):
                    if file_name in f:
                        current_file_index = i
                        break
            
            if current_file_index >= 0:
                # 计算总体进度：已完成文件数 + 当前文件的阶段进度
                completed_files = current_file_index
                stage_percent = (current + 1) * 25  # 25%, 50%, 75%, 100%
                overall_percent = int((completed_files + stage_percent / 100) / total_files * 100)
                
                # 主进度条 - 显示总体进度
                self.progress_bar.setValue(overall_percent)
                self.progress_bar.setFormat(f"总进度: {current_file_index + 1}/{total_files} ({overall_percent}%)")
                
                # 详细进度条 - 显示当前文件的处理阶段
                self.progress_detail_bar.setValue(stage_percent)
                self.progress_detail_bar.setFormat(f"当前文件: {message}")
                
                # 更新当前处理文件的状态
                try:
                    current_file = self.file_list[current_file_index]
                    if current_file:
                        self._update_file_status(current_file, 'processing')
                except:
                    pass
                
                # 根据主题调整进度条颜色
                self._update_progress_bar_style(overall_percent)
            else:
                # 无法确定文件索引，显示基本信息
                self.progress_detail_bar.setValue((current + 1) * 25)
                self.progress_detail_bar.setFormat(f"当前文件: {message}")
                
        elif total > 0 and total == total_files:
            # 总体进度（文件级别的）
            percent = int((current / total) * 100)
            
            # 主进度条 - 显示总体进度
            self.progress_bar.setValue(percent)
            self.progress_bar.setFormat(f"总进度: {current}/{total} ({percent}%)")
            
            # 详细进度条 - 显示当前文件处理状态
            self.progress_detail_bar.setValue(100)
            self.progress_detail_bar.setFormat(f"当前文件: {message}")
            
            # 更新当前处理文件的状态
            if message and current <= len(self.file_list):
                try:
                    current_file = self.file_list[current - 1] if current > 0 else ""
                    if current_file:
                        self._update_file_status(current_file, 'processing')
                except:
                    pass
            
            # 根据主题调整进度条颜色
            self._update_progress_bar_style(percent)
        else:
            # 未知进度的情况
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat(f"{message} - 处理中...")
            self.progress_detail_bar.setValue(50)
            self.progress_detail_bar.setFormat("处理中...")

    def _update_progress_bar_style(self, percent):
        """根据进度和主题更新进度条样式"""
        is_dark = self.settings.theme == "dark"
        
        # 根据进度选择颜色（更柔和的配色）
        if percent < 30:
            color = "#ffb84d"  # 橙色 - 警告色
        elif percent < 70:
            color = "#ffd93d"  # 黄色 - 进行中
        else:
            color = "#6bcf7f"  # 绿色 - 完成
        
        # 背景色根据主题调整
        bg_color = "#252525" if is_dark else "#fafafa"
        text_color = "#d4d4d4" if is_dark else "#333"
        border_color = "#3d3d3d" if is_dark else "#e0e0e0"
        
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {border_color};
                border-radius: 8px;
                text-align: center;
                background-color: {bg_color};
                font-size: 12px;
                font-weight: 600;
                color: {text_color};
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 6px;
            }}
        """)

    def _on_log_update(self, level, message):
        """日志更新"""
        self._add_log(level, message)

    def _on_processing_finished(self, success, message, size_before=0, size_after=0):
        """处理完成"""
        # 更新所有文件状态为完成
        for file_path in self.file_list:
            status = 'success' if success else 'error'
            self._update_file_status(file_path, status)
        
        if success:
            self._add_log("success", f"处理完成: {message}")
            
            # 显示总结弹窗
            self._show_summary_dialog(size_before, size_after, message)
            
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                    text-align: center;
                    background-color: #fafafa;
                    font-size: 11px;
                    font-weight: 600;
                    color: #333;
                }
                QProgressBar::chunk {
                    background-color: #6bcf7f;
                    border-radius: 5px;
                }
            """)
        else:
            self._add_log("error", f"处理失败: {message}")
            self._show_error("处理失败", message)
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                    text-align: center;
                    background-color: #fafafa;
                    font-size: 11px;
                    font-weight: 600;
                    color: #333;
                }
                QProgressBar::chunk {
                    background-color: #ff6b6b;
                    border-radius: 5px;
                }
            """)

        self._reset_processing_ui()

    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

    def _show_summary_dialog(self, size_before, size_after, message):
        """显示处理总结弹窗"""
        size_before_str = self._format_size(size_before)
        size_after_str = self._format_size(size_after)
        
        size_diff = size_after - size_before
        if size_diff > 0:
            size_change = f"+{self._format_size(size_diff)} ↑"
            color = "#ff6b6b"
        elif size_diff < 0:
            size_change = f"{self._format_size(abs(size_diff))} ↓"
            color = "#6bcf7f"
        else:
            size_change = "无变化"
            color = "#888"

        summary = f"""
        处理结果: {message}
        
        📊 文件大小统计:
        • 处理前: {size_before_str}
        • 处理后: {size_after_str}
        • 大小变化: <span style='color:{color}'>{size_change}</span>
        """

        from qfluentwidgets import Dialog, MessageBox

        dialog = MessageBox(
            "处理完成 - 总结报告",
            summary.strip(),
            self
        )
        dialog.exec()

    def _reset_processing_ui(self):
        """重置处理UI"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        # 重置进度显示
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("等待开始... %p%")
        self.progress_detail_bar.setValue(0)
        self.progress_detail_bar.setFormat("")

    def _open_output_folder(self):
        """打开输出文件夹"""
        backup_dir = self.settings.get_backup_dir_path()
        if backup_dir.exists():
            import os
            os.startfile(str(backup_dir))
        else:
            self._show_warning("文件夹不存在", "备份文件夹不存在")

    def _on_theme_changed(self, theme):
        """主题改变"""
        if theme == "深色":
            self._set_dark_theme()
        else:
            self._set_light_theme()

        # 保存设置
        self.settings.theme = "dark" if theme == "深色" else "light"
        self.settings.save()

        # 实时应用主题到主窗口和所有子组件
        self._apply_theme_to_all_widgets()

    def _set_dark_theme(self):
        """设置深色主题"""
        setTheme(Theme.DARK)

    def _set_light_theme(self):
        """设置浅色主题"""
        setTheme(Theme.LIGHT)

    def _apply_theme_to_all_widgets(self):
        """应用主题到所有组件 - 优化视觉反馈"""
        from PyQt5.QtWidgets import QApplication

        # 获取应用实例
        app = QApplication.instance()
        if not app:
            return

        # 根据当前主题设置样式
        if self.settings.theme == "dark":
            # 深色主题样式 - 现代化配色
            dark_stylesheet = """
            /* 基础组件样式 */
            QWidget {
                background-color: #202020;
                color: #e0e0e0;
                font-family: 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', sans-serif;
            }

            /* 卡片样式 */
            CardWidget {
                background-color: #2d2d2d;
                border-radius: 10px;
                border: 1px solid #404040;
                padding: 16px;
            }
            CardWidget:hover {
                border: 1px solid #0078d7;
                box-shadow: 0 2px 8px rgba(0, 120, 215, 0.2);
            }

            /* 标签样式 */
            SubtitleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #ffffff;
                letter-spacing: 0.5px;
            }
            StrongBodyLabel {
                font-size: 15px;
                font-weight: 600;
                color: #ffffff;
            }
            BodyLabel {
                font-size: 12px;
                color: #e0e0e0;
            }

            /* 按钮样式 */
            PrimaryPushButton {
                font-size: 13px;
                font-weight: 600;
                padding: 10px 18px;
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0078d7, stop:1 #005a9e);
                color: white;
                border: none;
            }
            PrimaryPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #106ebe, stop:1 #004578);
            }
            PrimaryPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #005a9e, stop:1 #003d5a);
            }
            PrimaryPushButton:disabled {
                background: #3a3a3a;
                color: #666;
            }

            PushButton {
                font-size: 13px;
                padding: 10px 18px;
                border-radius: 8px;
                border: 1px solid #404040;
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            PushButton:hover {
                background-color: #3d3d3d;
                border-color: #0078d7;
            }
            PushButton:pressed {
                background-color: #4d4d4d;
            }
            PushButton:disabled {
                border-color: #2d2d2d;
                color: #666;
                background-color: #252525;
            }

            /* 输入框样式 */
            LineEdit {
                font-size: 12px;
                padding: 8px 12px;
                border-radius: 8px;
                border: 1px solid #404040;
                background-color: #252525;
                color: #e0e0e0;
                selection-background-color: #0078d7;
            }
            LineEdit:focus {
                border: 2px solid #0078d7;
            }

            /* 组合框样式 */
            ComboBox {
                font-size: 12px;
                padding: 8px 12px;
                border-radius: 8px;
                border: 1px solid #404040;
                background-color: #252525;
                color: #e0e0e0;
            }
            ComboBox:hover {
                border: 1px solid #0078d7;
            }
            ComboBox::drop-down {
                border: none;
            }

            /* 数字输入框样式 */
            SpinBox {
                font-size: 12px;
                padding: 6px 10px;
                border-radius: 8px;
                border: 1px solid #404040;
                background-color: #252525;
                color: #e0e0e0;
            }
            SpinBox:focus {
                border: 2px solid #0078d7;
            }

            /* 树形列表样式 */
            TreeWidget {
                background-color: #252525;
                border: 2px solid #404040;
                border-radius: 10px;
                font-size: 12px;
                gridline-color: #404040;
            }
            TreeWidget::header {
                background-color: #2d2d2d;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #404040;
                border-radius: 8px 8px 0 0;
                font-weight: 600;
                color: #ffffff;
            }
            TreeWidget::item {
                padding: 8px 12px;
                height: 34px;
                border-bottom: 1px solid #353535;
                background-color: #252525;
            }
            TreeWidget::item:hover {
                background-color: #3d3d3d;
            }
            TreeWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0078d7, stop:1 #005a9e);
                color: white;
                border-radius: 0;
            }
            TreeWidget::item:selected:!active {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }

            /* 文本编辑器样式 */
            TextEdit {
                background-color: #1a1a1a;
                border: 2px solid #404040;
                border-radius: 10px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                color: #e0e0e0;
            }

            /* 进度条样式 */
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 10px;
                text-align: center;
                background-color: #252525;
                font-size: 12px;
                font-weight: 600;
                color: #e0e0e0;
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d7,
                    stop:0.5 #106ebe,
                    stop:1 #005a9e
                );
                border-radius: 8px;
            }

            /* 滚动区域 */
            QScrollArea {
                border: none;
            }

            /* 分隔线 */
            QFrame {
                border: 1px solid #404040;
            }
            """
            app.setStyleSheet(dark_stylesheet)
        else:
            # 浅色主题样式 - 现代化配色
            light_stylesheet = """
            /* 基础组件样式 */
            QWidget {
                background-color: #f5f7fa;
                color: #2c3e50;
                font-family: 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', sans-serif;
            }

            /* 卡片样式 */
            CardWidget {
                background-color: #ffffff;
                border-radius: 10px;
                border: 1px solid #e8eaed;
                padding: 16px;
            }
            CardWidget:hover {
                border: 1px solid #0078d7;
                box-shadow: 0 2px 12px rgba(0, 120, 215, 0.15);
            }

            /* 标签样式 */
            SubtitleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1a1a1a;
                letter-spacing: 0.5px;
            }
            StrongBodyLabel {
                font-size: 15px;
                font-weight: 600;
                color: #1a1a1a;
            }
            BodyLabel {
                font-size: 12px;
                color: #4a4a4a;
            }

            /* 按钮样式 */
            PrimaryPushButton {
                font-size: 13px;
                font-weight: 600;
                padding: 10px 18px;
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0078d7, stop:1 #005a9e);
                color: white;
                border: none;
            }
            PrimaryPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #106ebe, stop:1 #004578);
            }
            PrimaryPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #005a9e, stop:1 #003d5a);
            }
            PrimaryPushButton:disabled {
                background: #d0d0d0;
                color: #888;
            }

            PushButton {
                font-size: 13px;
                padding: 10px 18px;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #2c3e50;
            }
            PushButton:hover {
                background-color: #f8f9fa;
                border-color: #0078d7;
            }
            PushButton:pressed {
                background-color: #e9ecef;
            }
            PushButton:disabled {
                border-color: #e0e0e0;
                color: #999;
                background-color: #f5f5f5;
            }

            /* 输入框样式 */
            LineEdit {
                font-size: 12px;
                padding: 8px 12px;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #2c3e50;
                selection-background-color: #0078d7;
            }
            LineEdit:focus {
                border: 2px solid #0078d7;
            }

            /* 组合框样式 */
            ComboBox {
                font-size: 12px;
                padding: 8px 12px;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #2c3e50;
            }
            ComboBox:hover {
                border: 1px solid #0078d7;
            }
            ComboBox::drop-down {
                border: none;
            }

            /* 数字输入框样式 */
            SpinBox {
                font-size: 12px;
                padding: 6px 10px;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #2c3e50;
            }
            SpinBox:focus {
                border: 2px solid #0078d7;
            }

            /* 树形列表样式 */
            TreeWidget {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 12px;
                gridline-color: #e8eaed;
            }
            TreeWidget::header {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                border-radius: 8px 8px 0 0;
                font-weight: 600;
                color: #1a1a1a;
            }
            TreeWidget::item {
                padding: 8px 12px;
                height: 34px;
                border-bottom: 1px solid #f0f0f0;
                background-color: #ffffff;
            }
            TreeWidget::item:hover {
                background-color: #f8f9fa;
            }
            TreeWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0078d7, stop:1 #005a9e);
                color: white;
                border-radius: 0;
            }
            TreeWidget::item:selected:!active {
                background-color: #c7e0f4;
                color: #000;
            }

            /* 文本编辑器样式 */
            TextEdit {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                color: #2c3e50;
            }

            /* 进度条样式 */
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                text-align: center;
                background-color: #fafafa;
                font-size: 12px;
                font-weight: 600;
                color: #2c3e50;
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d7,
                    stop:0.5 #106ebe,
                    stop:1 #005a9e
                );
                border-radius: 8px;
            }

            /* 滚动区域 */
            QScrollArea {
                border: none;
            }

            /* 分隔线 */
            QFrame {
                border: 1px solid #e0e0e0;
            }
            """
            app.setStyleSheet(light_stylesheet)

    def _browse_script_dir(self):
        """浏览脚本目录"""
        folder = QFileDialog.getExistingDirectory(
            self, "选择脚本目录",
            self.script_dir_edit.text()
        )
        if folder:
            self.script_dir_edit.setText(folder)

    def _browse_backup_dir(self):
        """浏览备份目录"""
        folder = QFileDialog.getExistingDirectory(
            self, "选择备份目录",
            self.backup_dir_edit.text()
        )
        if folder:
            self.backup_dir_edit.setText(folder)

    def _save_settings(self):
        """保存设置"""
        self.settings.script_dir = self.script_dir_edit.text()
        self.settings.backup_dir = self.backup_dir_edit.text()
        self.settings.max_workers = self.worker_spin_settings.value()

        # 更新处理器的缓存清理间隔
        self.processor.cache_clean_interval = self.cache_clean_spin.value()

        if self.settings.save():
            self._show_info("设置已保存", f"设置已成功保存\n缓存清理间隔: 每 {self.cache_clean_spin.value()} 个文件")
            self._add_log("info", f"设置已保存 - 缓存清理间隔: 每 {self.cache_clean_spin.value()} 个文件")
        else:
            self._show_error("保存失败", "设置保存失败")

    def _clear_log(self):
        """清空日志"""
        self.full_log_text.clear()
        self._add_log("info", "日志已清空")

    def _save_log(self):
        """保存日志"""
        content = self.full_log_text.toPlainText()
        if not content:
            self._show_warning("无日志内容", "没有日志可以保存")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "保存日志",
            f"psd_processor_log_{self._get_timestamp()}.txt",
            "Text files (*.txt)"
        )

        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self._show_info("日志已保存", f"日志已保存到: {path}")
            except Exception as e:
                self._show_error("保存失败", f"保存日志失败: {e}")

    def _add_log(self, level, message):
        """添加日志"""
        timestamp = self._get_timestamp()
        log_line = f"[{timestamp}] [{level.upper()}] {message}"

        # 添加到完整日志
        self.full_log_text.append(log_line)

        # 滚动到底部
        self.full_log_text.verticalScrollBar().setValue(
            self.full_log_text.verticalScrollBar().maximum()
        )

    def _get_timestamp(self):
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _show_info(self, title, content):
        """显示信息"""
        InfoBar.info(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            position=InfoBarPosition.TOP,
            parent=self,
            duration=3000
        )

    def _show_warning(self, title, content):
        """显示警告"""
        InfoBar.warning(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            position=InfoBarPosition.TOP,
            parent=self,
            duration=4000
        )

    def _show_error(self, title, content):
        """显示错误"""
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            position=InfoBarPosition.TOP,
            parent=self,
            duration=5000
        )


def main():
    """主函数"""
    # 设置高DPI支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # 设置应用名称和组织
    app.setApplicationName("PSD Batch Processor")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("PSD Processor")

    # 创建并显示主窗口
    window = FluentMainWindowV2()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()