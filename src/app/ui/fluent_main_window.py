"""
PyQt-Fluent-Widgets 版主窗口
现代化 Fluent Design 风格的 PSD 批量处理器界面
"""

import sys
from pathlib import Path
from typing import List, Optional

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QTreeWidgetItem
from qfluentwidgets import (
    FluentWindow, NavigationInterface, CardWidget, SubtitleLabel,
    PrimaryPushButton, PushButton, LineEdit, ComboBox, SpinBox,
    TextEdit, TreeWidget, ProgressRing, InfoBar,
    InfoBarPosition, MessageBox, StrongBodyLabel, BodyLabel,
    PrimaryToolButton, ToolButton, FluentIcon, NavigationItemPosition
)

from app.config.settings import get_settings, init_settings
from app.core.processor import BatchProcessor
from app.models.file_item import FileItem, FileStatus
from utils.logger import get_logger, init_logger


class ProcessingThread(QThread):
    """处理线程 - 避免UI卡顿"""

    progress_signal = pyqtSignal(str, int, int)  # status, current, total
    log_signal = pyqtSignal(str, str)  # level, message
    finished_signal = pyqtSignal(bool, str)  # success, message

    def __init__(self, processor, files, script_path, parent=None):
        super().__init__(parent)
        self.processor = processor
        self.files = files
        self.script_path = script_path

    def run(self):
        """执行处理"""
        try:
            # 设置回调
            self.processor.set_callbacks(
                on_progress=self._on_progress,
                on_status_update=self._on_status_update,
                on_finished=self._on_finished
            )

            # 执行批量处理
            success = self.processor.process_batch(self.files, self.script_path)

            if success:
                self.finished_signal.emit(True, "处理完成")
            else:
                self.finished_signal.emit(False, "处理失败")

        except Exception as e:
            self.log_signal.emit("error", f"处理异常: {str(e)}")
            self.finished_signal.emit(False, f"异常: {str(e)}")

    def _on_progress(self, current, total, message=""):
        """进度回调"""
        self.progress_signal.emit(message, current, total)

    def _on_status_update(self, filename, status):
        """状态更新回调"""
        self.log_signal.emit("info", f"{filename}: {status}")

    def _on_finished(self, success, message):
        """完成回调"""
        self.finished_signal.emit(success, message)


