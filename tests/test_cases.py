"""
Mini 语言语法分析器完整测试用例集
包含正确程序和各种错误情况的测试
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import parse_from_source


# 测试用例集合
TEST_CASES = {
    "赋值语句测试": [
        {
            "name": "简单整数字面量赋值",
            "code": """
                program test_assign1;
                begin
                    x := 42
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "多个简单赋值",
            "code": """
                program test_assign2;
                begin
                    a := 10;
                    b := 20;
                    c := 30
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "复杂算术表达式赋值",
            "code": """
                program test_assign3;
                begin
                    result := a + b * c - d / e
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "带括号的复杂表达式赋值",
            "code": """
                program test_assign4;
                begin
                    result := (a + b) * (c - d)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套括号表达式赋值",
            "code": """
                program test_assign5;
                begin
                    x := ((a + b) * c) / (d - (e + f))
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "负数表达式赋值",
            "code": """
                program test_assign6;
                begin
                    x := -5;
                    y := -(a + b);
                    z := -x * -y
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "混合运算符优先级赋值",
            "code": """
                program test_assign7;
                begin
                    result := a + b * c / d - e
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "缺少赋值运算符",
            "code": """
                program test_assign_err1;
                begin
                    x = 10
                end.
            """,
            "expected_keyword": ":="
        },
        {
            "name": "赋值运算符后缺少表达式",
            "code": """
                program test_assign_err2;
                begin
                    x :=
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "不完整的算术表达式",
            "code": """
                program test_assign_err3;
                begin
                    x := 10 +
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "不完整的乘法表达式",
            "code": """
                program test_assign_err4;
                begin
                    y := a *
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "表达式缺少操作数",
            "code": """
                program test_assign_err5;
                begin
                    z := + 5
                end.
            """,
            "expected_keyword": "表达式错误"
        },
    ],
    "控制流语句测试": [
        # if-then statements with various conditions
        {
            "name": "if-then 简单关系条件",
            "code": """
                program test_if1;
                begin
                    if x > 0 then
                        y := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then 等于条件",
            "code": """
                program test_if2;
                begin
                    if a = 5 then
                        b := 10
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then 不等于条件",
            "code": """
                program test_if3;
                begin
                    if x <> y then
                        z := 0
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then 复杂逻辑条件 (and)",
            "code": """
                program test_if4;
                begin
                    if (x > 0) and (y < 10) then
                        z := x + y
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then 复杂逻辑条件 (or)",
            "code": """
                program test_if5;
                begin
                    if (a = 0) or (b = 0) then
                        result := 0
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then 带 not 的条件",
            "code": """
                program test_if6;
                begin
                    if not (x < 0) then
                        y := x * 2
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # if-then-else statements
        {
            "name": "if-then-else 简单条件",
            "code": """
                program test_ifelse1;
                begin
                    if x < y then
                        z := x
                    else
                        z := y
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then-else 复杂表达式",
            "code": """
                program test_ifelse2;
                begin
                    if a >= b then
                        max := a * 2 + 1
                    else
                        max := b * 2 + 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then-else 带语句块",
            "code": """
                program test_ifelse3;
                begin
                    if x > 0 then
                    begin
                        y := x;
                        z := x * 2
                    end
                    else
                    begin
                        y := -x;
                        z := -x * 2
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Nested if statements
        {
            "name": "嵌套 if-then 两层",
            "code": """
                program test_nested_if1;
                begin
                    if x > 0 then
                        if y > 0 then
                            z := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套 if-then-else 两层",
            "code": """
                program test_nested_if2;
                begin
                    if x > 0 then
                        if y > 0 then
                            z := 1
                        else
                            z := 2
                    else
                        z := 3
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套 if 三层",
            "code": """
                program test_nested_if3;
                begin
                    if a > 0 then
                        if b > 0 then
                            if c > 0 then
                                result := a + b + c
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套 if-else 复杂结构",
            "code": """
                program test_nested_if4;
                begin
                    if x > 10 then
                    begin
                        if x > 20 then
                            y := 3
                        else
                            y := 2
                    end
                    else
                    begin
                        if x > 5 then
                            y := 1
                        else
                            y := 0
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # while-do loops with simple bodies
        {
            "name": "while-do 简单循环",
            "code": """
                program test_while1;
                begin
                    while i > 0 do
                        i := i - 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "while-do 复杂条件",
            "code": """
                program test_while2;
                begin
                    while (x > 0) and (y < 100) do
                        x := x - 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "while-do 带 not 条件",
            "code": """
                program test_while3;
                begin
                    while not (done = 1) do
                        count := count + 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # while-do loops with block bodies
        {
            "name": "while-do 带语句块",
            "code": """
                program test_while_block1;
                begin
                    while i < 10 do
                    begin
                        sum := sum + i;
                        i := i + 1
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "while-do 多语句块",
            "code": """
                program test_while_block2;
                begin
                    while x > 0 do
                    begin
                        y := y + x;
                        z := z * 2;
                        x := x - 1
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Nested while loops
        {
            "name": "嵌套 while 两层",
            "code": """
                program test_nested_while1;
                begin
                    while i < 10 do
                        while j < 10 do
                            j := j + 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套 while 带语句块",
            "code": """
                program test_nested_while2;
                begin
                    while i < 10 do
                    begin
                        j := 0;
                        while j < 10 do
                        begin
                            sum := sum + i * j;
                            j := j + 1
                        end;
                        i := i + 1
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套 while 三层",
            "code": """
                program test_nested_while3;
                begin
                    while i < 5 do
                        while j < 5 do
                            while k < 5 do
                                k := k + 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Mixed nested control flow
        {
            "name": "while 中嵌套 if",
            "code": """
                program test_while_if;
                begin
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
            "name": "if 中嵌套 while",
            "code": """
                program test_if_while;
                begin
                    if n > 0 then
                    begin
                        i := 0;
                        while i < n do
                            i := i + 1
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Error cases - missing then keyword
        {
            "name": "if 缺少 then 关键字",
            "code": """
                program test_if_err1;
                begin
                    if x > 0
                        y := 1
                end.
            """,
            "expected_keyword": "then"
        },
        {
            "name": "if 复杂条件缺少 then",
            "code": """
                program test_if_err2;
                begin
                    if (x > 0) and (y < 10)
                        z := 1
                end.
            """,
            "expected_keyword": "then"
        },
        # Error cases - missing do keyword
        {
            "name": "while 缺少 do 关键字",
            "code": """
                program test_while_err1;
                begin
                    while x > 0
                        x := x - 1
                end.
            """,
            "expected_keyword": "do"
        },
        {
            "name": "while 复杂条件缺少 do",
            "code": """
                program test_while_err2;
                begin
                    while (i < 10) and (j > 0)
                        i := i + 1
                end.
            """,
            "expected_keyword": "do"
        },
        # Error cases - invalid condition errors
        {
            "name": "if 条件缺少关系运算符",
            "code": """
                program test_cond_err1;
                begin
                    if x then
                        y := 1
                end.
            """,
            "expected_keyword": "关系运算符"
        },
        {
            "name": "while 条件缺少关系运算符",
            "code": """
                program test_cond_err2;
                begin
                    while x do
                        x := x - 1
                end.
            """,
            "expected_keyword": "关系运算符"
        },
        {
            "name": "if 条件表达式不完整",
            "code": """
                program test_cond_err3;
                begin
                    if x > then
                        y := 1
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "while 条件表达式不完整",
            "code": """
                program test_cond_err4;
                begin
                    while i < do
                        i := i + 1
                end.
            """,
            "expected_keyword": "表达式错误"
        },
    ],
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

    "块结构测试": [
        # Blocks with multiple statements
        {
            "name": "块包含两条语句",
            "code": """
                program test_block1;
                begin
                    begin
                        x := 1;
                        y := 2
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "块包含三条语句",
            "code": """
                program test_block2;
                begin
                    begin
                        a := 10;
                        b := 20;
                        c := a + b
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "块包含多条复杂语句",
            "code": """
                program test_block3;
                begin
                    begin
                        x := (a + b) * c;
                        y := x / 2;
                        z := y - 10;
                        result := z * z
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "块包含控制流语句",
            "code": """
                program test_block4;
                begin
                    begin
                        if x > 0 then
                            y := 1;
                        while i < 10 do
                            i := i + 1;
                        z := x + y
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Empty blocks
        {
            "name": "空块",
            "code": """
                program test_empty_block1;
                begin
                    begin
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then 带空块",
            "code": """
                program test_empty_block2;
                begin
                    if x > 0 then
                    begin
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "while-do 带空块",
            "code": """
                program test_empty_block3;
                begin
                    while i < 10 do
                    begin
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "if-then-else 两个空块",
            "code": """
                program test_empty_block4;
                begin
                    if x > 0 then
                    begin
                    end
                    else
                    begin
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Nested blocks at various depths
        {
            "name": "嵌套块两层",
            "code": """
                program test_nested_block1;
                begin
                    begin
                        x := 1;
                        begin
                            y := 2
                        end
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套块三层",
            "code": """
                program test_nested_block2;
                begin
                    begin
                        a := 1;
                        begin
                            b := 2;
                            begin
                                c := 3
                            end
                        end
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套块四层",
            "code": """
                program test_nested_block3;
                begin
                    begin
                        begin
                            begin
                                x := 1
                            end
                        end
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套块五层带语句",
            "code": """
                program test_nested_block4;
                begin
                    begin
                        x := 1;
                        begin
                            y := 2;
                            begin
                                z := 3;
                                begin
                                    a := 4;
                                    begin
                                        b := 5
                                    end
                                end
                            end
                        end
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套块混合控制流",
            "code": """
                program test_nested_block5;
                begin
                    begin
                        if x > 0 then
                        begin
                            while y < 10 do
                            begin
                                y := y + 1
                            end
                        end
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "多个顺序嵌套块",
            "code": """
                program test_nested_block6;
                begin
                    begin
                        x := 1
                    end;
                    begin
                        y := 2
                    end;
                    begin
                        z := 3
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "深度嵌套块十层",
            "code": """
                program test_deep_nested;
                begin
                    begin
                        begin
                            begin
                                begin
                                    begin
                                        begin
                                            begin
                                                begin
                                                    begin
                                                        x := 1
                                                    end
                                                end
                                            end
                                        end
                                    end
                                end
                            end
                        end
                    end
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Missing begin keyword error
        {
            "name": "缺少 begin 关键字 - 块开始",
            "code": """
                program test_missing_begin1;
                begin
                    x := 1;
                    y := 2
                    end
                end.
            """,
            "expected_keyword": "语法错误"
        },
        {
            "name": "缺少 begin 关键字 - if 语句块",
            "code": """
                program test_missing_begin2;
                begin
                    if x > 0 then
                        x := 1;
                        y := 2
                    end
                end.
            """,
            "expected_keyword": "语法错误"
        },
        {
            "name": "缺少 begin 关键字 - while 语句块",
            "code": """
                program test_missing_begin3;
                begin
                    while i < 10 do
                        i := i + 1;
                        sum := sum + i
                    end
                end.
            """,
            "expected_keyword": "语法错误"
        },
        # Missing end keyword error
        {
            "name": "缺少 end 关键字 - 简单块",
            "code": """
                program test_missing_end1;
                begin
                    begin
                        x := 1
                end.
            """,
            "expected_keyword": "end"
        },
        {
            "name": "缺少 end 关键字 - 嵌套块",
            "code": """
                program test_missing_end2;
                begin
                    begin
                        begin
                            x := 1
                        end
                end.
            """,
            "expected_keyword": "end"
        },
        {
            "name": "缺少 end 关键字 - if 语句块",
            "code": """
                program test_missing_end3;
                begin
                    if x > 0 then
                    begin
                        x := 1;
                        y := 2
                end.
            """,
            "expected_keyword": "end"
        },
        {
            "name": "缺少 end 关键字 - while 语句块",
            "code": """
                program test_missing_end4;
                begin
                    while i < 10 do
                    begin
                        i := i + 1;
                        sum := sum + i
                end.
            """,
            "expected_keyword": "end"
        },
        # Begin-end mismatch errors
        {
            "name": "begin-end 不匹配 - 多余的 begin",
            "code": """
                program test_mismatch1;
                begin
                    begin
                        begin
                            x := 1
                        end
                end.
            """,
            "expected_keyword": "end"
        },
        {
            "name": "begin-end 不匹配 - 多余的 end",
            "code": """
                program test_mismatch2;
                begin
                    begin
                        x := 1
                    end
                    end
                end.
            """,
            "expected_keyword": "语法错误"
        },
        {
            "name": "begin-end 不匹配 - 嵌套错误",
            "code": """
                program test_mismatch3;
                begin
                    begin
                        x := 1;
                        begin
                            y := 2
                    end
                end.
            """,
            "expected_keyword": "end"
        },
        {
            "name": "begin-end 不匹配 - 交叉嵌套",
            "code": """
                program test_mismatch4;
                begin
                    begin
                        if x > 0 then
                        begin
                            y := 1
                    end
                end.
            """,
            "expected_keyword": "end"
        },
    ],

    "表达式解析测试": [
        # Arithmetic expressions with all operators (+, -, *, /)
        {
            "name": "加法表达式",
            "code": """
                program test_add;
                begin
                    result := a + b
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "减法表达式",
            "code": """
                program test_sub;
                begin
                    result := x - y
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "乘法表达式",
            "code": """
                program test_mul;
                begin
                    result := a * b
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "除法表达式",
            "code": """
                program test_div;
                begin
                    result := x / y
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "混合四则运算",
            "code": """
                program test_mixed;
                begin
                    result := a + b - c * d / e
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "连续加法",
            "code": """
                program test_chain_add;
                begin
                    sum := a + b + c + d + e
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "连续乘法",
            "code": """
                program test_chain_mul;
                begin
                    product := a * b * c * d
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "负数表达式",
            "code": """
                program test_negative;
                begin
                    x := -10;
                    y := -a;
                    z := -(-5)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "负数运算",
            "code": """
                program test_neg_ops;
                begin
                    result := -a + -b * -c
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Expressions testing operator precedence
        {
            "name": "乘法优先于加法",
            "code": """
                program test_prec1;
                begin
                    result := a + b * c
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "除法优先于减法",
            "code": """
                program test_prec2;
                begin
                    result := a - b / c
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "乘除优先于加减",
            "code": """
                program test_prec3;
                begin
                    result := a + b * c - d / e
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "左结合性测试 - 加法",
            "code": """
                program test_assoc1;
                begin
                    result := a - b - c
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "左结合性测试 - 乘法",
            "code": """
                program test_assoc2;
                begin
                    result := a / b / c
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "复杂优先级测试",
            "code": """
                program test_prec_complex;
                begin
                    result := a + b * c / d - e * f + g
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Expressions with parentheses
        {
            "name": "简单括号表达式",
            "code": """
                program test_paren1;
                begin
                    result := (a + b)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "括号改变优先级",
            "code": """
                program test_paren2;
                begin
                    result := (a + b) * c
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "多个括号表达式",
            "code": """
                program test_paren3;
                begin
                    result := (a + b) * (c - d)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套括号两层",
            "code": """
                program test_nested_paren1;
                begin
                    result := ((a + b) * c)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "嵌套括号三层",
            "code": """
                program test_nested_paren2;
                begin
                    result := (((a + b) * c) - d)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "复杂嵌套括号",
            "code": """
                program test_nested_paren3;
                begin
                    result := ((a + b) * (c - d)) / ((e + f) * (g - h))
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "深度嵌套括号",
            "code": """
                program test_deep_paren;
                begin
                    result := ((((a + b) * c) - d) / e)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "括号与负号",
            "code": """
                program test_paren_neg;
                begin
                    result := -(a + b);
                    x := (-a) * (-b);
                    y := -(a * b)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Logical expressions (and, or, not)
        {
            "name": "and 逻辑表达式",
            "code": """
                program test_and;
                begin
                    if (x > 0) and (y > 0) then
                        z := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "or 逻辑表达式",
            "code": """
                program test_or;
                begin
                    if (x < 0) or (y < 0) then
                        z := 0
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "not 逻辑表达式",
            "code": """
                program test_not;
                begin
                    if not (x = 0) then
                        y := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "and 和 or 组合",
            "code": """
                program test_and_or;
                begin
                    if (x > 0) and (y > 0) or (z > 0) then
                        result := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "not 和 and 组合",
            "code": """
                program test_not_and;
                begin
                    if not (x < 0) and (y > 0) then
                        result := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "not 和 or 组合",
            "code": """
                program test_not_or;
                begin
                    if not (x = 0) or not (y = 0) then
                        result := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "复杂逻辑表达式",
            "code": """
                program test_complex_logic;
                begin
                    if ((x > 0) and (y > 0)) or ((x < 0) and (y < 0)) then
                        result := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "多重 not 表达式",
            "code": """
                program test_multi_not;
                begin
                    if not (not (x > 0)) then
                        y := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "逻辑运算符优先级",
            "code": """
                program test_logic_prec;
                begin
                    if not (x > 0) and (y > 0) or (z > 0) then
                        result := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Relational expressions (all comparison operators)
        {
            "name": "小于运算符",
            "code": """
                program test_lt;
                begin
                    if a < b then
                        x := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "小于等于运算符",
            "code": """
                program test_le;
                begin
                    if a <= b then
                        x := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "大于运算符",
            "code": """
                program test_gt;
                begin
                    if a > b then
                        x := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "大于等于运算符",
            "code": """
                program test_ge;
                begin
                    if a >= b then
                        x := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "等于运算符",
            "code": """
                program test_eq;
                begin
                    if a = b then
                        x := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "不等于运算符",
            "code": """
                program test_ne;
                begin
                    if a <> b then
                        x := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "关系表达式比较算术表达式",
            "code": """
                program test_rel_arith;
                begin
                    if a + b < c * d then
                        x := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "关系表达式比较括号表达式",
            "code": """
                program test_rel_paren;
                begin
                    if (a + b) >= (c - d) then
                        x := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "多个关系表达式",
            "code": """
                program test_multi_rel;
                begin
                    if x < 10 then
                        y := 1;
                    if x <= 10 then
                        y := 2;
                    if x > 10 then
                        y := 3;
                    if x >= 10 then
                        y := 4;
                    if x = 10 then
                        y := 5;
                    if x <> 10 then
                        y := 6
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Complex nested expressions
        {
            "name": "复杂嵌套算术表达式",
            "code": """
                program test_complex_arith;
                begin
                    result := ((a + b) * (c - d)) / ((e * f) + (g / h))
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "复杂嵌套逻辑表达式",
            "code": """
                program test_complex_nested_logic;
                begin
                    if ((x > 0) and ((y > 0) or (z > 0))) or (not ((a < 0) and (b < 0))) then
                        result := 1
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "混合算术和关系表达式",
            "code": """
                program test_mixed_expr;
                begin
                    if (a + b * c) > (d - e / f) then
                        result := (x * y) + (z / w)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "深度嵌套混合表达式",
            "code": """
                program test_deep_mixed;
                begin
                    if ((((a + b) * c) > d) and (((e - f) / g) < h)) or (not (i = j)) then
                        result := ((x + y) * (z - w)) / ((p * q) + (r / s))
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "极度复杂表达式",
            "code": """
                program test_very_complex;
                begin
                    result := (((a + b) * (c - d)) / ((e + f) * (g - h))) + (((i * j) - (k / l)) * ((m + n) / (o - p)))
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        # Unmatched parentheses errors
        {
            "name": "缺少右括号",
            "code": """
                program test_missing_rparen;
                begin
                    result := (a + b
                end.
            """,
            "expected_keyword": "右括号"
        },
        {
            "name": "缺少左括号",
            "code": """
                program test_missing_lparen;
                begin
                    result := a + b)
                end.
            """,
            "expected_keyword": "语法错误"
        },
        {
            "name": "嵌套括号缺少右括号",
            "code": """
                program test_nested_missing_rparen;
                begin
                    result := ((a + b) * c
                end.
            """,
            "expected_keyword": "右括号"
        },
        {
            "name": "嵌套括号缺少左括号",
            "code": """
                program test_nested_missing_lparen;
                begin
                    result := a + b) * c)
                end.
            """,
            "expected_keyword": "语法错误"
        },
        {
            "name": "多个括号不匹配",
            "code": """
                program test_multi_mismatch;
                begin
                    result := ((a + b) * (c - d)
                end.
            """,
            "expected_keyword": "右括号"
        },
        {
            "name": "逻辑表达式括号不匹配",
            "code": """
                program test_logic_mismatch;
                begin
                    if ((x > 0) and (y > 0) then
                        z := 1
                end.
            """,
            "expected_keyword": "右括号"
        },
        # Incomplete operand errors
        {
            "name": "加法缺少右操作数",
            "code": """
                program test_incomplete_add;
                begin
                    result := a +
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "减法缺少右操作数",
            "code": """
                program test_incomplete_sub;
                begin
                    result := a -
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "乘法缺少右操作数",
            "code": """
                program test_incomplete_mul;
                begin
                    result := a *
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "除法缺少右操作数",
            "code": """
                program test_incomplete_div;
                begin
                    result := a /
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "缺少左操作数",
            "code": """
                program test_missing_left;
                begin
                    result := * 5
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "括号内表达式不完整",
            "code": """
                program test_incomplete_paren;
                begin
                    result := (a + )
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "关系运算符缺少右操作数",
            "code": """
                program test_incomplete_rel;
                begin
                    if x > then
                        y := 1
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "逻辑运算符缺少操作数",
            "code": """
                program test_incomplete_logic;
                begin
                    if (x > 0) and then
                        y := 1
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "连续运算符错误",
            "code": """
                program test_consecutive_ops;
                begin
                    result := a + * b
                end.
            """,
            "expected_keyword": "表达式错误"
        },
        {
            "name": "空括号",
            "code": """
                program test_empty_paren;
                begin
                    result := ()
                end.
            """,
            "expected_keyword": "表达式错误"
        },
    ],

    "变量声明与类型测试": [
        {
            "name": "简单变量声明和赋值",
            "code": """
                program var_simple;
                var
                    x: integer;
                    y: real;
                    flag: boolean;
                    msg: string;
                begin
                    x := 1;
                    y := 3.14;
                    flag := true;
                    msg := 'hello'
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "多行变量声明",
            "code": """
                program var_multi;
                var
                    a, b, c: integer;
                    s: string;
                begin
                    a := 1;
                    b := 2;
                    c := 3;
                    s := 'ok'
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "变量重复声明错误",
            "code": """
                program var_dup;
                var
                    x: integer;
                    x: integer;
                begin
                    x := 1
                end.
            """,
            "expected_keyword": "变量 'x' 重复声明"
        },
        {
            "name": "变量声明缺少类型",
            "code": """
                program var_missing_type;
                var
                    x, y:
                begin
                    x := 1
                end.
            """,
            "expected_keyword": "期望类型关键字"
        },
    ],

    "输入输出语句测试": [
        {
            "name": "write 和 read 语句",
            "code": """
                program io_basic;
                begin
                    write(123);
                    write('ok');
                    read(x)
                end.
            """,
            "expected": "该程序符合语法要求。"
        },
        {
            "name": "write 缺少左括号",
            "code": """
                program io_write_err1;
                begin
                    write 123
                end.
            """,
            "expected_keyword": "write 语句后期望 '('"
        },
        {
            "name": "write 缺少表达式",
            "code": """
                program io_write_err2;
                begin
                    write()
                end.
            """,
            "expected_keyword": "write 语句中缺少表达式"
        },
        {
            "name": "write 缺少右括号",
            "code": """
                program io_write_err3;
                begin
                    write(123
                end.
            """,
            "expected_keyword": "write 语句缺少 ')'"
        },
        {
            "name": "read 缺少左括号",
            "code": """
                program io_read_err1;
                begin
                    read x
                end.
            """,
            "expected_keyword": "read 语句后期望 '('"
        },
        {
            "name": "read 缺少变量名",
            "code": """
                program io_read_err2;
                begin
                    read()
                end.
            """,
            "expected_keyword": "read 语句中期望变量名"
        },
        {
            "name": "read 缺少右括号",
            "code": """
                program io_read_err3;
                begin
                    read(x
                end.
            """,
            "expected_keyword": "read 语句缺少 ')'"
        },
    ],

    "词法错误测试": [
        {
            "name": "非法字符",
            "code": """
                program lex_err1;
                begin
                    x := 1 @ 2
                end.
            """,
            "expected_keyword": "词法错误"
        },
        {
            "name": "未闭合的字符串",
            "code": """
                program lex_err2;
                begin
                    x := 'abc
                end.
            """,
            "expected_keyword": "词法错误"
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

    return passed_tests == total_tests


if __name__ == "__main__":
    run_all_tests()
