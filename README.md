# Financial Data Automation Tool

A command-line tool for automatically processing daily sales reports and updating Excel financial tracking spreadsheets.

## Features

- Parse Chinese-formatted sales reports
- Automatically populate Excel spreadsheet
- Preserve all cell formats and formulas
- Automatic backup creation
- Data validation
- Duplicate date detection

## Installation

### 1. Activate Virtual Environment

```bash
source venv/bin/activate
```

The virtual environment is pre-configured with all dependencies.

### 2. Verify Installation

Run tests to confirm everything is working:

```bash
python test_integration.py
```

You should see a message indicating all tests passed.

## Data Security and Privacy

**Important**: This project is pre-configured with a `.gitignore` file to protect your financial data privacy.

The following files and directories are **excluded** from Git commits:
- `Finance/*.xlsx` - Your actual financial data
- `Finance/*_backup_*.xlsx` - All backup files
- `reports/` - All generated charts (containing real data)
- `.env` - Environment configuration files

### Initial Setup

1. **Prepare Your Excel File**:
   - Place your Excel file in the `Finance/` directory
   - Ensure the filename matches the path in the code
   - Or modify the file path in the code to match your filename

2. **Excel File Structure**:
   - Must contain a worksheet named "每日数据" (Daily Data)
   - Column structure must follow the "Data Mapping" section in this README
   - Refer to project documentation for detailed table structure

3. **Verify .gitignore**:
   ```bash
   git status
   ```
   Ensure sensitive files are not being tracked.

## Usage

### Basic Usage

1. Run the program:

```bash
python main.py
```

2. Paste sales report text (format shown below)

3. Press `Ctrl+D` (Mac/Linux) or `Ctrl+Z` then `Enter` (Windows) to complete input

4. After confirming the data is correct, enter `Y` to confirm update

5. The program will automatically:
   - Validate data
   - Create backup
   - Update Excel file
   - Save changes

### Input Format

Sales reports must follow this format:

```
10月29日销售日报
1. 场地入账金额: 300
大众美团 50
储值卡核销 50
抖音 50
教练课核销 50
微信 50
支付宝 50
2.云店销售: 100
水 50
佳得乐 50
3.体验课: 50
4. 储值卡充值: 50 
5. 私教课充值: 50
6. 月卡: 50
当日总计: 600
```

**Notes:**
- First line must be in `X月Y日销售日报` format
- Empty fields can be left blank (program will record as no data)
- Numbers can be integers or decimals
- Values for "场地入账金额", "云店销售", "当日总计" are ignored (Excel auto-calculates)

## Project Structure

```
Finance/
├── 📊 Core Modules
│   ├── main.py                      # Daily data entry program
│   ├── parser.py                    # Chinese text parser
│   ├── excel_handler.py             # Excel file handler
│   ├── validator.py                 # Data validation
│   └── utils.py                     # Utility functions
│
├── 📈 Visualization System
│   ├── generate_report.py           # Report generator ⭐ New
│   └── visualizations/              # Visualization modules
│       ├── monthly_category.py      # Monthly category progress chart
│       ├── daily_progression.py     # Daily progression chart
│       └── monthly_pies.py          # Monthly percentage distribution charts
│
├── 📂 Data Files
│   └── Finance/
│       └── *.xlsx                   # Excel data files
│
├── 📄 Output Files
│   └── reports/
│       └── graphs/                  # Generated charts (PNG format)
│
├── 🛠️ Tools
│   └── tools/
│       └── update_monthly_formulas.py  # Monthly formula update tool
│
├── 🧪 Tests
│   └── tests/
│       └── test_integration.py      # Integration tests
│
├── 📚 Documentation
│   └── docs/
│       ├── CLAUDE.md                # Project description (for AI)
│       ├── TECHNICAL_PLAN.md        # Technical planning
│       ├── CHANGES_SUMMARY.md       # Changelog
│       └── VISUALIZATION_GUIDE.md   # Visualization guide ⭐
│
├── 📝 Examples
│   └── examples/
│       └── sample_input.txt         # Sample input data
│
└── requirements.txt                 # Python dependencies
```

## Running Examples

### Test with Sample File

```bash
python main.py < examples/sample_input.txt
```

Note: This will error due to user confirmation requirement, but you can see the parsing and validation process.

