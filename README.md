# 财务数据自动化工具

自动处理每日销售日报并更新Excel财务跟踪表的命令行工具。

## 功能特点

- 解析中文格式的销售日报
- 自动填充Excel表格
- 保留所有单元格格式和公式
- 自动创建备份
- 数据验证
- 重复日期检测

## 安装

### 1. 激活虚拟环境

```bash
source venv/bin/activate
```

虚拟环境已预先配置好所有依赖包。

### 2. 验证安装

运行测试以确认一切正常:

```bash
python test_integration.py
```

应该看到所有测试通过的消息。

## 数据安全与隐私

**重要**: 本项目默认配置了 `.gitignore` 文件以保护您的财务数据隐私。

以下文件和目录**不会**被提交到 Git：
- `Finance/财务跟踪表_完整版_KL.xlsx` - 您的真实财务数据
- `Finance/*_backup_*.xlsx` - 所有备份文件
- `reports/` - 所有生成的图表（包含真实数据）
- `.env` - 环境变量配置文件

### 首次设置

1. **准备您的Excel文件**:
   - 将您的Excel文件放在 `Finance/` 目录下
   - 确保文件名为 `财务跟踪表_完整版_KL.xlsx`
   - 或修改代码中的文件路径以匹配您的文件名

2. **Excel文件结构**:
   - 必须包含名为 "每日数据" 的工作表
   - 列结构必须符合本README中"数据映射"部分的说明
   - 可参考项目文档了解详细的表格结构

3. **验证 .gitignore**:
   ```bash
   git status
   ```
   确保敏感文件未被跟踪。

## 使用方法

### 基本使用

1. 运行程序:

```bash
python main.py
```

2. 粘贴销售日报文本（格式见下方）

3. 按 `Ctrl+D` (Mac/Linux) 或 `Ctrl+Z` 然后 `Enter` (Windows) 完成输入

4. 确认数据无误后，输入 `Y` 确认更新

5. 程序会自动:
   - 验证数据
   - 创建备份
   - 更新Excel文件
   - 保存更改

### 输入格式

销售日报必须遵循以下格式:

```
10月28日销售日报
1. 场地入账金额: 739
大众美团 144
储值卡核销 505
抖音
教练课核销 90
微信
支付宝
2.云店销售:
水
佳得乐
3.体验课:
4. 储值卡充值: 1000
5. 私教课充值:
6. 月卡:
当日总计: 1739
```

**注意:**
- 第一行必须是 `X月Y日销售日报` 格式
- 空字段留空即可（程序会记录为无数据）
- 数字可以是整数或小数
- "场地入账金额"、"云店销售"、"当日总计" 的数值会被忽略（Excel自动计算）

## 文件结构

```
Finance/
├── 📊 核心模块 (Core Modules)
│   ├── main.py                      # 每日数据录入程序
│   ├── parser.py                    # 中文文本解析器
│   ├── excel_handler.py             # Excel文件处理
│   ├── validator.py                 # 数据验证
│   └── utils.py                     # 工具函数
│
├── 📈 可视化系统 (Visualization System)
│   ├── generate_report.py           # 报告生成器 ⭐新功能
│   └── visualizations/              # 可视化模块
│       ├── monthly_category.py      # 月度分类进展图
│       ├── daily_progression.py     # 每日进展图
│       └── monthly_pies.py          # 月度百分比分布图
│
├── 📂 数据文件 (Data Files)
│   └── Finance/
│       └── 财务跟踪表_完整版_KL.xlsx  # Excel数据文件
│
├── 📄 输出文件 (Output Files)
│   └── reports/
│       └── graphs/                  # 生成的图表 (PNG格式)
│
├── 🛠️ 工具脚本 (Tools)
│   └── tools/
│       └── update_monthly_formulas.py  # 更新月度公式工具
│
├── 🧪 测试文件 (Tests)
│   └── tests/
│       └── test_integration.py      # 集成测试
│
├── 📚 文档 (Documentation)
│   └── docs/
│       ├── CLAUDE.md                # 项目说明 (给AI)
│       ├── TECHNICAL_PLAN.md        # 技术规划
│       ├── CHANGES_SUMMARY.md       # 更新日志
│       └── VISUALIZATION_GUIDE.md   # 可视化使用指南 ⭐
│
├── 📝 示例文件 (Examples)
│   └── examples/
│       └── sample_input.txt         # 示例输入数据
│
└── requirements.txt                 # Python依赖
```

