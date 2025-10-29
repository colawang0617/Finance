"""
Chinese Daily Report Parser

Parses structured Chinese text input containing daily sales data
and extracts it into a structured dictionary format.
"""

import re
from typing import Dict, Any, Optional


class ParseError(Exception):
    """Raised when parsing fails"""
    pass


# Field name mapping from Chinese to internal keys
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


def parse_daily_report(text: str) -> Dict[str, Any]:
    """
    Parse Chinese daily report text into structured data

    Args:
        text: Multi-line Chinese text with sales data

    Returns:
        Dictionary with parsed data:
        {
            'date': '10-28',
            'meituan': 144,
            'stored_card_redemption': 505,
            'douyin': None,
            ...
        }

    Raises:
        ParseError: If text format is invalid or date cannot be extracted
    """
    if not text or not text.strip():
        raise ParseError("输入文本为空")

    # Initialize result dictionary with all fields as None
    result = {key: None for key in FIELD_MAP.values()}

    # Parse date from header
    date_pattern = r'(\d+)月(\d+)日销售日报'
    date_match = re.search(date_pattern, text)

    if not date_match:
        raise ParseError("未找到日期信息，请确认格式为 'X月Y日销售日报'")

    month = int(date_match.group(1))
    day = int(date_match.group(2))

    # Convert to MM-DD format
    result['date'] = f"{month:02d}-{day:02d}"

    # Parse each field
    lines = text.split('\n')

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Try to match each field in our mapping
        for chinese_name, internal_key in FIELD_MAP.items():
            # Pattern: field name followed by optional colon/whitespace and number
            # Handles: "大众美团 144", "大众美团144", "大众美团", "4. 储值卡充值: 1000"
            pattern = rf'{re.escape(chinese_name)}[\s:：]*(\d+\.?\d*)?'
            match = re.search(pattern, line)

            if match:
                value_str = match.group(1)
                if value_str:
                    # Convert to float if decimal, int otherwise
                    if '.' in value_str:
                        result[internal_key] = float(value_str)
                    else:
                        result[internal_key] = int(value_str)
                else:
                    result[internal_key] = None
                break  # Move to next line after finding a match

    return result


def format_parsed_data(data: Dict[str, Any]) -> str:
    """
    Format parsed data into readable string for display

    Args:
        data: Parsed data dictionary

    Returns:
        Formatted string representation
    """
    lines = [f"日期: {data['date']}"]

    # Reverse mapping for display
    reverse_map = {v: k for k, v in FIELD_MAP.items()}

    non_empty_fields = []
    for key, value in data.items():
        if key == 'date':
            continue
        if value is not None:
            chinese_name = reverse_map.get(key, key)
            non_empty_fields.append(f"  {chinese_name}: {value}")

    if non_empty_fields:
        lines.extend(non_empty_fields)
    else:
        lines.append("  (无数据)")

    return '\n'.join(lines)


if __name__ == '__main__':
    # Test with sample input
    sample_text = """10月28日销售日报
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
当日总计: 1739"""

    try:
        result = parse_daily_report(sample_text)
        print("解析成功!")
        print(format_parsed_data(result))
        print("\n原始数据:")
        print(result)
    except ParseError as e:
        print(f"解析错误: {e}")
