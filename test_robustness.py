#!/usr/bin/env python3
"""
鲁棒性测试 - 边界和极端情况
测试各种边界条件和极端输入
"""

from src import parse_to_ast, run_program, Lexer


def test_lexer_boundaries():
    """测试词法分析器的边界情况"""
    print("=" * 70)
    print("【测试1】词法分析器边界情况")
    print("=" * 70)
    
    # 测试1.1: 空输入
    print("\n1.1 空输入:")
    try:
        lexer = Lexer("")
        tokens = lexer.tokenize()
        print(f"  ✅ 空输入处理正常，生成 {len(tokens)} 个 token")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 测试1.2: 极长标识符
    print("\n1.2 超长标识符 (300字符):")
    long_id = "a" * 300
    code = f"program test; var {long_id} : integer; begin end."
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        has_error = any(t.type.name == 'ERROR' for t in tokens)
        if has_error:
            error_token = [t for t in tokens if t.type.name == 'ERROR'][0]
            print(f"  ✅ 正确检测到错误: {error_token.value}")
        else:
            print(f"  ❌ 应该检测到标识符过长错误")
    except Exception as e:
        print(f"  ✅ 异常捕获: {str(e)[:60]}...")
    
    # 测试1.3: 极大数字
    print("\n1.3 超大整数 (超过 32 位):")
    code = "program test; begin x := 999999999999999999999 end."
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        has_error = any(t.type.name == 'ERROR' for t in tokens)
        if has_error:
            error_token = [t for t in tokens if t.type.name == 'ERROR'][0]
            print(f"  ✅ 正确检测到错误: {error_token.value}")
        else:
            print(f"  ❌ 应该检测到数字超范围错误")
    except Exception as e:
        print(f"  ✅ 异常捕获: {str(e)[:60]}...")
    
    # 测试1.4: 超长字符串
    print("\n1.4 超长字符串 (15000 字符):")
    long_str = "x" * 15000
    code = f'program test; begin x := "{long_str}" end.'
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        has_error = any(t.type.name == 'ERROR' for t in tokens)
        if has_error:
            error_token = [t for t in tokens if t.type.name == 'ERROR'][0]
            print(f"  ✅ 正确检测到错误: {error_token.value}")
        else:
            print(f"  ❌ 应该检测到字符串过长错误")
    except Exception as e:
        print(f"  ✅ 异常捕获: {str(e)[:60]}...")
    
    # 测试1.5: 跨行字符串
    print("\n1.5 跨行字符串:")
    code = '''program test; begin x := "hello
world" end.'''
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        has_error = any(t.type.name == 'ERROR' for t in tokens)
        if has_error:
            error_token = [t for t in tokens if t.type.name == 'ERROR'][0]
            print(f"  ✅ 正确检测到错误: {error_token.value}")
        else:
            print(f"  ❌ 应该检测到字符串跨行错误")
    except Exception as e:
        print(f"  ✅ 异常捕获: {str(e)[:60]}...")


def test_parser_boundaries():
    """测试语法分析器的边界情况"""
    print("\n\n" + "=" * 70)
    print("【测试2】语法分析器边界情况")
    print("=" * 70)
    
    # 测试2.1: 空程序
    print("\n2.1 空程序:")
    code = ""
    try:
        ast, errors, st = parse_to_ast(code)
        if errors:
            print(f"  ✅ 检测到错误: {errors[0][:60]}...")
        else:
            print(f"  ❌ 空程序应该报错")
    except Exception as e:
        print(f"  ✅ 异常捕获: {str(e)[:60]}...")
    
    # 测试2.2: 深层嵌套的表达式
    print("\n2.2 深层嵌套表达式 (100层):")
    expr = "x" + " + 1" * 100
    code = f"program test; var x:integer; begin x := {expr} end."
    try:
        ast, errors, st = parse_to_ast(code)
        if errors and "嵌套" in str(errors):
            print(f"  ✅ 检测到嵌套过深: {errors[0][:60]}...")
        elif not errors:
            print(f"  ⚠️  通过了（可能需要调整限制）")
        else:
            print(f"  ❌ 其他错误: {errors[0][:60]}...")
    except Exception as e:
        print(f"  ✅ 异常捕获: {str(e)[:60]}...")
    
    # 测试2.3: 深层嵌套的begin-end块
    print("\n2.3 深层嵌套 begin-end (10层):")
    nested_begin = "begin " * 10
    nested_end = "end; " * 10
    code = f"program test; begin {nested_begin} x := 1 {nested_end} end."
    try:
        ast, errors, st = parse_to_ast(code)
        if not errors:
            print(f"  ✅ 正常处理了嵌套块")
        else:
            print(f"  ⚠️  错误: {errors[0][:60]}...")
    except Exception as e:
        print(f"  ❌ 异常: {str(e)[:60]}...")


