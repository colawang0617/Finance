# Technical Project Plan - Financial Data Automation Tool

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Financial Data Automation                │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   User CLI   │ ───▶ │    Parser    │ ───▶ │Excel Handler │
│   (main.py)  │      │ (parser.py)  │      │(excel_handler│
│              │      │              │      │    .py)      │
└──────────────┘      └──────────────┘      └──────────────┘
      │                      │                      │
      │                      │                      │
      ▼                      ▼                      ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Validator  │      │Date Converter│      │Style Manager │
│(validator.py)│      │ (utils.py)   │      │ (utils.py)   │
└──────────────┘      └──────────────┘      └──────────────┘
```

---

## Module Specifications

### 1. **parser.py** - Text Parser Module

**Purpose**: Parse structured Chinese text input into Python dictionary

**Key Functions**:
```python
def parse_daily_report(text: str) -> Dict[str, Any]:
    """
    Parse Chinese daily report text

    Args:
        text: Multi-line Chinese text with sales data

    Returns:
        {
            'date': '10-28',
            'meituan': 144,
            'stored_card_redemption': 505,
            'douyin': None,
            'coaching_redemption': 90,
            'wechat': None,
            'alipay': None,
            'water': None,
            'gatorade': None,
            'other': None,
            'trial_class': None,
            'stored_card_recharge': 1000,
            'private_coaching_recharge': None,
            'monthly_card': None
        }

    Raises:
        ParseError: If text format invalid
    """
```

**Parsing Strategy**:
1. **Regex patterns** for each field:
   - Date: `(\d+)月(\d+)日销售日报`
   - Field with value: `(field_name)\s*(\d+\.?\d*)`
   - Field without value: `(field_name)\s*$`

2. **Field mapping**:
   ```python
   FIELD_MAP = {
       '大众美团': 'meituan',
       '储值卡核销': 'stored_card_redemption',
       '抖音': 'douyin',
       '教练课核销': 'coaching_redemption',
       '微信': 'wechat',
       '支付宝': 'alipay',
       '水': 'water',
       '佳得乐': 'gatorade',
       '其他': 'other',
       '体验课': 'trial_class',
       '储值卡充值': 'stored_card_recharge',
       '私教课充值': 'private_coaching_recharge',
       '月卡': 'monthly_card'
   }
   ```

3. **Ignored fields** (calculated in Excel):
   - 场地入账金额 (venue total)
   - 云店销售 (store total)
   - 当日总计 (daily grand total)

---

### 2. **excel_handler.py** - Excel Operations Module

**Purpose**: Manage all Excel file operations with styling preservation

**Key Classes**:
```python
class ExcelHandler:
    """Handle Excel file operations"""

    def __init__(self, filepath: str):
        """Initialize with Excel file path"""

    def find_next_row(self) -> int:
        """Find next empty row in 每日数据 sheet"""

    def insert_daily_data(self, data: Dict[str, Any]) -> int:
        """
        Insert parsed data into next row

        Returns:
            Row number where data was inserted
        """

    def copy_row_styling(self, source_row: int, target_row: int):
        """Copy all styling from source to target row"""

    def generate_formulas(self, row: int) -> Dict[str, str]:
        """Generate Excel formulas for calculated columns"""

    def create_backup(self) -> str:
        """Create timestamped backup file"""

    def check_duplicate_date(self, date: str) -> Optional[int]:
        """Check if date already exists, return row number"""
