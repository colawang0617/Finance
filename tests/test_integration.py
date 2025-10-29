#!/usr/bin/env python3
"""
Integration test script

Tests the complete workflow without user interaction.
"""

from parser import parse_daily_report
from excel_handler import ExcelHandler
from validator import InputValidator


def test_integration():
    """Test complete workflow"""
    print("=" * 60)
    print("           集成测试 - 财务数据自动化工具")
    print("=" * 60)

    # Test data
    test_input = """10月29日销售日报
1. 场地入账金额: 800
大众美团 200
储值卡核销 600
抖音
教练课核销
微信
支付宝
2.云店销售:
水 10
佳得乐 20
3.体验课: 100
4. 储值卡充值: 2000
5. 私教课充值: 500
6. 月卡: 300
当日总计: 3730"""

    print("\n步骤 1: 验证输入格式")
    is_valid, error = InputValidator.validate_structure(test_input)
    if is_valid:
        print("  ✓ 输入格式正确")
    else:
        print(f"  ✗ 输入格式错误: {error}")
        return

    print("\n步骤 2: 解析数据")
    try:
        data = parse_daily_report(test_input)
        print(f"  ✓ 解析成功，日期: {data['date']}")
        non_empty = sum(1 for k, v in data.items() if k != 'date' and v is not None)
        print(f"  ✓ 找到 {non_empty} 个有效字段")
    except Exception as e:
        print(f"  ✗ 解析失败: {e}")
        return

    print("\n步骤 3: 验证数据")
    is_valid, errors = InputValidator.validate_data(data)
    if is_valid:
        print("  ✓ 数据验证通过")
    else:
        print("  ✗ 数据验证失败:")
        for err in errors:
            print(f"    - {err}")
        return

    print("\n步骤 4: 检查Excel文件")
    try:
        handler = ExcelHandler('Finance/财务跟踪表_完整版_KL.xlsx')
        next_row = handler.find_next_row()
        print(f"  ✓ Excel文件打开成功")
        print(f"  ✓ 下一个空行: {next_row}")

        dup_row = handler.check_duplicate_date(data['date'])
        if dup_row:
            print(f"  ⚠ 日期 {data['date']} 已存在于第 {dup_row} 行")
        else:
            print(f"  ✓ 日期 {data['date']} 无重复")

        handler.close()

    except Exception as e:
        print(f"  ✗ Excel操作失败: {e}")
        return

    print("\n步骤 5: 数据预览")
    print("  " + "-" * 56)
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

    for key, value in data.items():
        if key == 'date':
            continue
        if value is not None:
            chinese_name = field_names.get(key, key)
            print(f"  {chinese_name}: {value}")

    print("  " + "-" * 56)

    print("\n" + "=" * 60)
    print("  ✓ 所有测试通过! 程序可以正常工作")
    print("  注意: 此测试未实际修改Excel文件")
    print("=" * 60)


if __name__ == '__main__':
    test_integration()
