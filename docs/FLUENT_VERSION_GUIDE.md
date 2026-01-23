# PyQt-Fluent-Widgets 版本指南

本文档介绍 PyQt-Fluent-Widgets 版本的 PSD Batch Processor，这是一个现代化、美观的界面版本。

## 📋 版本对比

| 特性 | CustomTkinter 版本 | PyQt-Fluent-Widgets 版本 |
|------|-------------------|-------------------------|
| **界面风格** | 现代化，类似 Material Design | Fluent Design (Windows 11 风格) |
| **导航方式** | 单页面布局 | 多页面导航 (侧边栏) |
| **控件丰富度** | 基础控件 | 丰富的高级控件 |
| **主题支持** | 深色/浅色主题 | 完整的 Fluent 主题系统 |
| **响应式设计** | 良好 | 优秀 |
| **学习曲线** | 简单 | 中等 |
| **依赖大小** | 较小 | 较大 |

## 🚀 快速启动

### 方法 1: 使用启动脚本

```bash
# 进入项目目录
cd "F:\插件脚本开发\PSD Batch Processor"

# 运行启动脚本
python tools\run_fluent.py
```

### 方法 2: 直接运行

```bash
# 进入项目目录
cd "F:\插件脚本开发\PSD Batch Processor"

# 安装依赖
pip install PyQt5 PyQt-Fluent-Widgets pywin32

# 运行主程序
python src\main_fluent.py
```

### 方法 3: 使用 Python 解释器

```python
import sys
from pathlib import Path

# 添加 src 到路径
src_dir = Path("src")
sys.path.insert(0, str(src_dir))

# 导入并运行
from app.ui.fluent_main_window import main
main()
```

## 🎨 界面特性

### 1. **Fluent Design 风格**
- 现代化的侧边栏导航
- 卡片式布局
- 平滑的动画效果
- 原生 Windows 风格

### 2. **多页面导航**
- **主页**: 文件处理核心功能
- **设置**: 配置选项
- **日志**: 完整日志查看

### 3. **丰富的控件**
- `FluentWindow`: 主窗口
- `CardWidget`: 卡片容器
- `InfoBar`: 信息提示条
- `TreeWidget`: 树形列表
- `ComboBox`: 下拉选择框
- `LineEdit`: 文本输入框
- `TextEdit`: 文本编辑器

### 4. **实时反馈**
- 进度条显示处理进度
- 实时日志更新
- 信息提示条
- 状态显示

## 📁 文件结构

```
PSD Batch Processor/
├── src/
│   ├── app/
│   │   └── ui/
│   │       ├── fluent_main_window.py    # PyQt-Fluent-Widgets 主窗口
│   │       └── main_window.py           # CustomTkinter 主窗口 (保留)
│   ├── main.py                          # CustomTkinter 启动脚本
│   └── main_fluent.py                   # PyQt-Fluent-Widgets 启动脚本
├── tools/
│   ├── run.bat                          # 运行 CustomTkinter 版本
│   ├── run_fluent.py                    # 运行 PyQt-Fluent-Widgets 版本
│   └── build.bat                        # 打包工具
├── tests/
│   └── test_fluent_widgets.py           # PyQt-Fluent-Widgets 测试
└── docs/
    └── FLUENT_VERSION_GUIDE.md          # 本文档
```

## 🔧 功能特性

### 主页界面

#### 设置区域
- **Photoshop 路径**: 浏览选择 Photoshop.exe
- **脚本选择**: 下拉框选择脚本，支持子目录
- **并发数设置**: 控制同时处理的文件数量

#### 文件列表
- **添加文件**: 选择多个 PSD 文件
- **添加文件夹**: 递归添加文件夹中的所有 PSD 文件
- **清空列表**: 清空所有文件
- **状态显示**: 实时显示每个文件的处理状态

#### 控制按钮
- **开始处理**: 开始批量处理
- **停止**: 停止当前处理
- **打开输出文件夹**: 快速打开备份目录