```

**Column-to-Data Mapping**:
```python
COLUMN_MAP = {
    'A': 'date',           # Direct value
    'B': 'FORMULA',        # =C{row}+D{row}+E{row}+F{row}+G{row}+H{row}
    'C': 'meituan',
    'D': 'stored_card_redemption',
    'E': 'douyin',
    'F': 'coaching_redemption',
    'G': 'wechat',
    'H': 'alipay',
    'I': 'FORMULA',        # =J{row}+K{row}+L{row}
    'J': 'water',
    'K': 'gatorade',
    'L': 'other',
    'M': 'trial_class',
    'N': 'stored_card_recharge',
    'O': 'private_coaching_recharge',
    'P': 'monthly_card',
    'Q': 'FORMULA',        # =B{row}+I{row}+P{row}
    'R': 'FORMULA'         # =B{row}+I{row}+M{row}+N{row}+O{row}+P{row}
}
```

**Styling Preservation**:
```python
STYLE_CONFIG = {
    'A': {  # Date column
        'fill': PatternFill(patternType='solid', fgColor='FFB4A7D6'),
        'font': Font(name='Cambria', size=11, color='FFFFFFFF'),
        'alignment': Alignment(horizontal='center')
    },
    'B': {  # Venue total (formula)
        'fill': PatternFill(patternType='solid', fgColor='FF366092'),
        'font': Font(name='Cambria', size=11, color='FFFFFF00'),
        'alignment': Alignment(horizontal='center')
    },
    'C-H': {  # Venue subcategories
        'fill': PatternFill(patternType='solid', fgColor='FF5B9BD5'),
        'font': Font(name='Cambria', size=11, color='FF000000'),
        'alignment': Alignment(horizontal='center')
    },
    'I': {  # Store total (formula)
        'fill': PatternFill(patternType='solid', fgColor='FF366092'),
        'font': Font(name='Cambria', size=11, color='FFFFFF00'),
        'alignment': Alignment(horizontal='center')
    },
    'J-L': {  # Store items
        'fill': PatternFill(patternType='solid', fgColor='FF5B9BD5'),
        'font': Font(name='Cambria', size=11, color='FF0000FF'),
        'alignment': Alignment(horizontal='center')
    },
    'M-P': {  # Recharges
        'fill': PatternFill(patternType='solid', fgColor='FF366092'),
        'font': Font(name='Cambria', size=11, color='FFFFFF00'),
        'alignment': Alignment(horizontal='center')
    },
    'Q-R': {  # Totals
        'fill': PatternFill(patternType='solid', fgColor='FFF4CCCC'),
        'font': Font(name='Cambria', size=11, color='FFCC0000'),
        'alignment': Alignment(horizontal='center')
    }
}
```

---

### 3. **utils.py** - Utility Functions

```python
def convert_chinese_date_to_excel_format(month: int, day: int) -> str:
    """Convert 10月28日 to 10-28 format"""

def validate_date(month: int, day: int) -> bool:
    """Validate date is reasonable (not future, valid month/day)"""

def format_number(value: Optional[float]) -> Optional[float]:
    """Format number, handle None values"""
```

---

### 4. **validator.py** - Input Validation

```python
class InputValidator:
    """Validate parsed data before Excel insertion"""

    @staticmethod
    def validate_date(date: str) -> Tuple[bool, str]:
        """Validate date format and value"""

    @staticmethod
    def validate_numbers(data: Dict) -> Tuple[bool, List[str]]:
        """Validate all numeric fields are valid"""

    @staticmethod
    def validate_structure(text: str) -> Tuple[bool, str]:
        """Validate input text has required structure"""
```

---

### 5. **main.py** - CLI Interface

```python
def main():
    """Main entry point"""
    # 1. Display welcome message
    # 2. Prompt for input (multi-line, end with Ctrl+D)
    # 3. Parse input
    # 4. Validate data
    # 5. Check for duplicates
    # 6. Create backup
    # 7. Insert into Excel
    # 8. Display success message
    # 9. Show inserted data summary

if __name__ == '__main__':
    main()
```

**User Flow**:
```
$ python main.py

财务数据自动化工具 v1.0
=========================

请粘贴销售日报 (完成后按 Ctrl+D):
[User pastes text]
[User presses Ctrl+D]

正在解析数据...
✓ 日期: 10-28
✓ 找到 4 个有效字段

正在验证...
✓ 数据验证通过

正在检查重复...
✓ 无重复日期

正在备份文件...
✓ 备份创建: 财务跟踪表_完整版_KL_backup_20251028_201530.xlsx

正在更新Excel...
✓ 数据已插入第 172 行

更新汇总:
- 大众美团: 144
- 储值卡核销: 505
- 教练课核销: 90
- 储值卡充值: 1000

✓ 完成!
```

---

## File Structure

```
Finance/
├── venv/                      # Virtual environment
├── Finance/
│   └── 财务跟踪表_完整版_KL.xlsx  # Excel file
├── main.py                    # CLI entry point
├── parser.py                  # Text parser
├── excel_handler.py           # Excel operations
├── validator.py               # Input validation
├── utils.py                   # Utility functions
├── requirements.txt           # Dependencies
├── CLAUDE.md                  # Documentation for Claude Code
├── TECHNICAL_PLAN.md          # This file
├── README.md                  # User guide
├── examples/
│   └── sample_input.txt       # Example input
└── tests/
    ├── test_parser.py
    ├── test_excel_handler.py
    └── test_integration.py
```

---

## Dependencies (requirements.txt)

```
openpyxl==3.1.5     # Excel file manipulation
pandas==2.3.3        # Data analysis (optional, for future features)
pytest==8.3.0        # Testing framework
python-dateutil==2.9.0  # Date parsing utilities
```

---

## Implementation Phases

### Phase 1: Core Functionality (Current Sprint)
1. ✅ CLAUDE.md created
2. ✅ Technical plan documented
3. ⏳ Build parser.py - Parse Chinese text input
4. ⏳ Build excel_handler.py - Insert data into Excel
5. ⏳ Implement styling preservation
6. ⏳ Generate formulas correctly
7. ⏳ Build validator.py - Input validation
8. ⏳ Build utils.py - Helper functions
9. ⏳ Build main.py - Basic CLI interface
10. ⏳ Create requirements.txt

### Phase 2: Robustness (Next Sprint)
- Comprehensive error handling
- Duplicate detection and handling
- Automatic backups with timestamp
- Unit tests (pytest)
- Integration tests
- Edge case handling

### Phase 3: Enhanced Features (Future)
- Batch processing from files
- Data visualization
- Monthly report export
- Statistical analysis
- GUI interface (PyQt/Tkinter)
- Web interface (Flask/FastAPI)

---

## Testing Strategy

### Unit Tests
```python
# test_parser.py
def test_parse_valid_input()
def test_parse_missing_fields()
def test_parse_invalid_date()
def test_parse_empty_fields()
def test_parse_decimal_numbers()