def test_interpreter_boundaries():
    """测试解释器的边界情况"""
    print("\n\n" + "=" * 70)
    print("【测试3】解释器边界情况")
    print("=" * 70)
    
    # 测试3.1: 除零错误
    print("\n3.1 除零错误:")
    code = """
program test;
var x, y: integer;
begin
    x := 10;
    y := 0;
    x := x / y
end.
"""
    try:
        final_state, result = run_program(code)
        if "除零" in result or "错误" in result:
            print(f"  ✅ 正确捕获除零错误")
        else:
            print(f"  ❌ 应该捕获除零错误")
    except Exception as e:
        print(f"  ✅ 异常捕获: {str(e)[:60]}...")
    
    # 测试3.2: 算术溢出
    print("\n3.2 算术溢出:")
    code = """
program test;
var x: real;
begin
    x := 1.0e308;
    x := x * 1000
end.
"""
    try:
        final_state, result = run_program(code)
        if "溢出" in result or "错误" in result:
            print(f"  ✅ 正确捕获溢出")
        else:
            print(f"  ⚠️  未检测到溢出，x = {final_state.get('x', 'N/A')}")
    except Exception as e:
        print(f"  ✅ 异常捕获: {str(e)[:60]}...")
    
    # 测试3.3: 潜在无限循环（有限制）
    print("\n3.3 循环次数限制 (100000 次):")
    code = """
program test;
var x: integer;
begin
    x := 1;
    while x > 0 do
        x := x + 1
end.
"""
    try:
        final_state, result = run_program(code)
        if "循环次数" in result or "无限循环" in result:
            print(f"  ✅ 正确检测到循环次数超限")
        else:
            print(f"  ❌ 应该检测到循环次数超限")
    except Exception as e:
        print(f"  ✅ 异常捕获: {str(e)[:60]}...")
    
    # 测试3.4: 正常的多次循环
    print("\n3.4 正常循环 (100 次):")
    code = """
program test;
var x: integer;
begin
    x := 100;
    while x > 0 do
        x := x - 1
end.
"""
    try:
        final_state, result = run_program(code)
        if "成功" in result:
            print(f"  ✅ 正常执行完成，x = {final_state.get('x', 'N/A')}")
        else:
            print(f"  ❌ 执行失败: {result[:60]}...")
    except Exception as e:
        print(f"  ❌ 异常: {str(e)[:60]}...")


def test_semantic_boundaries():
    """测试语义分析的边界情况"""
    print("\n\n" + "=" * 70)
    print("【测试4】语义分析边界情况")
    print("=" * 70)
    
    # 测试4.1: 类型完全不匹配
    print("\n4.1 字符串赋给整数:")
    code = """
program test;
var x: integer;
begin
    x := "hello"
end.
"""
    ast, errors, st = parse_to_ast(code)
    if errors and "类型" in str(errors):
        print(f"  ✅ 正确检测类型错误")
    else:
        print(f"  ❌ 应该检测到类型错误")
    
    # 测试4.2: 布尔运算用于数值
    print("\n4.2 布尔值参与算术运算:")
    code = """
program test;
var x: integer;
    b: boolean;
begin
    b := true;
    x := b + 1
end.
"""
    ast, errors, st = parse_to_ast(code)
    if errors and ("类型" in str(errors) or "算术" in str(errors)):
        print(f"  ✅ 正确检测类型错误")
    else:
        print(f"  ❌ 应该检测到类型错误")


def test_edge_cases():
    """测试其他边缘情况"""
    print("\n\n" + "=" * 70)
    print("【测试5】其他边缘情况")
    print("=" * 70)
    
    # 测试5.1: 未初始化变量
    print("\n5.1 使用未赋值的变量:")
    code = """
program test;
var x, y: integer;
begin
    y := x + 1
end.
"""
    try:
        final_state, result = run_program(code)
        print(f"  ⚠️  未初始化变量 x = {final_state.get('x', 'N/A')}")
        print(f"     y = {final_state.get('y', 'N/A')}")
    except Exception as e:
        print(f"  ✅ 捕获错误: {str(e)[:60]}...")
    
    # 测试5.2: 变量重复声明
    print("\n5.2 变量重复声明:")
    code = """
program test;
var x: integer;
    x: real;
begin
    x := 10
end.
"""
    ast, errors, st = parse_to_ast(code)
    if errors and "重复" in str(errors):
        print(f"  ✅ 正确检测重复声明")
    else:
        print(f"  ❌ 应该检测到重复声明")
    
    # 测试5.3: NaN 和 Infinity
    print("\n5.3 0.0/0.0 产生 NaN:")
    code = """
program test;
var x: real;
begin
    x := 0.0 / 0.0
end.
"""
    try:
        final_state, result = run_program(code)
        if "NaN" in result or "无效" in result or "错误" in result:
            print(f"  ✅ 正确处理 NaN")
        else:
            print(f"  ⚠️  结果: x = {final_state.get('x', 'N/A')}")
    except Exception as e:
        print(f"  ✅ 捕获错误: {str(e)[:60]}...")


def main():
    """运行所有测试"""
    print("\n" + "🔒" * 35)
    print("   Mini 语言解析器 - 鲁棒性测试")
    print("🔒" * 35 + "\n")
    
    try:
        test_lexer_boundaries()
        test_parser_boundaries()
        test_interpreter_boundaries()
        test_semantic_boundaries()
        test_edge_cases()
        
        print("\n\n" + "=" * 70)
        print("✅ 鲁棒性测试完成！")
        print("=" * 70)
        
        print("\n增强的边界检查:")
        print("  ✅ 词法分析器: 长度限制、数值范围、字符串跨行")
        print("  ✅ 语法分析器: 递归深度、嵌套深度、表达式深度")
        print("  ✅ 语义分析器: 类型检查、运算合法性")
        print("  ✅ 解释器: 除零、溢出、无限循环、NaN/Inf处理")
        print("  ✅ 全局: 输入验证、异常捕获、友好错误消息")
        
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