#### 进度显示
- **进度条**: 显示总体进度
- **进度信息**: 显示当前处理的文件和百分比

#### 日志预览
- **实时日志**: 显示最近的日志消息
- **颜色编码**: 不同级别日志使用不同颜色

### 设置界面

#### 主题设置
- **深色/浅色主题**: 切换界面主题
- **实时切换**: 无需重启应用

#### 路径设置
- **脚本目录**: 自定义脚本扫描目录
- **备份目录**: 自定义备份文件夹位置
- **保存设置**: 持久化配置

### 日志界面

#### 完整日志
- **全部日志**: 查看所有历史日志
- **清空日志**: 清空日志显示
- **保存日志**: 将日志保存到文件

#### 日志级别
- **INFO**: 一般信息
- **SUCCESS**: 成功消息
- **WARNING**: 警告信息
- **ERROR**: 错误信息

## 🎯 使用流程

### 1. 首次使用

1. **启动应用**
   ```bash
   python tools\run_fluent.py
   ```

2. **配置 Photoshop 路径**
   - 点击"浏览..."按钮
   - 选择 Photoshop.exe 文件
   - 通常在 `C:\Program Files\Adobe\Adobe Photoshop 2025\Photoshop.exe`

3. **选择脚本**
   - 点击"刷新"按钮扫描脚本
   - 从下拉框中选择要执行的脚本

4. **添加文件**
   - 点击"添加文件"选择 PSD 文件
   - 或点击"添加文件夹"批量添加

5. **开始处理**
   - 点击"开始处理"按钮
   - 等待处理完成

### 2. 日常使用

1. **快速启动**: 运行 `tools\run_fluent.py`
2. **添加文件**: 拖拽或浏览选择 PSD 文件
3. **选择脚本**: 选择预设脚本
4. **开始处理**: 点击开始按钮
5. **查看日志**: 在日志页面查看详细输出

## ⚙️ 配置选项

### 应用配置

配置文件位置：
- 开发环境: `src/config.json`
- 打包后: `%APPDATA%\PSDBatchProcessor\config.json`

配置项：
```json
{
  "photoshop_path": "C:\\Program Files\\Adobe\\Adobe Photoshop 2025\\Photoshop.exe",
  "script_dir": "scripts",
  "backup_dir": "backups",
  "last_script": "",
  "max_workers": 1,
  "theme": "dark",
  "include_subfolders": true
}
```

### 主题配置

支持两种主题：
- **深色主题**: 适合暗光环境，护眼
- **浅色主题**: 适合明亮环境

主题切换会立即生效，无需重启。

## 🔍 故障排除

### 问题: 无法导入 PyQt-Fluent-Widgets

**解决方案**:
```bash
pip install PyQt-Fluent-Widgets PyQt5
```

### 问题: 界面显示异常

**解决方案**:
1. 检查 Python 版本 (需要 3.8+)
2. 重新安装依赖:
   ```bash
   pip uninstall PyQt5 PyQt-Fluent-Widgets
   pip install PyQt5 PyQt-Fluent-Widgets
   ```

### 问题: Photoshop 无法启动

**解决方案**:
1. 检查 Photoshop 路径是否正确
2. 确保 Photoshop 已安装
3. 以管理员权限运行应用

### 问题: 脚本无法找到

**解决方案**:
1. 检查脚本目录设置
2. 点击"刷新"按钮重新扫描
3. 确保脚本文件扩展名为 `.jsx`

## 📦 打包发布

### 使用 PyInstaller 打包

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包 PyQt-Fluent-Widgets 版本
pyinstaller ^
    --name="PSDBatchProcessor_Fluent" ^
    --noconsole ^
    --onefile ^
    --add-data="docs/guides/START_HERE.txt;docs/guides" ^
    --add-data="docs/guides/QUICK_REFERENCE.txt;docs/guides" ^
    --add-data="scripts/production/*.jsx;scripts/production" ^
    --add-data="scripts/templates/*.jsx;scripts/templates" ^
    --add-data="scripts/examples/*.jsx;scripts/examples" ^
    --hidden-import=win32com ^
    --hidden-import=pythoncom ^
    --hidden-import=PIL ^
    --hidden-import=PyQt5 ^
    --hidden-import=PyQtFluentWidgets ^
    src/main_fluent.py
