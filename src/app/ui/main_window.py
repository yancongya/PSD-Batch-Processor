"""
主窗口界面
使用 customtkinter 构建现代化 GUI
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional

import customtkinter as ctk

from app.config.settings import get_settings, init_settings
from app.core.processor import BatchProcessor
from app.models.file_item import FileItem, FileStatus
from utils.logger import get_logger, init_logger


class MainWindow(ctk.CTk):
    """主窗口类"""

    def __init__(self):
        super().__init__()

        # 初始化配置和日志
        self.settings = init_settings()
        self.logger = init_logger()

        # 批量处理器
        self.processor = BatchProcessor()
        self.processor.set_callbacks(
            on_progress=self._on_progress,
            on_status_update=self._on_status_update,
            on_finished=self._on_finished
        )

        # 设置日志 GUI 回调
        self.logger.set_gui_callback(self._on_log_message)

        # 窗口配置
        self.title("PSD Batch Processor - PSD 批量处理器")
        self.geometry("1200x800")
        self.minsize(900, 600)  # 降低最小尺寸要求

        # 设置主题
        self._setup_theme()

        # 创建界面
        self._create_widgets()

        # 加载配置
        self._load_settings()

        # 确保脚本目录存在（单文件EXE时会提取脚本）
        self._ensure_directories()

        # 绑定事件
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_theme(self):
        """设置主题"""
        theme = self.settings.theme
        if theme == "dark":
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("dark-blue")
        else:
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")

    def _ensure_directories(self):
        """确保必要的目录存在（单文件EXE时会提取脚本）"""
        try:
            # 确保脚本目录存在（单文件EXE时会从打包资源中提取脚本）
            self.settings.ensure_script_dir_exists()

            # 确保备份目录存在
            backup_dir = self.settings.get_backup_dir_path()
            backup_dir.mkdir(parents=True, exist_ok=True)

            self.logger.info(f"脚本目录: {self.settings.get_script_dir_path()}")
            self.logger.info(f"备份目录: {backup_dir}")

        except Exception as e:
            self.logger.error(f"创建目录时出错: {e}")

    def _create_widgets(self):
        """创建界面组件"""
        # 主框架 - 使用可滚动的框架
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 顶部设置区
        self._create_settings_frame()

        # 中间文件列表区
        self._create_file_list_frame()

        # 底部日志和进度区
        self._create_log_frame()

        # 控制按钮区（固定在底部）
        self._create_control_frame()

    def _create_settings_frame(self):
        """创建设置区域"""
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", padx=10, pady=10)

        # 标题
        title = ctk.CTkLabel(frame, text="⚙️ 基础设置", font=("微软雅黑", 16, "bold"))
        title.pack(anchor="w", padx=10, pady=(10, 5))

        # Photoshop 路径
        ps_frame = ctk.CTkFrame(frame, fg_color="transparent")
        ps_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(ps_frame, text="Photoshop 路径:", width=120, anchor="w").pack(side="left")
        self.ps_path_var = ctk.StringVar()
        self.ps_path_entry = ctk.CTkEntry(ps_frame, textvariable=self.ps_path_var)
        self.ps_path_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.ps_browse_btn = ctk.CTkButton(ps_frame, text="浏览...", width=80, command=self._browse_photoshop_path)
        self.ps_browse_btn.pack(side="left")

        # 脚本目录
        script_frame = ctk.CTkFrame(frame, fg_color="transparent")
        script_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(script_frame, text="脚本目录:", width=120, anchor="w").pack(side="left")
        self.script_dir_var = ctk.StringVar()
        self.script_dir_entry = ctk.CTkEntry(script_frame, textvariable=self.script_dir_var)
        self.script_dir_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.script_browse_btn = ctk.CTkButton(script_frame, text="浏览...", width=80, command=self._browse_script_dir)
        self.script_browse_btn.pack(side="left")

        # 脚本选择
        script_select_frame = ctk.CTkFrame(frame, fg_color="transparent")
        script_select_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(script_select_frame, text="选择脚本:", width=120, anchor="w").pack(side="left")
        self.script_var = ctk.StringVar()
        self.script_combo = ctk.CTkComboBox(script_select_frame, variable=self.script_var)
        self.script_combo.pack(side="left", padx=5, fill="x", expand=True)

        self.refresh_script_btn = ctk.CTkButton(script_select_frame, text="刷新", width=80, command=self._refresh_scripts)
        self.refresh_script_btn.pack(side="left")

        # 备份目录
        backup_frame = ctk.CTkFrame(frame, fg_color="transparent")
        backup_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(backup_frame, text="备份目录:", width=120, anchor="w").pack(side="left")
        self.backup_dir_var = ctk.StringVar()
        self.backup_dir_entry = ctk.CTkEntry(backup_frame, textvariable=self.backup_dir_var)
        self.backup_dir_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.backup_browse_btn = ctk.CTkButton(backup_frame, text="浏览...", width=80, command=self._browse_backup_dir)
        self.backup_browse_btn.pack(side="left")

        # 选项
        options_frame = ctk.CTkFrame(frame, fg_color="transparent")
        options_frame.pack(fill="x", padx=10, pady=5)

        # 主题切换
        ctk.CTkLabel(options_frame, text="主题:").pack(side="left", padx=(0, 5))
        self.theme_var = ctk.StringVar(value=self.settings.theme)
        self.theme_combo = ctk.CTkComboBox(options_frame, values=["dark", "light"], variable=self.theme_var, width=100, command=self._on_theme_change)
        self.theme_combo.pack(side="left", padx=5)

        # 并发数
        ctk.CTkLabel(options_frame, text="并发数:").pack(side="left", padx=(20, 5))
        self.workers_var = ctk.StringVar(value=str(self.settings.max_workers))
        self.workers_combo = ctk.CTkComboBox(options_frame, values=["1", "2"], variable=self.workers_var, width=80)
        self.workers_combo.pack(side="left", padx=5)

        # 包含子文件夹
        self.subfolders_var = ctk.BooleanVar(value=self.settings.include_subfolders)
        self.subfolders_check = ctk.CTkCheckBox(options_frame, text="包含子文件夹", variable=self.subfolders_var)
        self.subfolders_check.pack(side="left", padx=(20, 5))


    def _create_file_list_frame(self):
        """创建文件列表区域"""
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # 标题和按钮
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(header_frame, text="📁 文件列表", font=("微软雅黑", 14, "bold")).pack(side="left")

        # 统计信息
        self.stats_label = ctk.CTkLabel(header_frame, text="共 0 个文件 | 待处理: 0", font=("微软雅黑", 11))
        self.stats_label.pack(side="left", padx=20)

        # 操作按钮
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side="right")

        self.add_files_btn = ctk.CTkButton(btn_frame, text="添加文件", width=90, command=self._add_files)
        self.add_files_btn.pack(side="left", padx=2)

        self.add_folder_btn = ctk.CTkButton(btn_frame, text="添加文件夹", width=90, command=self._add_folder)
        self.add_folder_btn.pack(side="left", padx=2)

        self.remove_btn = ctk.CTkButton(btn_frame, text="移除选中", width=90, command=self._remove_selected, fg_color="#dc3545", hover_color="#c82333")
        self.remove_btn.pack(side="left", padx=2)

        self.clear_btn = ctk.CTkButton(btn_frame, text="清空列表", width=90, command=self._clear_list, fg_color="#6c757d", hover_color="#5a6268")
        self.clear_btn.pack(side="left", padx=2)

        # 文件列表（使用 Treeview）
        from tkinter import ttk

        # 创建滚动框架
        scroll_frame = ctk.CTkFrame(frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 创建 Treeview
        columns = ("file_name", "path", "status", "size")
        self.tree = ttk.Treeview(scroll_frame, columns=columns, show="headings", height=12)  # 减少高度

        # 配置列 - 优化列宽比例
        self.tree.heading("file_name", text="文件名")
        self.tree.heading("path", text="路径")
        self.tree.heading("status", text="状态")
        self.tree.heading("size", text="大小")

        # 动态列宽设置（根据窗口大小调整）
        self.tree.column("file_name", width=180, anchor="w", minwidth=120)
        self.tree.column("path", width=350, anchor="w", minwidth=150)
        self.tree.column("status", width=100, anchor="center", minwidth=80)
        self.tree.column("size", width=80, anchor="e", minwidth=60)

        # 滚动条
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 右键菜单
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="打开文件夹", command=self._open_file_location)
        self.context_menu.add_command(label="用 Photoshop 打开", command=self._open_file_with_ps)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="移除", command=self._remove_selected)

        self.tree.bind("<Button-3>", self._show_context_menu)
        self.tree.bind("<Double-1>", self._on_double_click)

    def _create_log_frame(self):
        """创建日志区域"""
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", padx=10, pady=(0, 10))

        # 标题
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(header_frame, text="📝 日志", font=("微软雅黑", 14, "bold")).pack(side="left")

        # 进度条
        self.progress_bar = ctk.CTkProgressBar(header_frame, width=200)
        self.progress_bar.pack(side="right", padx=10)
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(header_frame, text="0%", width=50)
        self.progress_label.pack(side="right")

        # 日志文本框
        log_frame = ctk.CTkFrame(frame, fg_color="transparent")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = ctk.CTkTextbox(log_frame, height=120, font=("Consolas", 9))  # 减小高度
        self.log_text.pack(fill="both", expand=True)

    def _create_control_frame(self):
        """创建控制按钮区域"""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=10)

        # 使用更紧凑的布局
        # 左侧按钮组
        left_frame = ctk.CTkFrame(frame, fg_color="transparent")
        left_frame.pack(side="left")

        # 开始按钮
        self.start_btn = ctk.CTkButton(
            left_frame, text="▶️ 开始处理", font=("微软雅黑", 12, "bold"),
            fg_color="#28a745", hover_color="#218838",
            width=120, height=35, command=self._start_processing
        )
        self.start_btn.pack(side="left", padx=5)

        # 停止按钮
        self.stop_btn = ctk.CTkButton(
            left_frame, text="⏹️ 停止", font=("微软雅黑", 11),
            fg_color="#dc3545", hover_color="#c82333",
            width=90, height=35, command=self._stop_processing
        )
        self.stop_btn.pack(side="left", padx=5)

        # 右侧按钮组
        right_frame = ctk.CTkFrame(frame, fg_color="transparent")
        right_frame.pack(side="right")

        # 保存配置按钮
        self.save_config_btn = ctk.CTkButton(
            right_frame, text="💾 保存", font=("微软雅黑", 11),
            fg_color="#6c757d", hover_color="#5a6268",
            width=80, height=35, command=self._save_config
        )
        self.save_config_btn.pack(side="left", padx=5)

        # 打开备份文件夹按钮
        self.open_backup_btn = ctk.CTkButton(
            right_frame, text="📂 备份", font=("微软雅黑", 11),
            fg_color="#17a2b8", hover_color="#138496",
            width=80, height=35, command=self._open_backup_folder
        )
        self.open_backup_btn.pack(side="left", padx=5)

    def _load_settings(self):
        """加载配置到界面"""
        self.ps_path_var.set(self.settings.photoshop_path)
        self.script_dir_var.set(self.settings.script_dir)
        self.backup_dir_var.set(self.settings.backup_dir)
        self.script_var.set(self.settings.last_script)
        self.theme_var.set(self.settings.theme)
        self.workers_var.set(str(self.settings.max_workers))
        self.subfolders_var.set(self.settings.include_subfolders)

        # 刷新脚本列表
        self._refresh_scripts()

    def _save_config(self):
        """保存配置"""
        try:
            self.settings.photoshop_path = self.ps_path_var.get()
            self.settings.script_dir = self.script_dir_var.get()
            self.settings.backup_dir = self.backup_dir_var.get()
            self.settings.last_script = self.script_var.get()
            self.settings.theme = self.theme_var.get()
            self.settings.max_workers = int(self.workers_var.get())
            self.settings.include_subfolders = self.subfolders_var.get()

            if self.settings.save():
                messagebox.showinfo("成功", "配置已保存！")
            else:
                messagebox.showerror("错误", "保存配置失败！")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置时出错: {e}")

    def _on_theme_change(self, new_theme: str):
        """主题切换回调"""
        ctk.set_appearance_mode(new_theme)
        self.settings.theme = new_theme

    def _browse_photoshop_path(self):
        """浏览 Photoshop 路径"""
        path = filedialog.askopenfilename(
            title="选择 Photoshop 可执行文件",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if path:
            self.ps_path_var.set(path)

    def _browse_script_dir(self):
        """浏览脚本目录"""
        path = filedialog.askdirectory(title="选择脚本目录")
        if path:
            self.script_dir_var.set(path)
            self._refresh_scripts()

    def _browse_backup_dir(self):
        """浏览备份目录"""
        path = filedialog.askdirectory(title="选择备份目录")
        if path:
            self.backup_dir_var.set(path)

    def _refresh_scripts(self):
        """刷新脚本列表（支持递归扫描子目录）"""
        # 使用新的路径处理方法，支持单文件EXE
        script_dir_str = self.script_dir_var.get()
        script_dir = Path(script_dir_str)

        # 如果是相对路径，尝试解析为完整路径
        if not script_dir.is_absolute():
            script_dir = self.settings.get_script_dir_path()
        else:
            script_dir = Path(script_dir_str)

        if not script_dir.exists():
            self.script_combo.configure(values=[])
            return

        # 递归扫描所有.jsx文件（包括子目录）
        jsx_files = list(script_dir.rglob("*.jsx"))

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
            except ValueError:
                # 如果无法计算相对路径，直接使用文件名
                script_items.append({
                    'display': jsx_file.name,
                    'full_path': str(jsx_file)
                })

        # 按显示名称排序
        script_items.sort(key=lambda x: x['display'])

        # 更新下拉框
        display_names = [item['display'] for item in script_items]
        self.script_combo.configure(values=display_names)

        # 存储完整的路径映射
        self._script_path_map = {item['display']: item['full_path'] for item in script_items}

        # 如果有上次选择的脚本且在列表中，保持选中
        last_script = self.script_var.get()
        if last_script in display_names:
            self.script_var.set(last_script)
        elif display_names:
            self.script_var.set(display_names[0])

    def _add_files(self):
        """添加文件"""
        files = filedialog.askopenfilenames(
            title="选择 PSD 文件",
            filetypes=[("PSD files", "*.psd"), ("All files", "*.*")]
        )
        if files:
            added = self.processor.file_list.add_files(list(files))
            if added:
                self._update_file_list()
                self.logger.info(f"添加了 {len(added)} 个文件")

    def _add_folder(self):
        """添加文件夹"""
        folder = filedialog.askdirectory(title="选择包含 PSD 文件的文件夹")
        if folder:
            recursive = self.subfolders_var.get()
            added = self.processor.file_list.add_folder(folder, recursive)
            if added:
                self._update_file_list()
                self.logger.info(f"从文件夹添加了 {len(added)} 个文件")

    def _remove_selected(self):
        """移除选中的文件"""
        selected = self.tree.selection()
        if not selected:
            return

        # 获取选中的文件名
        for item_id in selected:
            values = self.tree.item(item_id, "values")
            if values:
                file_name = values[0]
                # 查找并移除
                for file_item in self.processor.file_list.get_all():
                    if file_item.file_name == file_name:
                        self.processor.file_list.remove_item(file_item)
                        break

        self._update_file_list()
        self.logger.info("已移除选中的文件")

    def _clear_list(self):
        """清空列表"""
        if messagebox.askyesno("确认", "确定要清空所有文件吗？"):
            self.processor.file_list.clear()
            self._update_file_list()
            self.logger.info("文件列表已清空")

    def _update_file_list(self):
        """更新文件列表显示"""
        # 清空 Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 添加文件
        for file_item in self.processor.file_list.get_all():
            values = (
                file_item.file_name,
                str(file_item.path.parent),
                file_item.status_text,
                f"{file_item.size_mb:.2f} MB"
            )
            self.tree.insert("", "end", values=values)

        # 更新统计
        self._update_stats()

    def _update_stats(self):
        """更新统计信息"""
        total = self.processor.file_list.count()
        pending = self.processor.file_list.count_pending()
        self.stats_label.configure(text=f"共 {total} 个文件 | 待处理: {pending}")

    def _show_context_menu(self, event):
        """显示右键菜单"""
        try:
            item = self.tree.identify_row(event.y)
            if item:
                self.tree.selection_set(item)
                self.context_menu.post(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def _on_double_click(self, event):
        """双击事件"""
        self._open_file_with_ps()

    def _open_file_location(self):
        """打开文件所在文件夹"""
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        values = self.tree.item(item_id, "values")
        if values:
            file_name = values[0]
            for file_item in self.processor.file_list.get_all():
                if file_item.file_name == file_name:
                    import subprocess
                    subprocess.Popen(['explorer', str(file_item.path.parent)])
                    break

    def _open_file_with_ps(self):
        """用 Photoshop 打开文件"""
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        values = self.tree.item(item_id, "values")
        if values:
            file_name = values[0]
            for file_item in self.processor.file_list.get_all():
                if file_item.file_name == file_name:
                    import os
                    os.startfile(str(file_item.path))
                    break

    def _open_backup_folder(self):
        """打开备份文件夹"""
        backup_folder = self.processor.get_backup_folder()
        if backup_folder and backup_folder.exists():
            import subprocess
            subprocess.Popen(['explorer', str(backup_folder)])
        else:
            messagebox.showwarning("提示", "没有找到备份文件夹")

    def _start_processing(self):
        """开始处理"""
        # 验证配置
        script_display = self.script_var.get()
        if not script_display:
            messagebox.showerror("错误", "请先选择要执行的脚本！")
            return

        # 使用路径映射获取完整的脚本路径
        if hasattr(self, '_script_path_map') and script_display in self._script_path_map:
            full_script_path_str = self._script_path_map[script_display]
            full_script_path = Path(full_script_path_str)
        else:
            # 回退到旧的路径解析方式
            script_dir_str = self.script_dir_var.get()
            script_dir = Path(script_dir_str)

            # 如果是相对路径，解析为完整路径
            if not script_dir.is_absolute():
                script_dir = self.settings.get_script_dir_path()

            full_script_path = script_dir / script_display

        if not full_script_path.exists():
            messagebox.showerror("错误", f"脚本文件不存在: {full_script_path}")
            return

        # 验证是否有文件
        if self.processor.file_list.count_pending() == 0:
            messagebox.showwarning("提示", "没有待处理的文件！")
            return

        # 确认开始
        if not messagebox.askyesno("确认", f"确定开始处理 {self.processor.file_list.count_pending()} 个文件吗？"):
            return

        # 更新配置
        self.settings.photoshop_path = self.ps_path_var.get()
        self.settings.script_dir = self.script_dir_var.get()
        self.settings.backup_dir = self.backup_dir_var.get()
        self.settings.last_script = self.script_var.get()
        self.settings.max_workers = int(self.workers_var.get())
        self.settings.include_subfolders = self.subfolders_var.get()

        # 禁用按钮
        self._set_buttons_enabled(False)

        # 清空日志
        self.log_text.delete("1.0", "end")

        # 开始处理（在主线程执行）
        self.after(100, lambda: self._run_processing(str(full_script_path)))

    def _run_processing(self, script_path: str):
        """执行处理（在主线程）"""
        try:
            self.processor.process_batch(script_path)
        except Exception as e:
            self.logger.error(f"处理过程中出错: {e}")
            messagebox.showerror("错误", f"处理过程中出错: {e}")
        finally:
            self._set_buttons_enabled(True)

    def _stop_processing(self):
        """停止处理"""
        if self.processor.is_processing:
            self.processor.stop_processing()
            self.logger.warning("用户主动停止处理")

    def _set_buttons_enabled(self, enabled: bool):
        """设置按钮启用状态"""
        state = "normal" if enabled else "disabled"
        self.start_btn.configure(state=state)
        self.add_files_btn.configure(state=state)
        self.add_folder_btn.configure(state=state)
        self.remove_btn.configure(state=state)
        self.clear_btn.configure(state=state)

    def _on_progress(self, current: int, total: int, message: str):
        """进度回调"""
        def update_progress():
            if total > 0:
                progress = current / total
                self.progress_bar.set(progress)
                self.progress_label.configure(text=f"{int(progress * 100)}%")
                self.logger.info(message)

        # 确保在主线程执行
        self.after(0, update_progress)

    def _on_status_update(self, file_name: str, status: str):
        """状态更新回调"""
        # 更新 Treeview 中的状态
        for item_id in self.tree.get_children():
            values = self.tree.item(item_id, "values")
            if values and values[0] == file_name:
                new_values = list(values)
                new_values[2] = status
                self.tree.item(item_id, values=new_values)
                break

    def _on_finished(self, success: int, failed: int, elapsed: float):
        """处理完成回调"""
        # 更新统计
        self._update_stats()

        # 显示结果
        message = f"处理完成！\\n成功: {success}\\n失败: {failed}\\n耗时: {elapsed:.2f} 秒"
        messagebox.showinfo("完成", message)

        # 重置进度条
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")

    def _on_log_message(self, level: str, message: str):
        """日志消息回调（确保在主线程执行）"""
        def update_log():
            # 根据级别设置颜色
            colors = {
                "info": "#000000",      # 黑色
                "success": "#00aa00",   # 绿色
                "warning": "#ff8800",   # 橙色
                "error": "#dd0000",     # 红色
                "debug": "#666666",     # 灰色
            }
            color = colors.get(level, "#000000")

            # 插入日志
            self.log_text.insert("end", f"{message}\\n")
            self.log_text.tag_add(level, "end-2l", "end-1l")
            self.log_text.tag_config(level, foreground=color)

            # 滚动到底部
            self.log_text.see("end")

        # 确保在主线程执行
        self.after(0, update_log)

    def _on_closing(self):
        """窗口关闭事件"""
        if self.processor.is_processing:
            if not messagebox.askyesno("确认", "处理正在进行中，确定要退出吗？"):
                return

        # 保存配置
        self._save_config()

        # 关闭窗口
        self.destroy()