### Full Test (without modifying files)

```bash
python3 tests/test_integration.py
```

## Common Issues

### 1. Excel File in Use

**Error**: `Cannot access Excel file, please ensure the file is not being used by another program`

**Solution**: Close Excel or other programs using the file.

### 2. Date Already Exists

**Message**: `Date 10-28 already exists at row X`

**Explanation**: The program detected existing data for this date. You can:
- Overwrite (will actually add a new row)
- Cancel operation

### 3. Parse Failure

**Error**: `Date information not found`

**Solution**: Confirm first line format is `X月Y日销售日报`, e.g., `10月28日销售日报`.

### 4. Data Validation Failure

**Error**: `Field X value cannot be negative`

**Solution**: Check input numbers, ensure no negative or invalid values.

## Backups

The program automatically creates backup files before each update in the format:

```
*_backup_YYYYMMDD_HHMMSS.xlsx
```

Example: `财务跟踪表_完整版_KL_backup_20251028_143025.xlsx`

Backup files are saved in the same directory as the original file.

## Data Mapping

The program maps the following Chinese fields to corresponding Excel columns:

| Chinese Field | Excel Column | Description |
|--------------|--------------|-------------|
| 日期 | A | MM-DD format |
| 大众美团 | C | Meituan revenue |
| 储值卡核销 | D | Stored value card usage |
| 抖音 | E | Douyin revenue |
| 教练课核销 | F | Coach class usage |
| 微信 | G | WeChat revenue |
| 支付宝 | H | Alipay revenue |
| 水 | J | Water sales |
| 佳得乐 | K | Gatorade sales |
| 其他 | L | Other items |
| 体验课 | M | Trial class revenue |
| 储值卡充值 | N | Stored value card recharge |
| 私教课充值 | O | Private training recharge |
| 月卡 | P | Monthly card sales |

**Auto-calculated columns** (no input needed):
- Column B: Venue revenue = C+D+E+F+G+H
- Column I: Store sales = J+K+L
- Column Q: Daily sales total = B+I+P
- Column R: Daily grand total = B+I+M+N+O+P

## Important Notes

1. **Don't manually modify Excel file structure** - The program depends on specific column layouts and formulas
2. **Regular backups** - While the program auto-creates backups, manual backups of important files are recommended
3. **Data validation** - The program validates data format, but human verification of value accuracy is still needed
4. **Date format** - Currently only supports MM-DD format, using current year

## Technical Support

For issues, please:
1. Check `docs/CLAUDE.md` for technical details
2. Check `docs/TECHNICAL_PLAN.md` for system architecture
3. Check `docs/VISUALIZATION_GUIDE.md` for visualization features
4. Run `python3 tests/test_integration.py` for diagnostics

## 🎨 Visualization Features ⭐ New

### Generate Financial Report Charts

The report generator now **automatically detects** which months have data in your Excel file!

```bash
# Generate all charts (auto-detects available months)
python3 generate_report.py --all

# Interactive menu (shows detected month range)
python3 generate_report.py

# Generate specific charts (auto-detects months)
python3 generate_report.py --monthly  # Monthly category progress chart
python3 generate_report.py --daily    # Daily progression chart
python3 generate_report.py --pies     # Monthly percentage distribution charts
python3 generate_report.py --stats    # Statistical analysis ⭐

# Manually specify month range (optional)
python3 generate_report.py --all --months 8,9,10,11
```

**Smart Month Detection:**
- Automatically includes all months with data (May-November currently)
- Will automatically include December when December data is added
- No need to update code when adding new months!

**Detailed usage**: See `docs/VISUALIZATION_GUIDE.md`

---

## 💻 Quick Command Reference

```bash
# Data Entry
python3 main.py                        # Add daily data

# Visualization Reports
python3 generate_report.py --all      # Generate all charts
python3 generate_report.py            # Interactive menu

# Tools and Maintenance
python3 tools/update_monthly_formulas.py  # Update monthly formulas
python3 tests/test_integration.py         # Run tests
```

---

## Future Features

Planned features:
- Batch processing of multiple reports
- Graphical User Interface (GUI)
- Web interface
- More statistical analysis charts
- PDF report export

---

Version: 2.0
Last Updated: October 28, 2025

