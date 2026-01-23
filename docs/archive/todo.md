# PSD Batch Processor

> PSD 批量处理器（或：PSD 脚本自动化工具）

---

## 一、项目概述

### 目标
开发一个独立的 Windows 桌面 GUI 应用程序，用于批量对 Photoshop 的 .psd 文件执行指定的 .jsx 脚本。核心特点是直接修改原始文件（生产环境常用模式），同时在处理前自动创建带时间戳的备份副本。

### 核心价值
- **安全**：每次批量操作前自动备份，避免误操作导致源文件永久丢失
- **高效**：通过 COM 接口直接控制已打开的 Photoshop 实例，减少启动开销
- **现代界面**：使用 customtkinter 打造美观、暗色/亮色主题一致的 UI
- **可维护**：分层清晰，配置可持久化，日志友好

### 目标用户
平面设计师、UI 设计师、批量修图/自动化后期人员（主要 Windows 环境）

---

## 二、功能需求（MVP → v1.0）

### 1. 基础设置区

- Photoshop 可执行路径检测/手动指定（默认尝试常见安装路径）
- 脚本存放目录（默认可设为程序同级 `scripts/` 或用户桌面）
- 支持刷新按钮，自动扫描目录下所有 `.jsx` 文件
- 下拉框选择要执行的脚本（单选）
- 备份目录（默认程序同级 `backups/`）
- 每次点击"开始"时，自动在备份目录下创建时间戳子文件夹，例如：`20260123_184530/`

### 2. 文件添加与管理

**支持两种添加方式：**
- 添加文件夹（递归扫描所有 `.psd`，可开关"包含子文件夹"）
- 添加文件（多选 `.psd`）

**文件列表展示**（Treeview 或 CTkScrollableFrame + 标签）：
- 列：文件名 | 完整路径 | 状态（待处理 / 备份完成 / 处理中 / 成功 / 失败）
- 支持右键菜单：移除该项 / 打开所在文件夹 / 打开文件（用 PS）

**其他功能：**
- 清空列表按钮
- 当前选中/总文件数统计

### 3. 处理流程（核心）

点击"开始处理"后：

1. 检查 Photoshop COM 是否可用
2. 创建本次时间戳备份子文件夹
3. 遍历待处理列表（建议单线程或最多并发 1~2，避免 PS 内存爆炸）
4. 使用 `shutil.copy2()` 复制源文件到备份子文件夹（保留元数据）
5. 通过 `win32com` 打开原始路径的 `.psd` 文件
6. 执行选中的 `.jsx` 脚本（`app.DoJavaScriptFile(jsx_path)`）
7. 根据执行结果：
   - 无异常 → 认为成功（jsx 内部应负责保存）
   - 有异常 → 记录错误信息，状态标记失败
8. 关闭文档（可选项：保存 / 不保存；默认跟随 jsx 行为）

实时更新列表状态 + 进度条 + 日志窗口

### 4. 日志与反馈

- 滚动日志窗口（支持不同颜色：info / success / error）
- 进度条（整体进度）
- 处理结束后：
  - 总结弹窗（成功 X / 失败 Y / 耗时）
  - "打开本次备份文件夹"按钮

### 5. 配置持久化（强烈推荐）

- 保存内容：脚本目录、备份根目录、Photoshop 路径、上次选择的 jsx 文件名
- 格式建议：`config.json` 或 `settings.toml`（放在程序目录或用户 AppData）

### 6. 非功能需求（MVP）

- 只支持 Windows（COM 依赖）
- 异常友好：大部分错误显示在日志，不崩溃程序
- 单实例运行（防止多开导致 COM 混乱）
- 日志同时输出到文件（`logs/20260123.log`）

---

## 三、技术栈（明确选型）

| 类别 | 选型 | 版本建议（2026年1月） | 理由 / 注意事项 |
|------|------|---------------------|----------------|
| 语言 | Python | 3.10 ~ 3.12 | 稳定 + pathlib 好用 |
| GUI 框架 | customtkinter | 5.2.2 或最新版 | 现代外观、内置暗黑模式、组件丰富 |
| Photoshop 控制 | win32com.client | pywin32 最新 | 最稳定、可精确打开指定文件 |
| 多线程/并发 | concurrent.futures.ThreadPoolExecutor | Python 标准库 | 简单、Future 好管理、易限并发数 |
| 文件复制 | shutil.copy2 | 标准库 | 保留元数据（修改时间等） |
| 路径处理 | pathlib (Path) | 标准库 | 跨平台写法、安全、链式调用友好 |
| 进度条 | customtkinter.CTkProgressBar | — | 与主题一致（比 ttk 更好看） |
| 日志组件 | customtkinter.CTkTextbox | — | 支持插入带颜色文本 |
| 配置文件 | json 或 tomllib (toml) | 标准库 (3.11+) | 人类可读，toml 更现代 |
| 依赖安装 | requirements.txt | — | 便于打包与分享 |
| 打包工具（可选） | PyInstaller / Nuitka | 最新版 | Nuitka 速度更快、体积可控 |

### 核心依赖清单（requirements.txt 示例）

```txt
customtkinter>=5.2.2
pywin32>=306
pillow   # 可选，用于将来预览缩略图
```

---

## 四、建议的分层架构（代码组织）

```
psd_batch_tool/
├── main.py                   # 程序入口，创建 CTk 窗口
├── app/
│   ├── __init__.py
│   ├── ui/
│   │   ├── main_window.py       # 主窗口布局、控件初始化、事件绑定
│   │   └── components/          # 可复用组件（如 FileListView、LogPanel）
│   ├── core/
│   │   ├── photoshop_controller.py   # COM 封装：open、run_jsx、close、错误处理
│   │   └── processor.py              # 批量处理逻辑（ThreadPoolExecutor）
│   ├── models/
│   │   └── file_item.py         # 文件项数据结构（path, status, backup_path...）
│   └── config/
│       └── settings.py          # 配置读写、默认值
├── utils/
│   ├── logger.py                # 日志工具（GUI + 文件双输出）
│   └── helpers.py               # 时间戳、路径安全检查等小函数
├── scripts/                     # 用户放 jsx 的目录（运行时扫描）
├── backups/                     # 备份根目录（gitignore）
├── logs/                        # 日志文件目录（gitignore）
└── config.json                  # 用户配置（gitignore 或纳入版本）
```

---

## 五、开发优先级建议（MVP 路线）

1. **环境验证**：写 30 行测试脚本，确认 win32com + customtkinter 能正常运行
2. **主界面骨架**：设置区 + 文件列表 + 脚本选择 + 开始按钮
3. **单文件处理验证**：open → run jsx → close（不加备份）
4. **加入备份逻辑** + 时间戳文件夹
5. **多文件 + ThreadPoolExecutor**（max_workers=1 或 2）
6. **日志着色 + 进度条联动**
7. **配置读写 + 异常美观处理**
8. **美化、测试、打包**

---

这份文档基本覆盖了从需求到技术实现的完整蓝图，适合自己开发或作为小团队/外包的说明文档使用。

如果你觉得某个部分需要更详细（例如 COM 错误码处理规范、进度更新的线程安全细节、备份策略的变体），可以告诉我，我再帮你扩展对应章节。
