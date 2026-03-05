# 构建和发布指南

## 🚀 快速开始

### 获取预编译版本（推荐）

直接从 GitHub Releases 下载：
https://github.com/yancongya/PSD-Batch-Processor/releases

## 📦 自动构建

### GitHub Actions 工作流

项目使用 GitHub Actions 实现自动化构建和发布。

#### 工作流特点

- **自动化**：推送标签时自动构建
- **多版本**：同时构建 Windowed、Console、OneFile
- **版本管理**：基于 Git 标签
- **一键发布**：自动创建 GitHub Release
- **持续集成**：确保构建质量

#### 触发构建

```bash
# 创建版本标签
git tag v1.0.1

# 推送标签，自动触发构建
git push origin v1.0.1
```

#### 构建流程

1. **检出代码**：获取最新代码
2. **设置环境**：配置 Python 3.13
3. **安装依赖**：安装 PyInstaller 和相关库
4. **构建版本**：
   - Windowed 模式（图形界面，推荐生产使用）
   - Console 模式（控制台，调试使用）
   - OneFile 模式（单文件，便携分发）
5. **打包发布**：创建 ZIP 包并发布到 GitHub Release

#### 构建产物

- `PSDBatchProcessor-vX.X.X.zip`：包含所有三个版本的完整包

#### 版本管理

版本号格式：`v{major}.{minor}.{patch}`

- `major`：重大更新
- `minor`：功能更新
- `patch`：Bug 修复

示例：
- `v1.0.0`：初始发布
- `v1.0.1`：Bug 修复
- `v1.1.0`：新功能
- `v2.0.0`：重大更新

#### 手动触发

如果需要手动触发构建：

1. 访问：https://github.com/yancongya/PSD-Batch-Processor/actions/workflows/build.yml
2. 点击 "Run workflow" 按钮
3. 选择分支并确认

#### 查看构建状态

- **GitHub Actions 页面**：https://github.com/yancongya/PSD-Batch-Processor/actions
- **Release 页面**：https://github.com/yancongya/PSD-Batch-Processor/releases
- **使用辅助脚本**：双击 `github_actions_helper.bat` 选择选项 2

## 🔧 手动构建

### 使用一键构建脚本

**Windows 用户**：
```batch
# 双击运行
tools\build.bat
```

**跨平台**：
```bash
# 运行 Python 脚本
python tools/build_all.py
```

### 本地测试构建

**Windows 用户**：
```batch
# 双击运行
test_build.bat
```

**跨平台**：
```bash
# 运行构建脚本
python .github/scripts/build.py
```

### PyInstaller 手动打包

详细说明请查看 [PACKAGING_GUIDE.md](PACKAGING_GUIDE.md)。

## 📊 构建优化

### 模块排除

为了减小构建体积，排除了以下不必要的模块：

```python
exclude_modules = [
    'torch', 'torchvision', 'torchaudio',  # PyTorch 相关
    'tensorflow', 'keras',                  # TensorFlow 相关
    'scipy', 'numpy', 'sympy',             # 科学计算
    'selenium', 'playwright',               # 网页自动化
    'pandas', 'matplotlib',                 # 数据分析
    'cv2', 'opencv-python',                 # 图像处理
    'langchain', 'openai', 'anthropic',    # AI 相关
]
```

**效果**：
- 构建时间：从 10-20 分钟减少到 1-2 分钟
- 文件大小：从 100+ MB 减少到 7-8 MB

### 数据文件

打包时包含以下数据文件：

```python
data_files = [
    'docs/guides/START_HERE.txt',
    'docs/guides/QUICK_REFERENCE.txt',
    'scripts/production/*.jsx',
    'scripts/templates/*.jsx',
    'scripts/examples/*.jsx',
]
```

### 隐藏导入

包含必要的隐藏导入：

```python
hidden_imports = [
    'win32com',      # Windows COM
    'pythoncom',     # Python COM
    'PIL',           # Pillow
    'customtkinter', # CustomTkinter
]
```

## 🛠️ 故障排除

### GitHub Actions 构建失败

#### 问题 1：403 权限错误

**错误信息**：
```
GitHub release failed with status: 403
```

**解决方案**：
确保工作流中包含权限设置：

```yaml
permissions:
  contents: write
```

#### 问题 2：找不到 src/main.py

**错误信息**：
```
ERROR: Script file 'src/main.py' does not exist.
```

**解决方案**：
检查 `.github/scripts/build.py` 中的项目根目录计算：

```python
script_file = Path(__file__).resolve()
project_root = script_file.parent.parent.parent  # 正确：三级父目录
```

#### 问题 3：文件路径不匹配

**错误信息**：
```
No files found to upload
```

**解决方案**：
确保工作流中的文件路径与构建产物匹配：

```yaml
- uses: softprops/action-gh-release@v1
  with:
    files: PSDBatchProcessor-*.zip
```

### 本地构建问题

#### 问题 1：PyInstaller 找不到模块

**解决方案**：
1. 检查依赖是否正确安装
2. 使用 `--hidden-import` 参数指定缺失的模块
3. 检查 Python 路径是否正确

#### 问题 2：打包体积过大

**解决方案**：
1. 添加 `--exclude-module` 参数排除不需要的模块
2. 使用 `--onefile` 模式（但启动会变慢）
3. 清理缓存：删除 `build/` 和 `dist/` 目录

## 📚 参考文档

- [README.md](../README.md) - 项目主文档
- [PACKAGING_GUIDE.md](PACKAGING_GUIDE.md) - 详细打包指南
- [FLUENT_VERSION_GUIDE.md](FLUENT_VERSION_GUIDE.md) - Fluent 版本指南
- [QUICK_REFERENCE.txt](guides/QUICK_REFERENCE.txt) - 快速参考

## 🤝 贡献

如果你发现构建或发布过程中的问题，欢迎提交 Issue 或 Pull Request！

## 📄 许可证

MIT License