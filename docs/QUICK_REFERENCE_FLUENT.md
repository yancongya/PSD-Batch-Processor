# PyQt-Fluent-Widgets 版本快速参考

## 🚀 快速启动

### 首次使用
```bash
# 1. 安装依赖
python tools\install_fluent.py

# 2. 启动应用
python tools\run_fluent.py
```

### 日常使用
```bash
python tools\run_fluent.py
```

## 📋 常用操作

### 添加文件
- **添加单个文件**: 点击"添加文件" → 选择 PSD 文件
- **添加文件夹**: 点击"添加文件夹" → 选择包含 PSD 的文件夹
- **清空列表**: 点击"清空"按钮

### 选择脚本
1. 点击"刷新"按钮扫描脚本
2. 从下拉框选择脚本
3. 脚本会自动扫描 `scripts/` 及其子目录

### 开始处理
1. 设置 Photoshop 路径（首次需要）
2. 选择脚本
3. 添加文件
4. 点击"开始处理"

### 查看日志
- **预览日志**: 主页底部
- **完整日志**: 点击侧边栏"日志"
- **保存日志**: 日志页面 → "保存日志"

## ⚙️ 设置选项

### 主题切换
- **位置**: 设置页面 → 主题设置
- **选项**: 深色 / 浅色
- **即时生效**: 无需重启

### 路径设置
- **脚本目录**: 默认 `scripts/`，可自定义
- **备份目录**: 默认 `backups/`，可自定义
- **保存**: 点击"保存设置"按钮

### 并发数
- **范围**: 1-8
- **推荐**:
  - 低配电脑: 1-2
  - 中配电脑: 2-4
  - 高配电脑: 4-8

## 🔧 问题解决

### 无法启动
```bash
# 检查依赖
python tests\test_fluent_widgets.py

# 重新安装
pip install PyQt5 PyQt-Fluent-Widgets pywin32
```

### 脚本找不到
1. 点击"刷新"按钮
2. 检查脚本目录设置
3. 确保脚本扩展名为 `.jsx`

### Photoshop 无法启动
1. 检查路径是否正确
2. 确保 Photoshop 已安装
3. 以管理员权限运行

## 📁 文件位置

### 配置文件
- **开发**: `src/config.json`
- **打包后**: `%APPDATA%\PSDBatchProcessor\config.json`

### 脚本目录
- **默认**: `scripts/`
- **子目录**: `production/`, `templates/`, `examples/`

### 备份目录
- **默认**: `backups/`
- **格式**: `backups/YYYYMMDD_HHMMSS/`

## 🎯 版本对比

| 特性 | CustomTkinter | PyQt-Fluent-Widgets |
|------|---------------|---------------------|
| 界面 | 简洁现代 | Fluent Design |
| 启动 | 快 (1-2秒) | 中等 (2-3秒) |
| 依赖 | 小 (~50MB) | 大 (~80MB) |
| 导航 | 单页面 | 多页面 |
| 推荐 | 轻量级需求 | 追求美观 |

## 📞 获取帮助

### 查看文档
- **完整指南**: `docs/FLUENT_VERSION_GUIDE.md`
- **主文档**: `README.md`
- **快速开始**: `docs/guides/START_HERE.txt`

### 测试脚本
```bash
# 测试依赖
python tests\test_fluent_widgets.py

# 测试环境
python tests\test_env.py
```

## 💡 小贴士

1. **首次使用**: 先安装依赖，再启动应用
2. **脚本管理**: 定期刷新脚本列表
3. **备份习惯**: 定期清理旧备份文件
4. **性能优化**: 根据电脑配置调整并发数
5. **日志保存**: 重要操作后保存日志

---

**版本**: 1.0.0
**更新**: 2026-01-24