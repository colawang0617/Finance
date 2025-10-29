"""
Input Validator Module

Validates parsed data before Excel insertion to ensure data quality.
"""

import re
from typing import Dict, Any, Tuple, List


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


class InputValidator:
    """Validate parsed data before Excel insertion"""

    @staticmethod
    def validate_structure(text: str) -> Tuple[bool, str]:
        """
        Validate that input text has required structure

        Args:
            text: Raw input text

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text or not text.strip():
            return False, "输入文本为空"

        # Check for date header
        if not re.search(r'\d+月\d+日销售日报', text):
            return False, "未找到日期标题 (格式: X月Y日销售日报)"

        # Check for at least some content
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if len(lines) < 2:
            return False, "输入内容太少，请确认格式正确"

        return True, ""

    @staticmethod
    def validate_date(date: str) -> Tuple[bool, str]:
        """
        Validate date format

        Args:
            date: Date in MM-DD format

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not date:
            return False, "日期为空"

        # Check format
        if not re.match(r'^\d{2}-\d{2}$', date):
            return False, f"日期格式错误: {date} (应为 MM-DD 格式)"

        # Parse month and day
        try:
            month, day = map(int, date.split('-'))

            if not (1 <= month <= 12):
                return False, f"月份无效: {month}"

            if not (1 <= day <= 31):
                return False, f"日期无效: {day}"

        except ValueError:
            return False, f"日期解析失败: {date}"

        return True, ""

    @staticmethod
    def validate_numbers(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate all numeric fields in parsed data

        Args:
            data: Parsed data dictionary

        Returns:
            Tuple of (is_valid, list_of_error_messages)
        """
        errors = []

        # Fields that should be numbers (if not None)
        numeric_fields = [
            'meituan', 'stored_card_redemption', 'douyin', 'coaching_redemption',
            'wechat', 'alipay', 'water', 'gatorade', 'other', 'trial_class',
            'stored_card_recharge', 'private_coaching_recharge', 'monthly_card'
        ]

        for field in numeric_fields:
            value = data.get(field)

            if value is not None:
                # Check if it's a valid number
                if not isinstance(value, (int, float)):
                    errors.append(f"字段 {field} 的值不是数字: {value}")

                # Check if it's negative
                elif value < 0:
                    errors.append(f"字段 {field} 的值不能为负数: {value}")

                # Check if it's unreasonably large (> 1 million)
                elif value > 1000000:
                    errors.append(f"字段 {field} 的值过大: {value} (请确认)")

        return len(errors) == 0, errors

    @staticmethod
    def validate_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Comprehensive validation of parsed data

        Args:
            data: Parsed data dictionary

        Returns:
            Tuple of (is_valid, list_of_error_messages)
        """
        all_errors = []

        # Validate date
        date_valid, date_error = InputValidator.validate_date(data.get('date', ''))
        if not date_valid:
            all_errors.append(date_error)

        # Validate numbers
        numbers_valid, number_errors = InputValidator.validate_numbers(data)
        if not numbers_valid:
            all_errors.extend(number_errors)

        # Check if there's at least some data
        has_data = any(
            data.get(field) is not None
            for field in data.keys()
            if field != 'date'
        )

        if not has_data:
            all_errors.append("所有数据字段都为空，请确认输入")

        return len(all_errors) == 0, all_errors


if __name__ == '__main__':
    # Test validation
    print("=== Structure Validation Tests ===")

    test_texts = [
        ("", "空文本"),
        ("10月28日销售日报\n大众美团 144", "有效文本"),
        ("随机文本\n没有日期", "无日期文本"),
    ]

    for text, desc in test_texts:
        is_valid, error = InputValidator.validate_structure(text)
        print(f"{desc}: {'✓' if is_valid else '✗ ' + error}")

    print("\n=== Date Validation Tests ===")

    test_dates = [
        "10-28",
        "13-01",
        "02-30",
        "invalid",
    ]

    for date in test_dates:
        is_valid, error = InputValidator.validate_date(date)
        print(f"{date}: {'✓' if is_valid else '✗ ' + error}")

    print("\n=== Data Validation Tests ===")

    test_data_sets = [
        {
            'date': '10-28',
            'meituan': 144,
            'stored_card_redemption': 505,
            'stored_card_recharge': 1000,
        },
        {
            'date': '10-28',
            'meituan': -100,  # Invalid: negative
        },
        {
            'date': 'invalid',
            'meituan': 144,
        },
        {
            'date': '10-28',
            # No data fields
        },
    ]

    for i, data in enumerate(test_data_sets, 1):
        is_valid, errors = InputValidator.validate_data(data)
        print(f"\n测试集 {i}: {'✓' if is_valid else '✗'}")
        if not is_valid:
            for error in errors:
                print(f"  - {error}")