## 运行示例

### 使用示例文件测试

```bash
python main.py < examples/sample_input.txt
```

注意: 由于需要用户确认，这种方式会报错，但可以看到解析和验证过程。

### 完整测试（不修改文件）

```bash
python3 tests/test_integration.py
```

## 常见问题

### 1. Excel文件被占用

**错误**: `无法访问Excel文件，请确认文件未被其他程序占用`

**解决**: 关闭Excel或其他正在使用该文件的程序。

### 2. 日期已存在

**提示**: `日期 10-28 已存在于第 X 行`

**说明**: 程序检测到该日期已有数据，可以选择:
- 覆盖（实际会添加新行）
- 取消操作

### 3. 解析失败

**错误**: `未找到日期信息`

**解决**: 确认第一行格式为 `X月Y日销售日报`，例如 `10月28日销售日报`。

### 4. 数据验证失败

**错误**: `字段 X 的值不能为负数`

**解决**: 检查输入的数字，确保没有负数或无效值。

## 备份

程序会在每次更新前自动创建备份文件，格式为:

```
财务跟踪表_完整版_KL_backup_YYYYMMDD_HHMMSS.xlsx
```

例如: `财务跟踪表_完整版_KL_backup_20251028_143025.xlsx`

备份文件保存在与原文件相同的目录下。

## 数据映射

程序将以下中文字段映射到Excel的对应列:

| 中文字段 | Excel列 | 说明 |
|---------|---------|------|
| 日期 | A | MM-DD格式 |
| 大众美团 | C | 美团收入 |
| 储值卡核销 | D | 储值卡使用 |
| 抖音 | E | 抖音收入 |
| 教练课核销 | F | 教练课使用 |
| 微信 | G | 微信收入 |
| 支付宝 | H | 支付宝收入 |
| 水 | J | 水销售 |
| 佳得乐 | K | 佳得乐销售 |
| 其他 | L | 其他商品 |
| 体验课 | M | 体验课收入 |
| 储值卡充值 | N | 储值卡充值 |
| 私教课充值 | O | 私教课充值 |
| 月卡 | P | 月卡销售 |

**自动计算列** (不需要输入):
- 列B: 场地入账金额 = C+D+E+F+G+H
- 列I: 云店销售 = J+K+L
- 列Q: 每日销售合计 = B+I+P
- 列R: 当日总计 = B+I+M+N+O+P

## 注意事项

1. **不要手动修改Excel文件结构** - 程序依赖于特定的列布局和公式
2. **定期备份** - 虽然程序会自动创建备份，但建议定期手动备份重要文件
3. **数据验证** - 程序会验证数据格式，但仍需人工确认数值准确性
4. **日期格式** - 目前仅支持 MM-DD 格式，使用当前年份

## 技术支持

如有问题，请:
1. 查看 `docs/CLAUDE.md` 了解技术细节
2. 查看 `docs/TECHNICAL_PLAN.md` 了解系统架构
3. 查看 `docs/VISUALIZATION_GUIDE.md` 了解可视化功能
4. 运行 `python3 tests/test_integration.py` 进行诊断

## 🎨 可视化功能 ⭐新功能

### 生成财务报告图表

```bash
# 生成所有图表
python3 generate_report.py --all

# 交互式菜单
python3 generate_report.py

# 生成特定图表
python3 generate_report.py --monthly  # 月度分类进展图
python3 generate_report.py --daily    # 每日进展图
python3 generate_report.py --pies     # 月度百分比分布图

# 指定月份范围
python3 generate_report.py --all --months 8,9,10
```

**详细使用说明**: 参见 `docs/VISUALIZATION_GUIDE.md`

---

## 💻 常用命令速查

```bash
# 数据录入
python3 main.py                        # 添加每日数据

# 可视化报告
python3 generate_report.py --all      # 生成所有图表
python3 generate_report.py            # 交互式菜单

# 工具和维护
python3 tools/update_monthly_formulas.py  # 更新月度公式
python3 tests/test_integration.py         # 运行测试
```

---

## 未来功能

计划中的功能:
- 批量处理多个日报
- 图形用户界面 (GUI)
- Web界面
- 更多统计分析图表
- PDF报告导出

---

版本: 2.0
最后更新: 2025年10月28日

