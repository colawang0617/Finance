# 📊 财务可视化系统使用指南
# Financial Visualization System Guide

## ✅ 已实现的功能

### 1. 月度分类进展图 (Monthly Category Progression)
**文件**: `visualizations/monthly_category.py`

**功能**: 生成6个面板的柱状图，显示6种收入类别的月度进展：
- 场地入账金额 (Venue Income)
- 云店销售 (Store Sales)
- 体验课 (Trial Class)
- 储值卡充值 (Card Topup)
- 私教课 (Private Coach)
- 月卡 (Monthly Card)

**特点**:
- ✅ 中文标签
- ✅ 每个柱上显示具体金额
- ✅ 自动从Excel读取最新数据
- ✅ PNG高清输出 (300 DPI)

---

### 2. 每日场地进展图 (Daily Venue Progression)
**文件**: `visualizations/daily_progression.py`

**功能**: 生成场地收入每日趋势线图，显示：
- 多月数据的连续趋势线
- 每月用不同颜色区分
- 平均线参考
- 关键数据点的金额标注

**特点**:
- ✅ 趋势线 + 数据标注（自动显示重要数据点）
- ✅ 月份分隔线和标签
- ✅ 平均值参考线
- ✅ 中文标签

---

### 3. 月度百分比分布图 (Monthly Percentage Distribution)
**文件**: `visualizations/monthly_pies.py`

**功能**: 生成饼图网格，显示每月场地收入的组成百分比：
- 美团 (Meituan)
- 储值卡核销 (Card Deduct)
- 抖音 (Douyin)
- 教练课核销 (Coach Fee)
- 微信 (WeChat)
- 支付宝 (Alipay)

**特点**:
- ✅ 每月一个饼图（最多6个月）
- ✅ 显示百分比和月度总额
- ✅ 彩色编码
- ✅ 完全中文标签

---

## 🚀 使用方法

### 方法1: 交互式菜单
```bash
python3 generate_report.py
```

然后按照菜单选择：
- 1 - 生成月度分类进展图
- 2 - 生成每日场地进展图
- 3 - 生成月度百分比分布图
- 4 - 生成所有图表
- 0 - 退出

---

### 方法2: 命令行参数
```bash
# 生成所有图表
python3 generate_report.py --all

# 只生成月度分类进展图
python3 generate_report.py --monthly

# 只生成每日进展图
python3 generate_report.py --daily

# 只生成百分比分布图
python3 generate_report.py --pies

# 指定月份范围 (例如: 只生成8-10月)
python3 generate_report.py --all --months 8,9,10
```

---

### 方法3: Python代码调用
```python
# 导入模块
from visualizations import monthly_category, daily_progression, monthly_pies

# 生成月度分类进展图 (5月到10月)
monthly_category.generate_monthly_category_chart(
    start_month=5,
    end_month=10
)

# 生成每日进展图 (只看10月)
daily_progression.generate_daily_progression(
    months=[10]
)

# 生成月度百分比分布图 (8-10月)
monthly_pies.generate_monthly_pies(
    months=[8, 9, 10]
)
```

---

## 📁 文件结构

```
Finance/
├── main.py                              # 每日数据录入
├── generate_report.py                   # 可视化生成器 ⭐
│
├── visualizations/                      # 可视化模块 ⭐
│   ├── __init__.py
│   ├── monthly_category.py              # 月度分类进展
│   ├── daily_progression.py             # 每日进展
│   └── monthly_pies.py                  # 月度百分比
│
├── reports/                             # 生成的报告
│   └── graphs/                          # 图表输出文件夹 ⭐
│       ├── 月度分类进展_YYYYMMDD_HHMMSS.png
│       ├── 每日进展_场地_YYYYMMDD_HHMMSS.png
│       └── 月度百分比分布_YYYYMMDD_HHMMSS.png
│
└── Finance/
    └── 财务跟踪表_完整版_KL.xlsx        # 数据源
```

---

## 🔄 自动更新机制

所有图表都**自动从Excel读取最新数据**：

1. 当你使用 `main.py` 添加新的每日数据后
2. 运行 `python3 generate_report.py --all`
3. 图表会自动包含新添加的数据

**无需手动更新任何配置！**

---

## 📸 输出示例

### 生成的文件命名规则：
- `月度分类进展_20251028_213707.png` - 月度分类进展图
- `每日进展_场地_20251028_213708.png` - 每日场地进展图
- `月度百分比分布_20251028_213708.png` - 月度百分比分布图

时间戳格式: `YYYYMMDD_HHMMSS`

---

## 🎨 自定义设置

### 修改月份范围
```python
# 在 generate_report.py 中修改默认月份
monthly_category.generate_monthly_category_chart(
    start_month=1,   # 从1月开始
    end_month=12     # 到12月结束
)
```

### 修改颜色
编辑对应的模块文件：
- `monthly_category.py` - 第105行：`categories` 列表中的颜色代码
- `daily_progression.py` - 第72行：`month_colors` 字典
- `monthly_pies.py` - 第94行：`colors` 列表

### 修改输出文件夹
```python
generate_monthly_category_chart(
    output_dir='custom/folder/path'
)
```

---

## 🔧 依赖库

已安装的必需库：
- ✅ `openpyxl` - Excel文件读取
- ✅ `matplotlib` - 图表生成
- ✅ `numpy` - 数值计算

---

## 📋 工作流程示例

### 典型的月度报告流程：

```bash
# 1. 整月录入数据
python3 main.py
# (输入10月1日的数据)
python3 main.py
# (输入10月2日的数据)
# ... 重复直到月底

# 2. 月底生成报告
python3 generate_report.py --all

# 3. 查看生成的图表
open reports/graphs/月度分类进展_*.png
open reports/graphs/每日进展_场地_*.png
open reports/graphs/月度百分比分布_*.png
```

---

## ⚠️ 注意事项

### 数据读取说明
- 图表生成器使用 `data_only=True` 读取Excel
- 这意味着它读取**计算后的值**，而不是公式
- 确保Excel文件在生成图表前被Excel打开并保存过一次（让公式计算）

### 首次使用
如果图表显示数据为空：
1. 用Excel打开 `财务跟踪表_完整版_KL.xlsx`
2. 按 `Cmd+S` 保存
3. 关闭Excel
4. 重新运行 `python3 generate_report.py --all`

### 中文字体
- 系统自动尝试使用中文字体
- macOS: Arial Unicode MS, Heiti TC
- 如果中文显示为方块，安装额外的中文字体

---

## 🎯 下一步计划 (可选扩展)

未来可以添加的功能：
- [ ] 统计分析图（直方图、箱线图）
- [ ] 百分比趋势线图
- [ ] 整体分布饼图
- [ ] 导出PDF格式
- [ ] 交互式HTML图表
- [ ] 自动发送邮件报告

---

## 📞 使用帮助

如需修改或添加新图表，请参考：
- `CLAUDE.md` - 项目总体说明
- `TECHNICAL_PLAN.md` - 技术规划
- 各模块文件的注释

---

**更新时间**: 2025-10-28
**版本**: v2.0
