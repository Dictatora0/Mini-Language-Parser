#!/usr/bin/env python3
"""
Mini 语言语法分析器 - 综合测试套件
包含所有要求的测试用例：
1. 赋值语句测试
2. if-then 结构测试
3. while 循环结构测试
4. 块测试
5. 不同级别的表达式测试
6. 错误处理测试
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import parse_from_source


class TestResult:
    """测试结果统计"""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.failed_cases = []

    def add_pass(self):
        self.total += 1
        self.passed += 1

    def add_fail(self, case_name, reason):
        self.total += 1
        self.failed += 1
        self.failed_cases.append((case_name, reason))

    def print_summary(self):
        print("\n" + "=" * 80)
        print(f"测试总结: {self.passed}/{self.total} 通过")
        if self.failed > 0:
            print(f"\n失败的测试用例 ({self.failed}):")
            for name, reason in self.failed_cases:
                print(f"  失败用例: {name}")
                print(f"     原因: {reason}")
        print("=" * 80)


def run_test(test_name, code, expected_success=True, expected_keywords=None):
    """
    运行单个测试用例

    Args:
        test_name: 测试用例名称
        code: 源代码
        expected_success: 是否期望成功（True=成功，False=失败）
        expected_keywords: 期望在结果中出现的关键字列表（用于错误检测）

    Returns:
        (passed, reason) 元组
    """
    print(f"\n测试: {test_name}")
    result = parse_from_source(code)

    if expected_success:
        # 期望成功
        if "该程序符合语法要求" in result:
            print("  通过")
            return True, None
        else:
            print(f"  失败 - 期望成功但失败了")
            print(f"  结果: {result[:100]}")
            return False, f"期望成功但得到错误: {result[:100]}"
    else:
        # 期望失败
        if "该程序符合语法要求" in result:
            print(f"  失败 - 期望失败但成功了")
            return False, "期望检测到错误但程序通过了"

        # 检查是否包含期望的关键字
        if expected_keywords:
            for keyword in expected_keywords:
                if keyword in result:
                    print(f"  通过 - 检测到错误: {keyword}")
                    return True, None
            print(f"  失败 - 未检测到期望的错误关键字")
            print(f"  期望关键字: {expected_keywords}")
            print(f"  实际结果: {result[:100]}")
            return False, f"未检测到期望的错误关键字: {expected_keywords}"
        else:
            print(f"  通过 - 检测到错误")
            return True, None


def test_assignment_statements():
    """测试 1: 赋值语句测试"""
    print("\n" + "=" * 80)
    print("【测试 1】赋值语句测试")
    print("验证语法分析器对赋值语句的识别能力")
    print("=" * 80)

    result = TestResult()

    # 正确的赋值语句
    tests = [
        ("简单整数赋值", """
            program test1;
            begin
                x := 5
            end.
        """, True, None),

        ("算术表达式赋值", """
            program test2;
            begin
                x := 5 + 3 * (2 - 1)
            end.
        """, True, None),

        ("复杂表达式赋值", """
            program test3;
            begin
                result := (a + b) * c - d / e
            end.
        """, True, None),

        ("多个赋值语句", """
            program test4;
            begin
                x := 10;
                y := 20;
                z := x + y
            end.
        """, True, None),

        ("负数赋值", """
            program test5;
            begin
                x := -5;
                y := -(a + b)
            end.
        """, True, None),
    ]

    # 错误的赋值语句
    error_tests = [
        ("缺少赋值运算符", """
            program err1;
            begin
                x = 10
            end.
        """, False, [":="]),

        ("赋值运算符后缺少表达式", """
            program err2;
            begin
                x :=
            end.
        """, False, ["表达式", "错误"]),

        ("不完整的算术表达式", """
            program err3;
            begin
                x := 10 +
            end.
        """, False, ["表达式", "错误"]),
    ]

    for test_name, code, expected_success, keywords in tests + error_tests:
        passed, reason = run_test(test_name, code, expected_success, keywords)
        if passed:
            result.add_pass()
        else:
            result.add_fail(test_name, reason)

    return result


def test_if_then_structures():
    """测试 2: if-then 结构测试"""
    print("\n" + "=" * 80)
    print("【测试 2】if-then 结构测试")
    print("测试 if-then 和 if-then-else 控制结构的识别与语法树构建")
    print("=" * 80)

    result = TestResult()

    # 正确的 if-then 结构
    tests = [
        ("简单 if-then", """
            program test1;
            begin
                if x >= 0 then
                    x := x - 1
            end.
        """, True, None),

        ("if-then-else", """
            program test2;
            begin
                if x > 0 then
                    y := 1
                else
                    y := 0
            end.
        """, True, None),

        ("if 条件中的算术表达式", """
            program test3;
            begin
                if x + y > 10 then
                    z := x * y
            end.
        """, True, None),

        ("if 条件中的逻辑运算", """
            program test4;
            begin
                if (x > 0) and (y < 10) then
                    z := 1
            end.
        """, True, None),

        ("嵌套 if-then", """
            program test5;
            begin
                if x > 0 then
                    if y > 0 then
                        z := x + y
            end.
        """, True, None),

        ("if-then 带语句块", """
            program test6;
            begin
                if x > 0 then
                begin
                    y := x;
                    z := x * 2
                end
            end.
        """, True, None),
    ]

    # 错误的 if-then 结构
    error_tests = [
        ("缺少 then 关键字", """
            program err1;
            begin
                if x
                    y := 1
            end.
        """, False, ["then", "关系运算符"]),

        ("if 条件缺少关系运算符", """
            program err2;
            begin
                if x then
                    y := 1
            end.
        """, False, ["关系运算符", "错误"]),
    ]

    for test_name, code, expected_success, keywords in tests + error_tests:
        passed, reason = run_test(test_name, code, expected_success, keywords)
        if passed:
            result.add_pass()
        else:
            result.add_fail(test_name, reason)

    return result


def test_while_structures():
    """测试 3: while 循环结构测试"""
    print("\n" + "=" * 80)
    print("【测试 3】while 循环结构测试")
    print("验证 while 循环结构的语法分析正确性")
    print("=" * 80)

    result = TestResult()

    # 正确的 while 结构
    tests = [
        ("简单 while 循环", """
            program test1;
            begin
                sum := 0;
                i := 1;
                while i <= 5 do
                    i := i + 1
            end.
        """, True, None),

        ("while 带语句块", """
            program test2;
            begin
                sum := 0;
                i := 1;
                while i <= 5 do
                begin
                    sum := sum + i;
                    i := i + 1
                end
            end.
        """, True, None),

        ("while 条件中的逻辑运算", """
            program test3;
            begin
                while (i < 10) and (sum < 100) do
                    i := i + 1
            end.
        """, True, None),

        ("嵌套 while 循环", """
            program test4;
            begin
                i := 0;
                while i < 5 do
                begin
                    j := 0;
                    while j < 5 do
                        j := j + 1;
                    i := i + 1
                end
            end.
        """, True, None),

        ("while 中嵌套 if", """
            program test5;
            begin
                i := 0;
                while i < 10 do
                begin
                    if i > 5 then
                        sum := sum + i;
                    i := i + 1
                end
            end.
        """, True, None),
    ]

    # 错误的 while 结构
    error_tests = [
        ("缺少 do 关键字", """
            program err1;
            begin
                while x > 0
                    x := x - 1
            end.
        """, False, ["do"]),

        ("while 条件缺少关系运算符", """
            program err2;
            begin
                while i do
                    i := i + 1
            end.
        """, False, ["关系运算符", "错误"]),
    ]

    for test_name, code, expected_success, keywords in tests + error_tests:
        passed, reason = run_test(test_name, code, expected_success, keywords)
        if passed:
            result.add_pass()
        else:
            result.add_fail(test_name, reason)

    return result


def test_block_structures():
    """测试 4: 块测试"""
    print("\n" + "=" * 80)
    print("【测试 4】块结构测试")
    print("验证语法分析器是否能正确处理代码块（Block）")
    print("=" * 80)

    result = TestResult()

    # 正确的块结构
    tests = [
        ("简单块", """
            program test1;
            begin
                begin
                    x := 5
                end
            end.
        """, True, None),

        ("块包含多条语句", """
            program test2;
            begin
                begin
                    x := 1;
                    y := 2;
                    z := x + y
                end
            end.
        """, True, None),

        ("嵌套块", """
            program test3;
            begin
                begin
                    x := 1;
                    begin
                        y := 2;
                        begin
                            z := 3
                        end
                    end
                end
            end.
        """, True, None),

        ("空块", """
            program test4;
            begin
                begin
                end
            end.
        """, True, None),

        ("if-then 带块", """
            program test5;
            begin
                if x > 0 then
                begin
                    y := x;
                    z := x * 2
                end
            end.
        """, True, None),

        ("while 带块", """
            program test6;
            begin
                while i < 10 do
                begin
                    sum := sum + i;
                    i := i + 1
                end
            end.
        """, True, None),
    ]

    # 错误的块结构
    error_tests = [
        ("缺少 end 关键字", """
            program err1;
            begin
                begin
                    x := 1
            end.
        """, False, ["end"]),

        ("begin-end 不匹配", """
            program err2;
            begin
                begin
                    begin
                        x := 1
                    end
            end.
        """, False, ["end"]),
    ]

    for test_name, code, expected_success, keywords in tests + error_tests:
        passed, reason = run_test(test_name, code, expected_success, keywords)
        if passed:
            result.add_pass()
        else:
            result.add_fail(test_name, reason)

    return result


def test_expression_levels():
    """测试 5: 不同级别的表达式测试"""
    print("\n" + "=" * 80)
    print("【测试 5】不同级别的表达式测试")
    print("测试运算符优先级与结合性处理的正确性")
    print("=" * 80)

    result = TestResult()

    # 正确的表达式
    tests = [
        ("简单算术表达式", """
            program test1;
            begin
                result := 2 + 3 * 4 - 5 / 2
            end.
        """, True, None),

        ("运算符优先级", """
            program test2;
            begin
                result := a + b * c / d - e
            end.
        """, True, None),

        ("括号改变优先级", """
            program test3;
            begin
                result := (a + b) * (c - d)
            end.
        """, True, None),

        ("嵌套括号", """
            program test4;
            begin
                result := ((a + b) * c) / (d - (e + f))
            end.
        """, True, None),

        ("负数表达式", """
            program test5;
            begin
                x := -5;
                y := -(a + b);
                z := -x * -y
            end.
        """, True, None),

        ("关系表达式", """
            program test6;
            begin
                if a + b > c * d then
                    x := 1
            end.
        """, True, None),

        ("逻辑表达式", """
            program test7;
            begin
                if (x > 0) and (y < 10) or (z = 5) then
                    result := 1
            end.
        """, True, None),

        ("not 运算符", """
            program test8;
            begin
                if not (x < 0) then
                    y := 1
            end.
        """, True, None),

        ("复杂混合表达式", """
            program test9;
            begin
                if ((a + b) * c > d) and (not (e = f)) then
                    result := (x + y) / (z - w)
            end.
        """, True, None),
    ]

    # 错误的表达式
    error_tests = [
        ("表达式不完整 - 加法", """
            program err1;
            begin
                result := 1 +
            end.
        """, False, ["表达式", "错误"]),

        ("表达式不完整 - 乘法", """
            program err2;
            begin
                result := a *
            end.
        """, False, ["表达式", "错误"]),

        ("括号不匹配", """
            program err3;
            begin
                result := (a + b
            end.
        """, False, ["右括号", ")"]),

        ("缺少操作数", """
            program err4;
            begin
                result := + 5
            end.
        """, False, ["表达式", "错误"]),
    ]

    for test_name, code, expected_success, keywords in tests + error_tests:
        passed, reason = run_test(test_name, code, expected_success, keywords)
        if passed:
            result.add_pass()
        else:
            result.add_fail(test_name, reason)

    return result


def test_error_handling():
    """测试 6: 错误处理测试"""
    print("\n" + "=" * 80)
    print("【测试 6】错误处理测试")
    print("验证语法分析器在遇到语法错误时能否正确识别并输出")
    print("=" * 80)

    result = TestResult()

    # 各种错误情况
    error_tests = [
        ("缺少 program 关键字", """
            test;
            begin
                x := 1
            end.
        """, False, ["program"]),

        ("缺少程序名", """
            program;
            begin
                x := 1
            end.
        """, False, ["标识符"]),

        ("缺少分号", """
            program test
            begin
                x := 1
            end.
        """, False, ["分号", ";"]),

        ("缺少 begin", """
            program test;
            x := 1
            end.
        """, False, ["begin"]),

        ("缺少 end", """
            program test;
            begin
                x := 1.
        """, False, ["end"]),

        ("缺少结束点", """
            program test;
            begin
                x := 1
            end
        """, False, ["."]),

        ("赋值运算符错误", """
            program test;
            begin
                x = 10
            end.
        """, False, [":="]),

        ("if 缺少 then", """
            program test;
            begin
                if x > 0
                    y := 1
            end.
        """, False, ["then"]),

        ("while 缺少 do", """
            program test;
            begin
                while x > 0
                    x := x - 1
            end.
        """, False, ["do"]),

        ("条件表达式错误", """
            program test;
            begin
                if x then
                    y := 1
            end.
        """, False, ["关系运算符", "错误"]),

        ("表达式不完整", """
            program test;
            begin
                x := 10 +
            end.
        """, False, ["表达式", "错误"]),

        ("括号不匹配", """
            program test;
            begin
                x := (10 + 20
            end.
        """, False, ["右括号", ")"]),

        ("begin-end 不匹配", """
            program test;
            begin
                begin
                    x := 1
            end.
        """, False, ["end"]),
    ]

    for test_name, code, expected_success, keywords in error_tests:
        passed, reason = run_test(test_name, code, expected_success, keywords)
        if passed:
            result.add_pass()
        else:
            result.add_fail(test_name, reason)

    return result


def run_all_tests():
    """运行所有测试"""
    print("=" * 80)
    print("  Mini 语言语法分析器 - 综合测试套件")
    print("=" * 80)

    # 运行所有测试类别
    test_functions = [
        test_assignment_statements,
        test_if_then_structures,
        test_while_structures,
        test_block_structures,
        test_expression_levels,
        test_error_handling,
    ]

    total_result = TestResult()

    for test_func in test_functions:
        try:
            result = test_func()
            total_result.total += result.total
            total_result.passed += result.passed
            total_result.failed += result.failed
            total_result.failed_cases.extend(result.failed_cases)
        except Exception as e:
            print(f"\n测试函数 {test_func.__name__} 执行异常: {e}")
            import traceback
            traceback.print_exc()

    # 打印总结
    total_result.print_summary()

    return total_result.failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

