#!/usr/bin/env python3
"""
Mini 语言编译器 - 改进功能演示
展示所有增强功能和改进
"""

from src import (
    parse_from_source, parse_to_ast, print_ast, ast_to_dict,
    run_program, analyze_semantics
)
import json


def print_section(title: str):
    """打印章节标题"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def demo_basic_parsing():
    """演示基础语法分析"""
    print_section("1. 基础语法分析")

    code = """
    program simple;
    var x, y: integer;
    begin
        x := 10;
        y := 20;
        x := x + y
    end.
    """

    print("源代码:")
    print(code)

    result = parse_from_source(code)
    print("\n分析结果:")
    print(result)


def demo_ast_generation():
    """演示 AST 生成"""
    print_section("2. AST 生成与可视化")

    code = """
    program ast_demo;
    var result: integer;
    begin
        result := (10 + 20) * 3
    end.
    """

    print("源代码:")
    print(code)

    ast, errors, symbol_table = parse_to_ast(code, enable_semantic_check=False)

    if not errors:
        print("\nAST 树形结构:")
        print(print_ast(ast))

        print("\nAST 字典表示 (JSON):")
        ast_dict = ast_to_dict(ast)
        print(json.dumps(ast_dict, indent=2, ensure_ascii=False))
    else:
        print("\n错误:")
        for error in errors:
            print(error)


def demo_symbol_table():
    """演示符号表管理"""
    print_section("3. 符号表与变量声明")

    code = """
    program symbol_demo;
    var
        x, y: integer;
        result: real;
        flag: boolean;
        message: string;
    begin
        x := 10;
        y := 20;
        result := x + y
    end.
    """

    print("源代码:")
    print(code)

    ast, errors, symbol_table = parse_to_ast(code)

    if not errors:
        print("\n符号表内容:")
        print(symbol_table.get_global_scope().print_table())
    else:
        print("\n错误:")
        for error in errors:
            print(error)


def demo_semantic_analysis():
    """演示语义分析"""
    print_section("4. 语义分析 - 类型检查")

    # 正确的程序
    print("\n【示例 4.1】类型正确的程序:")
    code_correct = """
    program type_correct;
    var x, y: integer;
    begin
        x := 10;
        y := x + 20
    end.
    """
    print(code_correct)

    ast, errors, symbol_table = parse_to_ast(code_correct)
    if errors:
        print("错误:")
        for error in errors:
            print(error)
    else:
        print("类型检查通过")

    # 类型错误的程序
    print("\n【示例 4.2】类型错误的程序:")
    code_error = """
    program type_error;
    var x: integer; s: string;
    begin
        x := "hello"
    end.
    """
    print(code_error)

    ast, errors, symbol_table = parse_to_ast(code_error)
    if errors:
        print("检测到语义错误:")
        for error in errors:
            print(error)

    # 未声明变量
    print("\n【示例 4.3】未声明变量:")
    code_undeclared = """
    program undeclared;
    var x: integer;
    begin
        y := 10
    end.
    """
    print(code_undeclared)

    ast, errors, symbol_table = parse_to_ast(code_undeclared)
    if errors:
        print("检测到语义错误:")
        for error in errors:
            print(error)


def demo_enhanced_lexer():
    """演示增强的词法分析"""
    print_section("5. 增强的词法分析")

    code = """
    program lexer_demo;
    var
        i: integer;
        pi: real;
        flag: boolean;
        msg: string;
    begin
        i := 42;
        pi := 3.14159;
        flag := true;
        msg := "Hello, World!"
    end.
    """

    print("源代码:")
    print(code)

    from src.lexer import Lexer
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    print("\nToken 流 (前 30 个):")
    for i, token in enumerate(tokens[:30]):
        print(f"  {i+1:2d}. {token.type.name:15s} '{token.value}'")

    if len(tokens) > 30:
        print(f"  ... (还有 {len(tokens) - 30} 个 tokens)")


def demo_error_handling():
    """演示错误处理"""
    print_section("6. 增强的错误处理")

    print("\n【示例 6.1】语法错误 - 缺少分号:")
    code_syntax = """
    program syntax_error;
    begin
        x := 10
        y := 20
    end.
    """
    print(code_syntax)
    result = parse_from_source(code_syntax)
    print("\n错误信息:")
    print(result)

    print("\n【示例 6.2】表达式错误 - 不完整:")
    code_expr = """
    program expr_error;
    begin
        x := 10 +
    end.
    """
    print(code_expr)
    result = parse_from_source(code_expr)
    print("\n错误信息:")
    print(result)

    print("\n【示例 6.3】除零错误检测:")
    code_div = """
    program div_zero;
    var x: integer;
    begin
        x := 10 / 0
    end.
    """
    print(code_div)
    ast, errors, symbol_table = parse_to_ast(code_div)
    if errors:
        print("\n错误信息:")
        for error in errors:
            print(error)


def demo_interpreter():
    """演示解释器"""
    print_section("7. 程序执行 - 解释器")

    print("\n【示例 7.1】简单计算:")
    code_calc = """
    program calculator;
    var x, y, sum, product: integer;
    begin
        x := 10;
        y := 20;
        sum := x + y;
        product := x * y
    end.
    """
    print(code_calc)

    final_state, result = run_program(code_calc)
    print("\n执行结果:")
    print(result)

    print("\n【示例 7.2】条件语句:")
    code_if = """
    program conditional;
    var x, y, max: integer;
    begin
        x := 15;
        y := 20;
        if x > y then
            max := x
        else
            max := y
    end.
    """
    print(code_if)

    final_state, result = run_program(code_if)
    print("\n执行结果:")
    print(result)

    print("\n【示例 7.3】循环计算阶乘:")
    code_factorial = """
    program factorial;
    var n, fact: integer;
    begin
        n := 5;
        fact := 1;
        while n > 0 do
        begin
            fact := fact * n;
            n := n - 1
        end
    end.
    """
    print(code_factorial)

    final_state, result = run_program(code_factorial)
    print("\n执行结果:")
    print(result)


def demo_complex_program():
    """演示复杂程序"""
    print_section("8. 复杂程序示例")

    code = """
    program fibonacci;
    var n, a, b, temp, i: integer;
    begin
        n := 10;
        a := 0;
        b := 1;
        i := 1;

        while i < n do
        begin
            temp := a + b;
            a := b;
            b := temp;
            i := i + 1
        end
    end.
    """

    print("源代码 - 斐波那契数列:")
    print(code)

    print("\n【语法分析】")
    ast, errors, symbol_table = parse_to_ast(code)
    if errors:
        print("错误:")
        for error in errors:
            print(error)
    else:
        print("语法正确")
        print("\n符号表:")
        print(symbol_table.get_global_scope().print_table())

    print("\n【程序执行】")
    final_state, result = run_program(code)
    print(result)


def demo_all_features():
    """演示所有功能"""
    print("\n" + "=" * 80)
    print("  Mini 语言编译器 - 完整功能演示")
    print("  展示所有增强功能和改进")
    print("=" * 80)

    demos = [
        ("基础语法分析", demo_basic_parsing),
        ("AST 生成", demo_ast_generation),
        ("符号表管理", demo_symbol_table),
        ("语义分析", demo_semantic_analysis),
        ("增强词法分析", demo_enhanced_lexer),
        ("错误处理", demo_error_handling),
        ("解释器执行", demo_interpreter),
        ("复杂程序", demo_complex_program),
    ]

    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            demo_func()
        except Exception as e:
            print(f"\n演示 {i} ({name}) 出错: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 80)
    print("  演示完成！")
    print("=" * 80)


if __name__ == "__main__":
    demo_all_features()
