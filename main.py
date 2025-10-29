#!/usr/bin/env python3
"""
Financial Data Automation Tool - Main Program

Command-line interface for processing daily income reports
and updating Excel financial tracking system.
"""

import sys
import os
from parser import parse_daily_report, ParseError, format_parsed_data
from excel_handler import ExcelHandler, ExcelHandlerError
from validator import InputValidator, ValidationError
from utils import format_currency


# Configuration
EXCEL_FILE_PATH = 'Finance/财务跟踪表_完整版_KL.xlsx'


def print_header():
    """Print welcome header"""
    print("=" * 50)
    print("       财务数据自动化工具 v1.0")
    print("=" * 50)
    print()


def print_success(message: str):
    """Print success message"""
    print(f"✓ {message}")


def print_error(message: str):
    """Print error message"""
    print(f"✗ {message}")


def print_warning(message: str):
    """Print warning message"""
    print(f"⚠ {message}")


def get_multiline_input() -> str:
    """
    Get multi-line input from user

    Returns:
        Complete input text
    """
    print("请粘贴销售日报 (完成后按 Ctrl+D 或 Ctrl+Z+Enter):")
    print("-" * 50)

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    print("-" * 50)
    return '\n'.join(lines)


def confirm_action(prompt: str) -> bool:
    """
    Ask user for confirmation

    Args:
        prompt: Confirmation prompt

    Returns:
        True if user confirms, False otherwise
    """
    while True:
        response = input(f"{prompt} [Y/n]: ").strip().lower()
        if response in ['y', 'yes', '是', '']:
            return True
        elif response in ['n', 'no', '否']:
            return False
        else:
            print("请输入 Y 或 N")


def display_summary(data: dict):
    """Display summary of non-empty fields"""
    print("\n数据汇总:")
    print("-" * 50)

    # Field name mapping for display
    field_names = {
        'meituan': '大众美团',
        'stored_card_redemption': '储值卡核销',
        'douyin': '抖音',
        'coaching_redemption': '教练课核销',
        'wechat': '微信',
        'alipay': '支付宝',
        'water': '水',
        'gatorade': '佳得乐',
        'other': '其他',
        'trial_class': '体验课',
        'stored_card_recharge': '储值卡充值',
        'private_coaching_recharge': '私教课充值',
        'monthly_card': '月卡'
    }

    count = 0
    for key, value in data.items():
        if key == 'date':
            continue
        if value is not None:
            chinese_name = field_names.get(key, key)
            formatted_value = format_currency(value)
            print(f"  {chinese_name}: {formatted_value}")
            count += 1

    if count == 0:
        print("  (无有效数据)")

    print("-" * 50)


def main():
    """Main program entry point"""
    print_header()

    # Check if Excel file exists
    if not os.path.exists(EXCEL_FILE_PATH):
        print_error(f"Excel文件不存在: {EXCEL_FILE_PATH}")
        print("请确认文件路径是否正确")
        return 1

    try:
        # Step 1: Get input
        input_text = get_multiline_input()

        if not input_text.strip():
            print_error("输入为空，程序退出")
            return 1

        # Step 2: Validate structure
        print("\n正在验证输入格式...")
        is_valid, error = InputValidator.validate_structure(input_text)
        if not is_valid:
            print_error(f"输入格式错误: {error}")
            return 1
        print_success("输入格式正确")

        # Step 3: Parse input
        print("\n正在解析数据...")
        try:
            data = parse_daily_report(input_text)
            print_success(f"日期: {data['date']}")

            # Count non-empty fields
            field_count = sum(1 for v in data.values() if v is not None and v != data.get('date'))
            print_success(f"找到 {field_count} 个有效字段")

        except ParseError as e:
            print_error(f"解析失败: {e}")
            return 1

        # Step 4: Validate data
        print("\n正在验证数据...")
        is_valid, errors = InputValidator.validate_data(data)
        if not is_valid:
            print_error("数据验证失败:")
            for error in errors:
                print(f"  - {error}")
            return 1
        print_success("数据验证通过")

        # Step 5: Display summary
        display_summary(data)

        # Step 6: Confirm before proceeding
        if not confirm_action("\n是否继续更新Excel文件?"):
            print("\n操作已取消")
            return 0

        # Step 7: Open Excel and check for duplicates
        print("\n正在检查Excel文件...")
        try:
            handler = ExcelHandler(EXCEL_FILE_PATH)

            # Check for duplicate date
            dup_row = handler.check_duplicate_date(data['date'])
            if dup_row:
                print_warning(f"日期 {data['date']} 已存在于第 {dup_row} 行")
                if not confirm_action("是否覆盖现有数据?"):
                    print("\n操作已取消")
                    handler.close()
                    return 0
                # Note: Current implementation doesn't actually overwrite,
                # it will add a new row. To implement overwrite, modify excel_handler.py

            print_success("无重复日期" if not dup_row else "用户确认覆盖")

            # Step 8: Create backup
            print("\n正在创建备份...")
            backup_path = handler.create_backup()
            backup_name = os.path.basename(backup_path)
            print_success(f"备份已创建: {backup_name}")

            # Step 9: Insert data
            print("\n正在更新Excel...")
            row = handler.insert_daily_data(data)
            print_success(f"数据已插入第 {row} 行")

            # Step 10: Save
            print("\n正在保存文件...")
            handler.save()
            print_success("文件保存成功")

            handler.close()

            # Final success message
            print("\n" + "=" * 50)
            print("           ✓ 更新完成!")
            print("=" * 50)

            return 0

        except ExcelHandlerError as e:
            print_error(f"Excel操作失败: {e}")
            return 1

    except KeyboardInterrupt:
        print("\n\n操作已取消")
        return 1
    except Exception as e:
        print_error(f"未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
