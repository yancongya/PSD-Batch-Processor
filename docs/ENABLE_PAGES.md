# GitHub Pages 启用指南

## 问题说明

当前错误：
```
Error: Get Pages site failed. Please verify that the repository has Pages enabled and configured to build using GitHub Actions
```

这意味着 GitHub Pages 还没有在仓库中启用。

## 解决步骤

### 方法 1：通过 GitHub 网页界面启用（推荐）

1. **访问仓库设置**
   - 打开：https://github.com/yancongya/PSD-Batch-Processor/settings
   - 或者：在仓库页面点击 "Settings" 标签

2. **找到 Pages 设置**
   - 在左侧菜单中，向下滚动找到 "Code and automation" 部分
   - 点击 "Pages"

3. **配置 GitHub Pages**
   - **Source**: 选择 "GitHub Actions"
   - **Build and deployment**: 确保选择 "GitHub Actions"
   - 点击 "Save" 保存设置

4. **等待激活**
   - GitHub 会自动创建 Pages 站点
   - 通常需要 1-2 分钟

5. **验证部署**
   - 访问：https://github.com/yancongya/PSD-Batch-Processor/actions
   - 查看 "Deploy to GitHub Pages" 工作流是否成功运行

### 方法 2：使用 GitHub CLI（如果已安装）

如果你已经安装了 GitHub CLI，可以使用以下命令：

```bash
# 启用 GitHub Pages
gh api -X POST repos/yancongya/PSD-Batch-Processor/pages \
  -f source='{
    "type": "github_actions"
  }'

# 验证设置
gh api repos/yancongya/PSD-Batch-Processor/pages
```

## 部署工作流

一旦 GitHub Pages 启用，工作流会自动运行：

**工作流文件**：`.github/workflows/deploy-pages.yml`

**触发条件**：
- 推送到 master 分支（自动触发）
- 手动触发（workflow_dispatch）

**部署内容**：
- 使用 `index.html` 作为主页
- 包含所有项目文件
- 自动部署到 GitHub Pages

## 访问地址

启用后，可以通过以下地址访问：

**主地址**：
https://yancongya.github.io/PSD-Batch-Processor/

**备用地址**（如果主地址不可用）：
https://yancongya.github.io/PSD-Batch-Processor/index.html

## 常见问题

### Q: 启用后仍然看不到网站？

**A**: GitHub Pages 部署需要时间，通常需要 1-5 分钟。请耐心等待并检查 Actions 页面查看部署状态。

### Q: 如何更新网站内容？

**A**: 直接修改 `index.html` 或其他文件，然后推送到 master 分支。GitHub Actions 会自动重新部署。

### Q: 如何查看部署日志？

**A**: 访问 https://github.com/yancongya/PSD-Batch-Processor/actions，查看 "Deploy to GitHub Pages" 工作流的运行日志。

### Q: 网站显示 404 错误？

**A**: 
1. 确认 GitHub Pages 已启用
2. 检查 Actions 工作流是否成功运行
3. 等待 DNS 传播（最多 24 小时）
4. 清除浏览器缓存后重试

## 验证步骤

启用 GitHub Pages 后，按以下步骤验证：

1. **检查 Actions 页面**
   - 访问：https://github.com/yancongya/PSD-Batch-Processor/actions
   - 确认 "Deploy to GitHub Pages" 工作流运行成功

2. **访问网站**
   - 打开：https://yancongya.github.io/PSD-Batch-Processor/
   - 检查是否能看到产品主页

3. **检查源代码**
   - 在浏览器中右键点击页面
   - 选择"查看页面源代码"
   - 确认内容与 `index.html` 一致

## 后续维护

### 更新网站

只需修改相关文件并推送：

```bash
# 修改文件
vim index.html

# 提交更改
git add index.html
git commit -m "更新网站内容"
git push
```

### 查看部署状态

```bash
# 使用 GitHub CLI
gh run list --workflow=deploy-pages.yml

# 或者访问网页
# https://github.com/yancongya/PSD-Batch-Processor/actions
```

## 相关链接

- [GitHub Pages 官方文档](https://docs.github.com/pages)
- [GitHub Actions 文档](https://docs.github.com/actions)
- [仓库主页](https://github.com/yancongya/PSD-Batch-Processor)
- [Actions 页面](https://github.com/yancongya/PSD-Batch-Processor/actions)