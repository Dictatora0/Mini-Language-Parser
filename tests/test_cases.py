"""
Mini 语言语法分析器完整测试用例集
包含正确程序和各种错误情况的测试
"""

from src import parse_from_source


# 测试用例集合
TEST_CASES = {
    "正确程序": [
        {
            "name": "简单赋值和算术运算",
            "code": """
                program test1;
                begin
                    x := 10;
                    y := 20;
                    z := x + y * 2
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then 语句",
            "code": """
                program test2;
                begin
                    if x > 0 then
                        y := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then-else 语句",
            "code": """
                program test3;
                begin
                    if x < y then
                        z := x + y
                    else
                        z := x - y
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "while-do 循环",
            "code": """
                program test4;
                begin
                    i := 10;
                    while i > 0 do
                        i := i - 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "while-do-begin-end 语句块",
            "code": """
                program test5;
                begin
                    i := 10;
                    while i > 0 do
                    begin
                        sum := sum + i;
                        i := i - 1
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套 if 和 while",
            "code": """
                program nested;
                begin
                    x := 10;
                    while x > 0 do
                    begin
                        if x > 5 then
                            y := x * 2
                        else
                            y := x + 1;
                        x := x - 1
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "复杂算术表达式",
            "code": """
                program expr;
                begin
                    result := (a + b) * (c - d) / e;
                    x := -5;
                    y := -(a + b)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "逻辑表达式 and/or/not",
            "code": """
                program logic;
                begin
                    if (x > 0) and (y < 10) then
                        z := 1;
                    if (a = 5) or (b <> 3) then
                        c := 2;
                    if not (m >= n) then
                        p := 0
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "所有关系运算符",
            "code": """
                program relop;
                begin
                    if a < b then x := 1;
                    if a <= b then x := 2;
                    if a > b then x := 3;
                    if a >= b then x := 4;
                    if a = b then x := 5;
                    if a <> b then x := 6
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "复杂嵌套逻辑",
            "code": """
                program complex_logic;
                begin
                    if ((x > 0) and (y > 0)) or ((x < 0) and (y < 0)) then
                    begin
                        if not (z = 0) then
                            result := x * y / z
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
    ],
    
    "表达式错误": [
        {
            "name": "算术表达式不完整",
            "code": """
                program err1;
                begin
                    i := 1 + 
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "缺少运算数",
            "code": """
                program err2;
                begin
                    x := * 5
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "括号不匹配",
            "code": """
                program err3;
                begin
                    y := (a + b * c
                end.
            """,
            "expected_keyword": "右括号"
        },
        {
            "name": "多余的右括号",
            "code": """
                program err4;
                begin
                    z := a + b)
                end.
            """,
            "expected_keyword": "语法错误"
        },
    ],
    
    "语句错误": [
        {
            "name": "缺少赋值运算符",
            "code": """
                program err5;
                begin
                    x = 10
                end.
            """,
            "expected_keyword": ":="
        },
        {
            "name": "缺少分号",
            "code": """
                program err6;
                begin
                    x := 10
                    y := 20
                end.
            """,
            "expected_keyword": "语法错误"
        },
        {
            "name": "if 缺少 then",
            "code": """
                program err7;
                begin
                    if x > 0
                        y := 1
                end.
            """,
            "expected_keyword": "then"
        },
        {
            "name": "while 缺少 do",
            "code": """
                program err8;
                begin
                    while x > 0
                        x := x - 1
                end.
            """,
            "expected_keyword": "do"
        },
        {
            "name": "条件表达式错误",
            "code": """
                program err9;
                begin
                    if x then
                        y := 1
                end.
            """,
            "expected_keyword": "关系运算符"
        },
    ],
    
    "结构错误": [
        {
            "name": "缺少 program 关键字",
            "code": """
                test;
                begin
                    x := 1
                end.
            """,
            "expected_keyword": "program"
        },
        {
            "name": "缺少程序名",
            "code": """
                program;
                begin
                    x := 1
                end.
            """,
            "expected_keyword": "标识符"
        },
        {
            "name": "缺少 begin",
            "code": """
                program test;
                x := 1
                end.
            """,
            "expected_keyword": "begin"
        },
        {
            "name": "缺少 end",
            "code": """
                program test;
                begin
                    x := 1.
            """,
            "expected_keyword": "end"
        },
        {
            "name": "缺少结束点",
            "code": """
                program test;
                begin
                    x := 1
                end
            """,
            "expected_keyword": "."
        },
        {
            "name": "begin-end 不匹配",
            "code": """
                program test;
                begin
                    begin
                        x := 1
                    end
            """,
            "expected_keyword": "end"
        },
    ],
    
    "边界情况": [
        {
            "name": "空程序",
            "code": """
                program empty;
                begin
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "只有一条语句",
            "code": """
                program single;
                begin
                    x := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "末尾多余分号",
            "code": """
                program extra_semi;
                begin
                    x := 1;
                    y := 2;
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "深层嵌套",
            "code": """
                program deep;
                begin
                    if a > 0 then
                        if b > 0 then
                            if c > 0 then
                                if d > 0 then
                                    x := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
    ],
}


def run_test(category: str, test_case: dict):
    """运行单个测试用例"""
    print(f"\n【{test_case['name']}】")
    print("源代码:")
    print(test_case['code'])
    
    result = parse_from_source(test_case['code'])
    print("分析结果:")
    print(result)
    
    # 检查结果
    if 'expected' in test_case:
        if result == test_case['expected']:
            print("测试通过")
            return True
        else:
            print(f"测试失败，期望: {test_case['expected']}")
            return False
    elif 'expected_keyword' in test_case:
        if test_case['expected_keyword'] in result:
            print("测试通过（包含预期错误信息）")
            return True
        else:
            print(f"测试失败，期望包含关键字: {test_case['expected_keyword']}")
            return False
    
    return True


def run_all_tests():
    """运行所有测试用例"""
    print("=" * 80)
    print("Mini 语言语法分析器 - 完整测试套件")
    print("=" * 80)
    
    total_tests = 0
    passed_tests = 0
    
    for category, tests in TEST_CASES.items():
        print(f"\n{'=' * 80}")
        print(f"测试类别: {category}")
        print(f"{'=' * 80}")
        
        for test_case in tests:
            total_tests += 1
            if run_test(category, test_case):
                passed_tests += 1
    
    # 总结
    print("\n" + "=" * 80)
    print(f"测试总结: {passed_tests}/{total_tests} 通过")
    print("=" * 80)
    
    if passed_tests == total_tests:
        print("所有测试通过！")
    else:
        print(f"{total_tests - passed_tests} 个测试失败")


if __name__ == "__main__":
    run_all_tests()