class FluentMainWindow(FluentWindow):
    """PyQt-Fluent-Widgets 主窗口"""

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

    def _create_interfaces(self):
        """创建各个界面"""
        # 主页界面
        self.home_interface = QWidget()
        self.home_interface.setObjectName("HomeInterface")
        self._setup_home_interface()

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
        self.addSubInterface(self.home_interface, FluentIcon.HOME, "主页")
        self.addSubInterface(self.settings_interface, FluentIcon.SETTING, "设置")
        self.addSubInterface(self.log_interface, FluentIcon.DOCUMENT, "日志")

    def _setup_home_interface(self):
        """设置主页界面"""
        layout = QVBoxLayout(self.home_interface)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = SubtitleLabel("PSD 批量处理器")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # 设置卡片
        layout.addWidget(self._create_settings_card())

        # 文件列表卡片
        layout.addWidget(self._create_file_list_card())

        # 控制按钮
        layout.addWidget(self._create_control_buttons())

        # 进度显示
        layout.addWidget(self._create_progress_card())

        # 日志预览
        layout.addWidget(self._create_log_preview())

        layout.addStretch()

    def _create_settings_card(self):
        """创建设置卡片"""
        card = CardWidget()
        card.setMinimumHeight(150)
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # 标题
        title = StrongBodyLabel("⚙️ 设置")
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

        # 脚本选择
        script_layout = QHBoxLayout()
        script_layout.addWidget(BodyLabel("选择脚本:"))

        self.script_combo = ComboBox()
        self.script_combo.setPlaceholderText("选择要执行的脚本")
        script_layout.addWidget(self.script_combo, 1)

        refresh_btn = PushButton("刷新")
        refresh_btn.setIcon(FluentIcon.SYNC)
        refresh_btn.clicked.connect(self._refresh_scripts)
        script_layout.addWidget(refresh_btn)

        layout.addLayout(script_layout)

        # 并发数设置
        worker_layout = QHBoxLayout()
        worker_layout.addWidget(BodyLabel("并发数:"))

        self.worker_spin = SpinBox()
        self.worker_spin.setRange(1, 8)
        self.worker_spin.setValue(self.settings.max_workers)
        worker_layout.addWidget(self.worker_spin)

        worker_layout.addStretch()
        layout.addLayout(worker_layout)

        return card

    def _create_file_list_card(self):
        """创建文件列表卡片"""
        card = CardWidget()
        card.setMinimumHeight(300)
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # 标题和按钮
        header_layout = QHBoxLayout()

        title = StrongBodyLabel("📁 文件列表")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # 添加文件按钮
        add_btn = PrimaryPushButton("添加文件")
        add_btn.setIcon(FluentIcon.ADD)
        add_btn.clicked.connect(self._add_files)
        header_layout.addWidget(add_btn)

        # 添加文件夹按钮
        add_folder_btn = PushButton("添加文件夹")
        add_folder_btn.setIcon(FluentIcon.FOLDER_ADD)
        add_folder_btn.clicked.connect(self._add_folder)
        header_layout.addWidget(add_folder_btn)

        # 清空按钮
        clear_btn = PushButton("清空")
        clear_btn.setIcon(FluentIcon.DELETE)
        clear_btn.clicked.connect(self._clear_files)
        header_layout.addWidget(clear_btn)

        layout.addLayout(header_layout)

        # 文件列表 TreeWidget
        self.file_tree = TreeWidget()
        self.file_tree.setHeaderLabels(["文件名", "状态", "路径"])
        self.file_tree.setColumnWidth(0, 300)
        self.file_tree.setColumnWidth(1, 100)
        self.file_tree.setColumnWidth(2, 500)
        self.file_tree.setMinimumHeight(200)
        layout.addWidget(self.file_tree)

        # 统计信息
        self.stats_label = BodyLabel("就绪 - 0 个文件")
        layout.addWidget(self.stats_label)

        return card

    def _create_control_buttons(self):
        """创建控制按钮"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(10)

        # 开始按钮
        self.start_btn = PrimaryPushButton("开始处理")
        self.start_btn.setIcon(FluentIcon.PLAY)
        self.start_btn.setMinimumHeight(45)
        self.start_btn.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.start_btn.clicked.connect(self._start_processing)
        layout.addWidget(self.start_btn)

        # 停止按钮
        self.stop_btn = PushButton("停止")
        self.stop_btn.setIcon(FluentIcon.PAUSE)
        self.stop_btn.setMinimumHeight(45)
        self.stop_btn.clicked.connect(self._stop_processing)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)

        # 打开文件夹按钮
        open_btn = PushButton("打开输出文件夹")
        open_btn.setIcon(FluentIcon.FOLDER)
        open_btn.setMinimumHeight(45)
        open_btn.clicked.connect(self._open_output_folder)
        layout.addWidget(open_btn)

        layout.addStretch()

        return widget

    def _create_progress_card(self):
        """创建进度卡片"""
        card = CardWidget()
        card.setVisible(False)  # 初始隐藏
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # 标题
        self.progress_title = StrongBodyLabel("处理进度")
        layout.addWidget(self.progress_title)

        # 进度条
        from PyQt5.QtWidgets import QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078d7;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # 进度信息
        self.progress_info = BodyLabel("准备中...")
        layout.addWidget(self.progress_info)

        return card

    def _create_log_preview(self):
        """创建日志预览"""
        card = CardWidget()
        card.setMinimumHeight(150)
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        # 标题
        title = StrongBodyLabel("📋 日志预览")
        layout.addWidget(title)

        # 日志文本
        self.log_text = TextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        self.log_text.setStyleSheet("""
            TextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.log_text)

        return card

    def _setup_settings_interface(self):
        """设置界面"""
        layout = QVBoxLayout(self.settings_interface)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = SubtitleLabel("设置")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # 主题设置卡片
        theme_card = CardWidget()
        theme_layout = QVBoxLayout(theme_card)
        theme_layout.setSpacing(10)

        theme_title = StrongBodyLabel("🎨 主题设置")
        theme_layout.addWidget(theme_title)

        # 主题选择
        theme_select_layout = QHBoxLayout()
        theme_select_layout.addWidget(BodyLabel("外观主题:"))

        self.theme_combo = ComboBox()
        self.theme_combo.addItems(["深色", "浅色"])
        self.theme_combo.setCurrentText("深色" if self.settings.theme == "dark" else "浅色")
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        theme_select_layout.addWidget(self.theme_combo)

        theme_select_layout.addStretch()
        theme_layout.addLayout(theme_select_layout)

        layout.addWidget(theme_card)

        # 路径设置卡片
        path_card = CardWidget()
        path_layout = QVBoxLayout(path_card)
        path_layout.setSpacing(10)

        path_title = StrongBodyLabel("📂 路径设置")
        path_layout.addWidget(path_title)

        # 脚本目录
        script_dir_layout = QHBoxLayout()
        script_dir_layout.addWidget(BodyLabel("脚本目录:"))

        self.script_dir_edit = LineEdit()
        self.script_dir_edit.setText(self.settings.script_dir)
        script_dir_layout.addWidget(self.script_dir_edit, 1)

        script_dir_btn = PushButton("浏览...")
        script_dir_btn.clicked.connect(self._browse_script_dir)
        script_dir_layout.addWidget(script_dir_btn)

        path_layout.addLayout(script_dir_layout)

        # 备份目录
        backup_dir_layout = QHBoxLayout()
        backup_dir_layout.addWidget(BodyLabel("备份目录:"))

        self.backup_dir_edit = LineEdit()
        self.backup_dir_edit.setText(self.settings.backup_dir)
        backup_dir_layout.addWidget(self.backup_dir_edit, 1)

        backup_dir_btn = PushButton("浏览...")
        backup_dir_btn.clicked.connect(self._browse_backup_dir)
        backup_dir_layout.addWidget(backup_dir_btn)

        path_layout.addLayout(backup_dir_layout)

        # 保存按钮
        save_btn = PrimaryPushButton("保存设置")
        save_btn.setIcon(FluentIcon.SAVE)
        save_btn.clicked.connect(self._save_settings)
        path_layout.addWidget(save_btn)

        layout.addWidget(path_card)
        layout.addStretch()

    def _setup_log_interface(self):
        """设置日志界面"""
        layout = QVBoxLayout(self.log_interface)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = SubtitleLabel("处理日志")
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
        self.worker_spin.setValue(self.settings.max_workers)

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

            # 创建相对路径显示，便于用户识别
            script_items = []
            for jsx_file in jsx_files:
                try:
                    # 计算相对于脚本目录的相对路径
                    rel_path = jsx_file.relative_to(script_dir)

                    # 如果在子目录中，显示为 "子目录/脚本名"
                    if rel_path.parent.name != ".":
                        display_name = str(rel_path)
                    else:
                        display_name = rel_path.name

                    script_items.append({
                        'display': display_name,
                        'full_path': str(jsx_file)
                    })

                except ValueError as e:
                    self._add_log("error", f"无法处理文件 {jsx_file}: {e}")

            # 按显示名称排序
            script_items.sort(key=lambda x: x['display'])

            # 添加到下拉框和映射
            for item in script_items:
                self.script_combo.addItem(item['display'], item['full_path'])
                self.script_path_map[item['display']] = item['full_path']

            self._add_log("info", f"找到 {len(script_items)} 个脚本文件")
            self._show_info("脚本刷新完成", f"找到 {len(script_items)} 个脚本")

        except Exception as e:
            self._add_log("error", f"刷新脚本时出错: {e}")
            self._show_error("错误", f"刷新脚本失败: {e}")

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

    def _add_file_to_tree(self, file_path):
        """添加文件到树形列表"""
        path = Path(file_path)

        item = QTreeWidgetItem(self.file_tree)
        item.setText(0, path.name)
        item.setText(1, "待处理")
        item.setText(2, str(path))

        # 设置图标和颜色
        item.setIcon(0, FluentIcon.PHOTO.icon())

    def _clear_files(self):
        """清空文件列表"""
        if self.file_list:
            reply = MessageBox(
                "确认清空",
                f"确定要清空 {len(self.file_list)} 个文件吗？",
                self
            ).exec()

            if reply == QMessageBox.Yes:
                self.file_list.clear()
                self.file_tree.clear()
                self._update_stats()
                self._add_log("info", "文件列表已清空")

    def _update_stats(self):
        """更新统计信息"""
        total = len(self.file_list)
        self.stats_label.setText(f"就绪 - {total} 个文件")

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
        self.settings.max_workers = self.worker_spin.value()
        self.settings.last_script = current_script
        self.settings.save()

        # 显示进度卡片
        self.findChild(CardWidget).setVisible(True)  # 显示第一个卡片（进度卡片）

        # 禁用开始按钮，启用停止按钮
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        # 清空日志
        self.log_text.clear()

        self._add_log("info", f"开始处理 {len(self.file_list)} 个文件")
        self._add_log("info", f"使用脚本: {current_script}")
        self._add_log("info", f"并发数: {self.settings.max_workers}")

        # 创建并启动处理线程
        self.processing_thread = ProcessingThread(
            self.processor,
            self.file_list,
            script_path,
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

    def _on_progress_update(self, message, current, total):
        """进度更新"""
        if total > 0:
            percent = int((current / total) * 100)
            self.progress_bar.setValue(percent)
            self.progress_info.setText(f"{message} - {current}/{total} ({percent}%)")

    def _on_log_update(self, level, message):
        """日志更新"""
        self._add_log(level, message)

    def _on_processing_finished(self, success, message):
        """处理完成"""
        if success:
            self._add_log("success", f"处理完成: {message}")
            self._show_info("处理完成", message)
        else:
            self._add_log("error", f"处理失败: {message}")
            self._show_error("处理失败", message)

        self._reset_processing_ui()

    def _reset_processing_ui(self):
        """重置处理UI"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        # 隐藏进度卡片
        for child in self.home_interface.findChildren(CardWidget):
            if child.findChild(StrongBodyLabel) and child.findChild(StrongBodyLabel).text() == "处理进度":
                child.setVisible(False)
                break

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

        self.settings.theme = "dark" if theme == "深色" else "light"
        self.settings.save()

    def _toggle_theme(self):
        """切换主题"""
        current = self.theme_combo.currentText()
        new_theme = "浅色" if current == "深色" else "深色"
        self.theme_combo.setCurrentText(new_theme)

    def _set_dark_theme(self):
        """设置深色主题"""
        from PyQt5.QtWidgets import QApplication
        QApplication.instance().setStyleSheet("")
        # 这里可以添加深色主题的具体样式

    def _set_light_theme(self):
        """设置浅色主题"""
        from PyQt5.QtWidgets import QApplication
        QApplication.instance().setStyleSheet("")
        # 这里可以添加浅色主题的具体样式

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

        if self.settings.save():
            self._show_info("设置已保存", "设置已成功保存")
            self._add_log("info", "设置已保存")
        else:
            self._show_error("保存失败", "设置保存失败")

    def _clear_log(self):
        """清空日志"""
        self.full_log_text.clear()
        self.log_text.clear()
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

        # 添加到预览日志（限制行数）
        if self.log_text.document().lineCount() > 50:
            self.log_text.clear()
        self.log_text.append(log_line)

        # 滚动到底部
        self.full_log_text.verticalScrollBar().setValue(
            self.full_log_text.verticalScrollBar().maximum()
        )
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
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
    window = FluentMainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()