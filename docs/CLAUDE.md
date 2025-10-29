# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a financial data automation tool for processing daily income reports in Chinese and updating an Excel-based financial tracking system. The tool parses structured Chinese text input containing daily sales data and automatically inserts it into an existing Excel workbook while preserving all formulas, formatting, and styling.

## Key Commands

### Development Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the main program
python main.py

# Run tests
python -m pytest tests/ -v
```

### Testing with Sample Data
```bash
# Test parser only
python -c "from parser import parse_daily_report; import sys; print(parse_daily_report(sys.stdin.read()))"

# Test with example file
python main.py < examples/sample_input.txt
```

## Architecture Overview

### Core Components

1. **Parser Module (`parser.py`)**
   - Extracts structured data from Chinese text input
   - Handles date parsing and conversion (e.g., "10月28日" → "10-28")
   - Maps Chinese field names to Excel column positions
   - Returns structured dictionary with all income categories

2. **Excel Handler Module (`excel_handler.py`)**
   - Manages Excel file operations using `openpyxl`
   - Inserts data into next available row in "每日数据" sheet
   - Preserves all cell styling (colors, fonts, borders)
   - Maintains Excel formulas for calculated fields
   - Never modifies existing data or formulas

3. **Main Program (`main.py`)**
   - Command-line interface for user input
   - Coordinates parser and Excel handler
   - Provides validation and error messages
   - Creates backup before modifications

### Data Flow

```
User Input (Chinese text)
    ↓
Parser (parse_daily_report)
    ↓
Structured Data Dictionary
    ↓
Excel Handler (insert_daily_data)
    ↓
Updated Excel File
```

## Excel File Structure

**File**: `Finance/财务跟踪表_完整版_KL.xlsx`

### Sheet: 每日数据 (Daily Data)

**Row Structure**:
- Row 1: Headers
- Row 2: Empty separator
- Row 3+: Daily data entries

**Column Mapping**:
```
A:  日期 (Date) - Format: MM-DD, e.g., "10-28"
B:  场地入账金额 (Venue Total) - FORMULA: =C+D+E+F+G+H
C:  大众美团 (Meituan)
D:  储值卡核销 (Stored Value Card Redemption)
E:  抖音 (Douyin)
F:  教练课核销 (Coaching Class Redemption)
G:  微信 (WeChat)
H:  支付宝 (Alipay)
I:  云店销售 (Online Store Total) - FORMULA: =J+K+L
J:  水 (Water)
K:  佳得乐 (Gatorade)
L:  其他 (Other)
M:  体验课 (Trial Classes)
N:  储值卡充值 (Stored Value Card Recharge)
O:  私教课充值 (Private Coaching Recharge)
P:  月卡 (Monthly Card)
Q:  每日销售合计 (Daily Sales Total) - FORMULA: =B+I+P
R:  当日总计 (Grand Total) - FORMULA: =B+I+M+N+O+P
```

**Styling Patterns** (MUST be preserved):
- Column A (Date): Purple background (#B4A7D6), white text, center aligned
- Columns B, I (Calculated venue/store): Dark blue background (#366092), yellow text
- Columns C-H (Venue subcategories): Light blue background (#5B9BD5), black text
- Columns J-L (Store items): Light blue background (#5B9BD5), blue text
- Columns M-P (Recharges/cards): Dark blue background (#366092), yellow text
- Columns Q-R (Totals): Light red background (#F4CCCC), red text
- All cells: Center aligned, Cambria/Calibri font, size 11

### Other Sheets
- **月度汇总 (Monthly Summary)**: Auto-calculated from 每日数据
- **总计 (Total)**: Overall totals from 每日数据

## Critical Rules

### DO NOT:
1. **Never modify existing rows** - Only append to next empty row
2. **Never change formulas** - Columns B, I, Q, R use specific formulas
3. **Never alter styling** - Each column has specific colors/fonts
4. **Never skip empty cells** - Use `None` for missing values, not 0
5. **Never modify other sheets** - Only touch "每日数据" sheet
6. **Never overwrite the Excel file without backup**

### ALWAYS:
1. **Find next empty row** by scanning from row 3 until `A{row}` is None
2. **Copy styling from previous row** for all cells
3. **Insert formulas** (not values) in columns B, I, Q, R
4. **Convert dates** from "X月Y日" to "MM-DD" format
5. **Validate input structure** before any Excel operations
6. **Create backup** before modifying Excel file

## Input Format Specification

Expected Chinese text format:
```
X月Y日销售日报
1. 场地入账金额: [number]
大众美团 [number]
储值卡核销 [number]
抖音 [number]
教练课核销 [number]
微信 [number]
支付宝 [number]
2.云店销售: [number]
水 [number]
佳得乐 [number]
其他 [number]
3.体验课: [number]
4. 储值卡充值: [number]
5. 私教课充值: [number]
6. 月卡: [number]
当日总计: [number]
```

- Empty fields may have no number (treated as None)
- "场地入账金额" total is ignored (Excel calculates)
- "云店销售" total is ignored (Excel calculates)
- "当日总计" can be used for validation but not inserted

## Error Handling

The tool must handle:
- Malformed Chinese input (missing sections, typos)
- Invalid dates (future dates, malformed)
- Duplicate dates (warn user, offer overwrite)
- Excel file locked/missing
- Corrupted Excel file

## Future Enhancements

Planned but not yet implemented:
- GUI interface (PyQt/Tkinter)
- Web interface (Flask/FastAPI)
- Batch processing from text files
- Date range validation
- Monthly report generation
- Data visualization
- Multi-user support
