# Reports Directory

此目录用于存放自动生成的财务可视化报告。

## 目录结构

```
reports/
└── graphs/          # PNG格式的图表文件
```

## 生成的图表类型

### 1. 月度分类进展图 (Monthly Category Progression)
- 文件名: `月度分类进展_YYYYMMDD_HHMMSS.png`
- 显示各收入类别的月度趋势
- 6个子图显示不同收入来源

### 2. 每日场地进展图 (Daily Venue Progression)
- 文件名: `每日进展_场地_YYYYMMDD_HHMMSS.png`
- 显示场地收入的每日变化趋势
- 包含趋势线和关键数据点标注

### 3. 月度百分比分布图 (Monthly Percentage Distribution)
- 文件名: `月度百分比分布_YYYYMMDD_HHMMSS.png`
- 饼图显示各月份收入来源占比
- 网格布局便于对比

### 4. 统计分析图 (Statistical Analysis)
- 文件名: `统计分析_场地_YYYYMMDD_HHMMSS.png`
- 综合统计指标（平均值、中位数、标准差等）
- 箱线图、统计表格和对比柱状图

## 生成图表

```bash
# 生成所有图表
python3 generate_report.py --all

# 生成特定图表
python3 generate_report.py --stats     # 统计分析
python3 generate_report.py --monthly   # 月度分类进展
python3 generate_report.py --daily     # 每日进展
python3 generate_report.py --pies      # 百分比分布

# 交互式菜单
python3 generate_report.py
```

## 数据隐私

**注意**: `.gitignore` 已配置为忽略 `graphs/` 目录中的所有 `.png` 文件，因为这些图表包含真实的财务数据。

此目录本身和 README 文件会被提交到版本控制，但生成的图表不会。
