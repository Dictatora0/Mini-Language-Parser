#!/usr/bin/env python3
"""
Mini 语言分析器 - 最终演示
展示所有核心功能和4大改进
"""

from src import parse_to_ast, run_program, print_ast, Lexer

def demo_header():
    print("\n" + "🎯" * 35)
    print("   Mini 语言分析器 - 功能演示")
    print("   词法·语法·语义·解释·鲁棒")
    print("🎯" * 35 + "\n")

def demo_complete_program():
    """演示完整程序"""
    print("=" * 70)
    print("【演示1】完整程序 - 斐波那契数列")
    print("=" * 70)
    
    code = """
program fibonacci;
var
    n, a, b, temp, i: integer;
begin
    n := 10;
    a := 0;
    b := 1;
    i := 1;
    
    write(a);
    write(b);
    
    while i < n do
    begin
        temp := a + b;
        a := b;
        b := temp;
        write(temp);
        i := i + 1
    end
end.
"""
    
    print("\n源代码:")
    print(code)
    
    print("\n第1步：词法分析...")
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(f"✓ 生成 {len(tokens)} 个token")
    
    print("\n第2步：语法和语义分析...")
    ast, errors, st = parse_to_ast(code)
    if not errors:
        print("✓ 语法正确")
        print("✓ 语义检查通过")
        print(f"✓ 符号表: {list(st.get_global_scope().symbols.keys())}")
    else:
        print(f"✗ 错误: {errors}")
        return
    
    print("\n第3步：执行程序...")
    final_state, result = run_program(code)
    print(result)

def demo_semantic_analysis():
    """演示语义分析"""
    print("\n\n" + "=" * 70)
    print("【演示2】语义分析 - 4种类型检查")
    print("=" * 70)
    
    test_cases = [
        ("类型不匹配", 'program t; var x:integer; begin x := "text" end.'),
        ("未声明变量", 'program t; begin x := 10 end.'),
        ("重复声明", 'program t; var x:integer; x:real; begin end.'),
        ("条件类型错误", 'program t; var x:integer; begin if x then x:=1 end.'),
    ]
    
    for i, (name, code) in enumerate(test_cases, 1):
        print(f"\n{i}. {name}:")
        ast, errors, st = parse_to_ast(code)
        if errors:
            print(f"   ✓ 检测到: {errors[0][:65]}...")
        else:
            print(f"   ✗ 未检测到错误")

def demo_io():
    """演示I/O功能"""
    print("\n\n" + "=" * 70)
    print("【演示3】I/O功能 - write语句")
    print("=" * 70)
    
    code = """
program io_demo;
var x, y: integer;
    pi: real;
begin
    x := 100;
    y := 200;
    pi := 3.14159;
    
    write(x);
    write(y);
    write(x + y);
    write(pi)
end.
"""
    
    print("\n程序输出:")
    final_state, result = run_program(code)

def demo_robustness():
    """演示鲁棒性"""
    print("\n\n" + "=" * 70)
    print("【演示4】鲁棒性 - 边界和错误处理")
    print("=" * 70)
    
    tests = [
        ("除零保护", 'program t; var x:integer; begin x := 10/0 end.'),
        ("溢出检测", 'program t; var x:real; begin x:=1.0e308; x:=x*1000 end.'),
        ("超长标识符", f'program t; var {"a"*300}:integer; begin end.'),
        ("循环限制", 'program t; var x:integer; begin x:=1; while x>0 do x:=x+1 end.'),
    ]
    
    for i, (name, code) in enumerate(tests, 1):
        print(f"\n{i}. {name}:")
        try:
            # 词法检查
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            has_lex_error = any(t.type.name == 'ERROR' for t in tokens)
            
            if has_lex_error:
                error_token = [t for t in tokens if t.type.name == 'ERROR'][0]
                print(f"   ✓ 词法层捕获: {error_token.value[:50]}")
                continue
            
            # 语法/语义检查
            ast, errors, st = parse_to_ast(code)
            if errors:
                print(f"   ✓ 解析层捕获: {errors[0][:50]}...")
                continue
            
            # 运行时检查
            final_state, result = run_program(code)
            if "错误" in result or "超过" in result:
                print(f"   ✓ 运行时捕获: {result.split('：')[0] if '：' in result else result[:50]}...")
            else:
                print(f"   ⚠ 通过了（结果: {list(final_state.values())[0] if final_state else 'N/A'}）")
        except Exception as e:
            print(f"   ✓ 异常捕获: {str(e)[:50]}...")

def demo_ast():
    """演示AST生成"""
    print("\n\n" + "=" * 70)
    print("【演示5】AST生成和可视化")
    print("=" * 70)
    
    code = """
program ast_demo;
var x, y: integer;
begin
    x := 10;
    y := x * 2 + 5;
    if y > 20 then
        write(y)
end.
"""
    
    print("\n源代码:")
    print(code)
    
    ast, errors, st = parse_to_ast(code)
    if not errors:
        print("\nAST结构:")
        ast_str = print_ast(ast)
        # 只显示前500字符
        if len(ast_str) > 500:
            print(ast_str[:500] + "\n  ... (省略)")
        else:
            print(ast_str)

def print_summary():
    """打印总结"""
    print("\n\n" + "=" * 70)
    print("✅ 演示完成")
    print("=" * 70)
    
    print("\n📊 实现的功能:")
    print("\n1. 词法分析（Lexer）")
    print("   • 整数、浮点数、字符串、布尔值")
    print("   • 关键字识别、运算符、分隔符")
    print("   • 边界检查：长度限制、数值范围、跨行检测")
    
    print("\n2. 语法分析（Parser）")
    print("   • 递归下降分析")
    print("   • AST生成")
    print("   • 边界检查：递归深度、嵌套限制")
    
    print("\n3. 语义分析（Semantic Analyzer）⭐")
    print("   • 类型检查（INTEGER/REAL/BOOLEAN/STRING）")
    print("   • 运算合法性验证")
    print("   • 变量声明检查、重复声明检测")
    print("   • 条件表达式类型验证")
    
    print("\n4. 符号表（Symbol Table）⭐")
    print("   • 变量作用域管理")
    print("   • 类型信息存储")
    print("   • 声明检查")
    
    print("\n5. 解释器（Interpreter）⭐")
    print("   • 变量赋值和表达式计算")
    print("   • 控制流（if-then-else, while-do）")
    print("   • I/O操作（write, read）⭐")
    print("   • 边界检查：除零、溢出、循环限制")
    
    print("\n6. 鲁棒性增强⭐")
    print("   • 词法层：255字符标识符、10000字符字符串、100位数字")
    print("   • 语法层：100层递归、50层嵌套")
    print("   • 运行层：10000次循环限制、1000行输出限制")
    print("   • 错误处理：除零、溢出、NaN/Inf检测")
    
    print("\n🎯 4大核心改进已全部实现!")
    print("   1. ✅ 静态语义分析")
    print("   2. ✅ I/O功能（write/read）")
    print("   3. ✅ 类型精度（INTEGER vs REAL）")
    print("   4. ✅ 解释器鲁棒性")

def main():
    """主函数"""
    try:
        demo_header()
        demo_complete_program()
        demo_semantic_analysis()
        demo_io()
        demo_robustness()
        demo_ast()
        print_summary()
    except KeyboardInterrupt:
        print("\n\n⚠️ 演示被中断")
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
