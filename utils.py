"""
Utility Functions

Helper functions for date conversion, number formatting, and validation.
"""

from datetime import datetime
from typing import Optional, Tuple


def convert_chinese_date_to_excel_format(month: int, day: int) -> str:
    """
    Convert Chinese date format to Excel MM-DD format

    Args:
        month: Month number (1-12)
        day: Day number (1-31)

    Returns:
        Date string in MM-DD format (e.g., "10-28")
    """
    return f"{month:02d}-{day:02d}"


def validate_date(month: int, day: int) -> Tuple[bool, str]:
    """
    Validate that date is reasonable and not in the future

    Args:
        month: Month number (1-12)
        day: Day number (1-31)

    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is empty string
    """
    # Check valid ranges
    if not (1 <= month <= 12):
        return False, f"月份无效: {month} (应在 1-12 之间)"

    if not (1 <= day <= 31):
        return False, f"日期无效: {day} (应在 1-31 之间)"

    # Check month/day combination
    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if day > days_in_month[month - 1]:
        return False, f"{month}月不能有{day}日"

    # Check if date is in the future
    now = datetime.now()
    current_year = now.year

    try:
        input_date = datetime(current_year, month, day)

        # If date is more than 1 day in the future, warn
        if input_date > now and (input_date - now).days > 1:
            return False, f"日期 {month}月{day}日 在未来，请确认"

    except ValueError:
        return False, f"日期无效: {month}月{day}日"

    return True, ""


def format_number(value: Optional[float]) -> Optional[float]:
    """
    Format number for Excel insertion

    Args:
        value: Number value or None

    Returns:
        Formatted number or None
    """
    if value is None:
        return None

    # Round to 2 decimal places if needed
    if isinstance(value, float):
        return round(value, 2)

    return value


def format_currency(value: Optional[float]) -> str:
    """
    Format number as currency string for display

    Args:
        value: Number value or None

    Returns:
        Formatted currency string
    """
    if value is None:
        return "0"

    return f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"


if __name__ == '__main__':
    # Test date validation
    print("=== Date Validation Tests ===")

    test_cases = [
        (10, 28),
        (2, 30),   # Invalid
        (13, 1),   # Invalid month
        (12, 32),  # Invalid day
    ]

    for month, day in test_cases:
        is_valid, error = validate_date(month, day)
        date_str = convert_chinese_date_to_excel_format(month, day)
        print(f"{month}月{day}日 -> {date_str}: {'✓' if is_valid else '✗ ' + error}")

    print("\n=== Number Formatting Tests ===")
    test_numbers = [None, 144, 505.5, 1000.123]
    for num in test_numbers:
        formatted = format_number(num)
        currency = format_currency(num)
        print(f"{num} -> {formatted} (display: {currency})")