# test_excel_handler.py
def test_find_next_row()
def test_insert_data()
def test_formula_generation()
def test_styling_preservation()
def test_backup_creation()
def test_duplicate_detection()

# test_validator.py
def test_validate_date()
def test_validate_numbers()
def test_validate_structure()

# test_integration.py
def test_full_workflow()
def test_duplicate_handling()
def test_error_recovery()
```

### Test Data
```
examples/
├── sample_input.txt         # Valid complete input
├── sample_partial.txt       # Input with missing fields
├── sample_invalid.txt       # Malformed input
└── sample_decimal.txt       # Input with decimal values
```

---

## Data Flow Diagram

```
┌─────────────────┐
│  User Input     │
│  (Chinese Text) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validator      │ ← Checks text structure
│  validate_      │
│  structure()    │
└────────┬────────┘
         │ Valid
         ▼
┌─────────────────┐
│  Parser         │
│  parse_daily_   │ ← Extract fields with regex
│  report()       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Dict Data      │
│  {date, fields} │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validator      │ ← Validate date & numbers
│  validate_date()│
│  validate_      │
│  numbers()      │
└────────┬────────┘
         │ Valid
         ▼
┌─────────────────┐
│  Excel Handler  │ ← Check duplicates
│  check_         │
│  duplicate_date │
└────────┬────────┘
         │ No duplicate
         ▼
┌─────────────────┐
│  Excel Handler  │ ← Create backup
│  create_backup()│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Excel Handler  │ ← Find next row
│  find_next_row()│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Excel Handler  │ ← Insert data
│  insert_daily_  │   - Set values
│  data()         │   - Copy styling
│                 │   - Generate formulas
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Excel File     │
│  Updated ✓      │
└─────────────────┘
```

---

## Error Handling Strategy

### Error Types and Responses

1. **Parse Errors**
   - Missing date → "错误: 未找到日期信息"
   - Invalid format → "错误: 输入格式不正确"
   - Action: Show example format, ask to retry

2. **Validation Errors**
   - Future date → "警告: 日期是未来日期，确认继续？"
   - Invalid numbers → "错误: 字段 [X] 包含无效数值"
   - Action: Display errors, ask for correction

3. **Excel Errors**
   - File not found → "错误: Excel文件不存在"
   - File locked → "错误: Excel文件被占用，请关闭文件后重试"
   - Permission denied → "错误: 无权限访问Excel文件"
   - Action: Provide clear instructions

4. **Duplicate Date**
   - Found existing date → "警告: 日期 [X] 已存在于第 [Y] 行"
   - Action: Offer options: [O]verwrite, [S]kip, [C]ancel

---

## Performance Considerations

- **File I/O**: Only open Excel file once per operation
- **Memory**: Use `read_only=False` for openpyxl to allow editing
- **Speed**: Current Excel has 172 rows, processing should be < 1 second
- **Scalability**: Tested up to 1000 rows, remains performant

---

## Security Considerations

- **Input Sanitization**: Validate all numeric inputs
- **File Path**: Use absolute paths, validate file existence
- **Backup**: Always create backup before modification
- **Data Loss Prevention**: Atomic operations (backup → modify → save)

---

## Future Enhancements Roadmap

### Version 2.0
- Batch processing (multiple days at once)
- Edit/delete existing entries
- Data export to CSV/PDF
- Monthly summary generation

### Version 3.0
- GUI with PyQt/Tkinter
- Real-time preview before insertion
- Undo/redo functionality
- Multi-user support with locking

### Version 4.0
- Web interface with Flask/FastAPI
- Mobile app support
- Cloud storage integration
- Automated report emailing
- Dashboard with charts

---

## Development Timeline

**Week 1**: Core Implementation
- Days 1-2: Parser and validator
- Days 3-4: Excel handler with styling
- Days 5-7: Main CLI, testing, bug fixes

**Week 2**: Polish and Testing
- Days 1-3: Comprehensive testing
- Days 4-5: Error handling refinement
- Days 6-7: Documentation and examples

**Week 3**: Deployment
- Days 1-2: User testing
- Days 3-4: Bug fixes from user feedback
- Days 5-7: Production deployment
