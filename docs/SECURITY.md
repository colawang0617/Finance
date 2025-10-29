# 数据安全与隐私保护指南

## 概述

本项目已配置完整的数据隐私保护机制，确保您的真实财务数据不会被意外提交到 GitHub 或其他版本控制系统。

## 🔒 被保护的文件

以下文件和目录已通过 `.gitignore` 配置为**永不提交**：

### 1. Excel 数据文件
```
Finance/*.xlsx                      # 主数据文件
Finance/**/*.xlsx                   # 所有子目录中的Excel文件
Finance/.~*.xlsx                    # Excel临时文件
**/.~*.xlsx                         # 任何位置的Excel临时文件
```

**示例被保护的文件**:
- `Finance/财务跟踪表_完整版_KL.xlsx` (主数据文件)
- `Finance/财务跟踪表_完整版_KL_backup_*.xlsx` (所有备份)

### 2. 生成的图表报告
```
reports/graphs/*.png                # 所有PNG图表
```

**示例被保护的文件**:
- `reports/graphs/月度分类进展_*.png`
- `reports/graphs/每日进展_场地_*.png`
- `reports/graphs/月度百分比分布_*.png`
- `reports/graphs/统计分析_场地_*.png`

### 3. 环境配置文件
```
.env                                # 环境变量
.env.local                          # 本地环境变量
```

### 4. 系统与开发文件
```
__pycache__/                        # Python缓存
*.pyc, *.pyo, *.pyd                # Python编译文件
venv/, env/, ENV/                   # 虚拟环境
.DS_Store                           # macOS系统文件
.vscode/, .idea/                    # IDE配置
```

## ✅ 将被提交的文件

以下文件**会被提交**到版本控制：

```
✓ 所有Python源代码 (*.py)
✓ 文档文件 (*.md)
✓ 示例文件 (examples/)
✓ 测试文件 (tests/)
✓ 配置文件 (requirements.txt, .gitignore)
✓ 目录结构说明 (Finance/README.md, reports/README.md)
```

## 🔍 提交前验证

在首次 `git push` 前，请务必验证：

### 步骤 1: 检查被忽略的文件
```bash
git status --ignored
```

确认输出中的 "Ignored files" 部分包含：
- `Finance/财务跟踪表_完整版_KL.xlsx`
- `reports/graphs/*.png`

### 步骤 2: 检查将被提交的文件
```bash
git add .
git status
```

确认以下文件**不在**提交列表中：
- ❌ 任何 `.xlsx` 文件
- ❌ 任何 `.png` 图表文件
- ❌ `venv/` 目录

### 步骤 3: 查看将要提交的内容
```bash
git diff --cached --name-only
```

如果看到任何敏感文件，立即执行：
```bash
git reset
```

然后检查 `.gitignore` 配置。

## 🚨 紧急情况：如果已经提交敏感数据

如果不小心提交了敏感数据，立即执行：

### 1. 还未 push（数据只在本地）
```bash
# 撤销最后一次提交，保留文件
git reset --soft HEAD~1

# 从暂存区移除敏感文件
git reset Finance/*.xlsx
git reset reports/graphs/*.png

# 重新提交
git add .
git commit -m "Your commit message"
```

### 2. 已经 push 到远程
```bash
# ⚠️ 警告：这会改写历史，团队需要同步
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch Finance/*.xlsx" \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

**更安全的方法**：
1. 立即删除远程仓库
2. 修改 `.gitignore`
3. 重新创建干净的仓库
4. 重新提交

## 📋 最佳实践

### 开发流程
1. **修改代码前**：确认 `.gitignore` 正确
2. **提交前**：运行 `git status --ignored` 检查
3. **Push前**：再次确认没有敏感文件
4. **定期审查**：检查 `.gitignore` 是否需要更新

### 协作建议
1. **文档化**：确保团队成员了解哪些文件不应提交
2. **模板数据**：提供示例数据结构，不包含真实数据
3. **环境隔离**：使用 `.env` 文件管理敏感配置
4. **代码审查**：Pull Request 时检查是否包含敏感数据

### 备份策略
即使数据不会被提交到 Git：
1. 定期备份 `Finance/` 目录到安全位置
2. 使用加密云存储备份重要数据
3. 保留多个版本的备份

## 🛠️ 故障排查

### 问题：Excel 文件仍显示在 `git status` 中

**解决方案**：
```bash
# 清除已缓存的文件
git rm --cached Finance/*.xlsx
git commit -m "Remove cached xlsx files"

# 确认 .gitignore 正确配置
cat .gitignore | grep xlsx
```

### 问题：图表文件显示为未跟踪

**解决方案**：
```bash
# 确认图表文件被正确忽略
git check-ignore -v reports/graphs/*.png

# 如果未被忽略，检查 .gitignore
```

### 问题：意外提交了敏感文件

参见上面的"紧急情况"部分。

## 📞 支持

如有数据安全方面的问题：
1. 查看本文档
2. 检查 `.gitignore` 配置
3. 在提交前多次验证

**记住**：一旦敏感数据被 push 到公共仓库，即使删除也可能被他人下载。预防胜于补救！
