# Data Security and Privacy Protection Guide

## Overview

This project has a complete data privacy protection mechanism configured to ensure your real financial data will not be accidentally committed to GitHub or other version control systems.

## 🔒 Protected Files

The following files and directories are configured via `.gitignore` to **never be committed**:

### 1. Excel Data Files
```
Finance/*.xlsx                      # Main data files
Finance/**/*.xlsx                   # Excel files in all subdirectories
Finance/.~*.xlsx                    # Excel temporary files
**/.~*.xlsx                         # Excel temp files anywhere
```

**Examples of protected files**:
- `Finance/财务跟踪表_完整版_KL.xlsx` (main data file)
- `Finance/财务跟踪表_完整版_KL_backup_*.xlsx` (all backups)

### 2. Generated Chart Reports
```
reports/graphs/*.png                # All PNG charts
```

**Examples of protected files**:
- `reports/graphs/月度分类进展_*.png`
- `reports/graphs/每日进展_场地_*.png`
- `reports/graphs/月度百分比分布_*.png`
- `reports/graphs/统计分析_场地_*.png`

### 3. Environment Configuration Files
```
.env                                # Environment variables
.env.local                          # Local environment variables
```

### 4. System and Development Files
```
__pycache__/                        # Python cache
*.pyc, *.pyo, *.pyd                # Python compiled files
venv/, env/, ENV/                   # Virtual environments
.DS_Store                           # macOS system files
.vscode/, .idea/                    # IDE configurations
```

## ✅ Files That Will Be Committed

The following files **will be committed** to version control:

```
✓ All Python source code (*.py)
✓ Documentation files (*.md)
✓ Example files (examples/)
✓ Test files (tests/)
✓ Configuration files (requirements.txt, .gitignore)
✓ Directory structure documentation (Finance/README.md, reports/README.md)
```

## 🔍 Pre-Commit Verification

Before your first `git push`, you must verify:

### Step 1: Check Ignored Files
```bash
git status --ignored
```

Confirm that the "Ignored files" section includes:
- `Finance/财务跟踪表_完整版_KL.xlsx`
- `reports/graphs/*.png`

### Step 2: Check Files To Be Committed
```bash
git add .
git status
```

Confirm that the following files are **NOT** in the commit list:
- ❌ Any `.xlsx` files
- ❌ Any `.png` chart files
- ❌ `venv/` directory

### Step 3: View What Will Be Committed
```bash
git diff --cached --name-only
```

If you see any sensitive files, immediately execute:
```bash
git reset
```

Then check your `.gitignore` configuration.

## 🚨 Emergency: If Sensitive Data Already Committed

If you accidentally committed sensitive data, immediately execute:

### 1. Not Yet Pushed (data only local)
```bash
# Undo last commit, keep files
git reset --soft HEAD~1

# Remove sensitive files from staging area
git reset Finance/*.xlsx
git reset reports/graphs/*.png

# Recommit
git add .
git commit -m "Your commit message"
```

### 2. Already Pushed to Remote
```bash
# ⚠️ Warning: This rewrites history, team needs to sync
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch Finance/*.xlsx" \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

**Safer Method**:
1. Immediately delete the remote repository
2. Fix `.gitignore`
3. Recreate a clean repository
4. Recommit

## 📋 Best Practices

### Development Workflow
1. **Before modifying code**: Confirm `.gitignore` is correct
2. **Before committing**: Run `git status --ignored` to check
3. **Before pushing**: Verify again that no sensitive files are included
4. **Regular reviews**: Check if `.gitignore` needs updates

### Collaboration Guidelines
1. **Documentation**: Ensure team members know which files should not be committed
2. **Template data**: Provide example data structures without real data
3. **Environment isolation**: Use `.env` files to manage sensitive configurations
4. **Code review**: Check for sensitive data in Pull Requests

### Backup Strategy
Even though data won't be committed to Git:
1. Regularly backup `Finance/` directory to a secure location
2. Use encrypted cloud storage for important data backups
3. Keep multiple versions of backups

## 🛠️ Troubleshooting

### Issue: Excel files still showing in `git status`

**Solution**:
```bash
# Clear cached files
git rm --cached Finance/*.xlsx
git commit -m "Remove cached xlsx files"

# Verify .gitignore is correctly configured
cat .gitignore | grep xlsx
```

### Issue: Chart files showing as untracked

**Solution**:
```bash
# Verify chart files are correctly ignored
git check-ignore -v reports/graphs/*.png

# If not ignored, check .gitignore
```

### Issue: Accidentally committed sensitive files

Refer to the "Emergency" section above.

## 📞 Support

If you have data security questions:
1. Review this document
2. Check `.gitignore` configuration
3. Verify multiple times before committing

**Remember**: Once sensitive data is pushed to a public repository, it may be downloaded by others even after deletion. Prevention is better than cure!