```

### 使用打包脚本

```bash
# 使用 tools\build.bat 选择 "One-file mode"
python tools\build.bat
```

## 🎨 界面截图说明

### 主页界面
```
┌─────────────────────────────────────────────────────────┐
│ PSD 批量处理器                                            │
├─────────────────────────────────────────────────────────┤
│ ⚙️ 设置                                                  │
│   Photoshop 路径: [浏览...]                              │
│   选择脚本:     [下拉框] [刷新]                          │
│   并发数:       [1]                                      │
├─────────────────────────────────────────────────────────┤
│ 📁 文件列表                                              │
│   [添加文件] [添加文件夹] [清空]                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │ 文件名          状态      路径                  │   │
│   │ test.psd        待处理    C:\...\test.psd       │   │
│   └─────────────────────────────────────────────────┘   │
│   就绪 - 1 个文件                                        │
├─────────────────────────────────────────────────────────┤
│ [开始处理] [停止] [打开输出文件夹]                       │
├─────────────────────────────────────────────────────────┤
│ 📋 日志预览                                              │
│   [2026-01-24 12:00:00] [INFO] 脚本目录: ...            │
│   [2026-01-24 12:00:01] [INFO] 备份目录: ...            │
└─────────────────────────────────────────────────────────┘
```

### 设置界面
```
┌─────────────────────────────────────────────────────────┐
│ 设置                                                    │
├─────────────────────────────────────────────────────────┤
│ 🎨 主题设置                                             │
│   外观主题: [深色 ▼]                                    │
├─────────────────────────────────────────────────────────┤
│ 📂 路径设置                                             │
│   脚本目录: [scripts] [浏览...]                         │
│   备份目录: [backups] [浏览...]                         │
│   [保存设置]                                            │
└─────────────────────────────────────────────────────────┘
```

### 日志界面
```
┌─────────────────────────────────────────────────────────┐
│ 处理日志                                                │
├─────────────────────────────────────────────────────────┤
│ [清空日志] [保存日志]                                   │
├─────────────────────────────────────────────────────────┤
│ [2026-01-24 12:00:00] [INFO] 开始处理 5 个文件          │
│ [2026-01-24 12:00:01] [INFO] 使用脚本: example.jsx      │
│ [2026-01-24 12:00:02] [INFO] test.psd: 处理中           │
│ [2026-01-24 12:00:05] [SUCCESS] test.psd: 完成          │
│ [2026-01-24 12:00:10] [SUCCESS] 处理完成                │
└─────────────────────────────────────────────────────────┘
```

## 📊 性能对比

| 指标 | CustomTkinter | PyQt-Fluent-Widgets |
|------|---------------|---------------------|
| **启动时间** | ~1-2 秒 | ~2-3 秒 |
| **内存占用** | ~50 MB | ~80 MB |
| **界面响应** | 快速 | 快速 |
| **动画效果** | 基础 | 流畅 |
| **系统集成** | 一般 | 优秀 (Windows) |

## 🔗 相关资源

- **PyQt-Fluent-Widgets GitHub**: https://github.com/zhiyiYo/PyQt-Fluent-Widgets
- **官方文档**: https://pyqt-fluent-widgets.readthedocs.io/
- **示例代码**: https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/main/examples

## 📝 总结

PyQt-Fluent-Widgets 版本提供了：
- ✅ 更现代化的界面设计
- ✅ 更好的 Windows 集成
- ✅ 更丰富的控件库
- ✅ 更流畅的用户体验
- ✅ 完整的 Fluent Design 风格

适合追求界面美观和用户体验的用户。如果需要轻量级版本，可以继续使用 CustomTkinter 版本。

---

**版本**: 1.0.0
**更新日期**: 2026-01-24
**维护者**: Claude Code