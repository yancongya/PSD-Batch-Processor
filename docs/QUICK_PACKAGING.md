# 快速打包指南

## 🚀 一键打包（推荐）

### 方法 1：使用 Python 脚本（推荐）

```bash
cd "F:\插件脚本开发\PSD Batch Processor"
python tools/build.py
```

然后选择：
- **1** - 窗口模式（推荐，无控制台）
- **2** - 控制台模式（调试用）
- **3** - 单文件模式（便携版）

### 方法 2：使用批处理脚本

```bash
cd "F:\插件脚本开发\PSD Batch Processor"
tools\build.bat
```

然后选择相应的模式。

## 📦 打包模式说明

### 1. 窗口模式（推荐）
- **特点**：无控制台窗口，双击运行
- **文件大小**：60-80 MB
- **适合**：最终用户分发
- **使用场景**：给其他人使用

### 2. 控制台模式
- **特点**：显示控制台窗口，可以看到日志
- **文件大小**：60-80 MB
- **适合**：调试和问题排查
- **使用场景**：开发测试

### 3. 单文件模式
- **特点**：所有文件打包到一个 EXE
- **文件大小**：60-80 MB
- **适合**：便携使用
- **使用场景**：U盘携带，无需安装

## 📁 打包结果

打包完成后，文件位置：
```
dist/PSDBatchProcessor/
├── PSDBatchProcessor.exe      # 主程序
├── README.md                  # 说明文档
├── docs/
│   └── guides/
│       ├── START_HERE.txt     # 快速开始
│       └── QUICK_REFERENCE.txt # 快速参考
└── (其他依赖文件)
```

## 🎯 首次运行

### 1. 运行程序
双击 `PSDBatchProcessor.exe`

### 2. 自动创建的文件和目录
- `backups/` - 备份目录
- `src/app/config/config.json` - 配置文件

### 3. 配置步骤
1. 设置 Photoshop 路径
2. 选择脚本目录
3. 添加 PSD 文件
4. 开始处理

## ⚠️ 常见问题

### 1. 杀毒软件拦截
**问题**：EXE 被杀毒软件误报为病毒

**解决**：
- 添加例外：将 EXE 文件添加到杀毒软件白名单
- 信任文件：右键文件 → 属性 → 解除锁定（如果有）
- 使用代码签名（高级）

### 2. 文件体积大
**问题**：打包后文件 60-80 MB

**原因**：包含 Python 运行时和所有依赖库

**说明**：这是正常的，PyInstaller 打包的 Python 程序都会比较大

### 3. 缺少 DLL
**问题**：运行时提示缺少 DLL 文件

**解决**：
- 确保在 Windows 10/11 上运行
- 安装 Visual C++ Redistributable
- 使用控制台模式查看详细错误

### 4. 脚本文件找不到
**问题**：找不到 JSX 脚本

**解决**：
- 确保脚本目录设置正确
- 检查 `scripts/production/` 目录是否存在
- 重新打包确保脚本文件被包含

## 🔧 手动打包（高级）

如果自动打包失败，可以手动打包：

### 1. 安装 PyInstaller
```bash
pip install pyinstaller
```

### 2. 执行打包命令
```bash
cd "F:\插件脚本开发\PSD Batch Processor"

pyinstaller ^
    --name="PSDBatchProcessor" ^
    --noconsole ^
    --add-data="src/app/config/config.json;app/config" ^
    --add-data="docs/guides/START_HERE.txt;docs/guides" ^
    --add-data="scripts/production/*.jsx;scripts/production" ^
    --hidden-import=win32com ^
    --hidden-import=pythoncom ^
    src/main.py
```

### 3. 获取结果
```
dist/PSDBatchProcessor/PSDBatchProcessor.exe
```

## 📊 打包对比

| 模式 | 文件大小 | 启动速度 | 便携性 | 适合场景 |
|------|----------|----------|--------|----------|
| 窗口模式 | 60-80 MB | 快 | 好 | 最终用户 |
| 控制台模式 | 60-80 MB | 快 | 好 | 调试 |
| 单文件模式 | 60-80 MB | 稍慢 | 极好 | 便携 |

## 🎨 添加图标（可选）

如果需要为 EXE 添加图标：

### 1. 准备图标文件
- 格式：.ico (Windows)
- 尺寸：256x256, 128x128, 64x64, 32x32, 16x16
- 位置：`assets/icon.ico`

### 2. 修改打包脚本
在 `tools/build.py` 或 `tools/build.bat` 中取消图标注释：

```python
# Python 脚本中
cmd.extend(["--icon=assets/icon.ico"])
```

```batch
:: 批处理中
--icon=assets/icon.ico
```

### 3. 重新打包

## 📋 打包检查清单

- [x] 安装 Python 3.10+
- [x] 安装 PyInstaller
- [x] 清理旧的构建文件
- [x] 选择合适的打包模式
- [x] 等待打包完成
- [x] 验证 EXE 文件存在
- [x] 测试运行 EXE
- [x] 检查自动创建的文件
- [x] 配置 Photoshop 路径
- [x] 测试批量处理功能

## 🚀 分发建议

### 1. 压缩打包
```bash
# 使用 7-Zip 或 WinRAR
# 压缩 dist/PSDBatchProcessor/ 文件夹
# 命名: PSDBatchProcessor_v1.0.zip
```

### 2. 创建发布说明
创建 `RELEASE_NOTES.txt`：
```
PSD Batch Processor v1.0

更新内容：
- 优化了批量处理性能
- 修复了进度条显示问题
- 移除了不必要的自动模式

使用说明：
1. 双击运行 PSDBatchProcessor.exe
2. 按照快速开始文档配置
3. 添加 PSD 文件并处理

详细文档：docs/guides/START_HERE.txt
```

### 3. 发布渠道
- **GitHub Releases**: 上传 ZIP 压缩包
- **百度网盘**: 分享下载链接
- **邮件发送**: 直接发送给用户

## 📚 相关文档

- **详细打包指南**: `docs/PACKAGING_GUIDE.md`
- **快速开始**: `docs/guides/START_HERE.txt`
- **项目结构**: `docs/project_structure.md`

## 💡 提示

### 开发阶段
- 使用控制台模式打包，便于调试
- 保留原始 Python 代码，方便修改

### 发布阶段
- 使用窗口模式打包，用户体验好
- 添加图标提升专业感
- 压缩后分发，减小文件体积

### 用户支持
- 提供详细的使用文档
- 准备常见问题解答
- 提供技术支持联系方式

---

**开始打包吧！** 🎉

运行 `python tools/build.py` 或 `tools\build.bat` 即可一键打包！