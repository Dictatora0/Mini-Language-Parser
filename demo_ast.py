#!/usr/bin/env python3
"""
Mini 语言增强功能演示
展示 AST 生成、符号表、解释器等新功能
"""

from src import parse_to_ast, print_ast, run_program

# 示例程序
EXAMPLES = {
    "1. 变量声明和赋值": """
program var_demo;
var
    x, y : integer;
    result : real;
begin
    x := 10;
    y := 20;
    result := (x + y) * 1.5
end.
""",
    
    "2. 阶乘计算": """
program factorial;
var
    n, fact : integer;
begin
    n := 5;
    fact := 1;
    while n > 0 do
    begin
        fact := fact * n;
        n := n - 1
    end
end.
""",
    
    "3. 条件判断": """
program if_demo;
var
    score : integer;
    grade : integer;
begin
    score := 85;
    if score >= 90 then
        grade := 1
    else
        if score >= 80 then
            grade := 2
        else
            grade := 3
end.
""",
    
    "4. 布尔运算": """
program boolean_demo;
var
    a, b : integer;
    result : boolean;
begin
    a := 10;
    b := 20;
    result := (a > 5) and (b < 30)
end.
""",
    
    "5. 浮点数运算": """
program float_demo;
var
    pi : real;
    radius : real;
    area : real;
begin
    pi := 3.14159;
    radius := 5.0;
    area := pi * radius * radius
end.
""",
}


def demo_ast_generation():
    """演示 AST 生成"""
    print("=" * 80)
    print("【演示 1】AST 生成与可视化")
    print("=" * 80)
    
    source_code = EXAMPLES["1. 变量声明和赋值"]
    
    print("\n源代码:")
    print(source_code)
    
    # 解析生成 AST
    ast, errors, symbol_table = parse_to_ast(source_code)
    
    if errors:
        print("\n错误:")
        for error in errors:
            print(error)
        return
    
    # 打印 AST
    print("\n=== 抽象语法树 (AST) ===")
    print(print_ast(ast))
    
    # 打印符号表
    print("\n=== 符号表 ===")
    print(symbol_table.get_global_scope().print_table())


def demo_interpreter():
    """演示解释器"""
    print("\n\n" + "=" * 80)
    print("【演示 2】程序执行（解释器）")
    print("=" * 80)
    
    for title, source_code in EXAMPLES.items():
        print(f"\n{title}")
        print("-" * 60)
        print("源代码:")
        print(source_code)
        
        # 运行程序
        final_state, result = run_program(source_code, debug=False)
        
        print("\n执行结果:")
        print(result)


def demo_error_handling():
    """演示错误处理"""
    print("\n\n" + "=" * 80)
    print("【演示 3】错误处理与提示")
    print("=" * 80)
    
    error_examples = {
        "未声明变量": """
program error1;
begin
    x := 10
end.
""",
        "变量重复声明": """
program error2;
var
    x : integer;
    x : real;
begin
    x := 10
end.
""",
        "类型不匹配（词法错误）": """
program error3;
var
    s : string;
begin
    s := "hello world
end.
""",
    }
    
    for title, source_code in error_examples.items():
        print(f"\n{title}")
        print("-" * 60)
        print("源代码:")
        print(source_code)
        
        # 尝试解析
        ast, errors, symbol_table = parse_to_ast(source_code)
        
        if errors:
            print("\n检测到的错误:")
            for error in errors:
                print(error)
        else:
            print("\n未检测到错误（可能需要进一步改进）")


def demo_features_comparison():
    """演示旧版 vs 新版功能对比"""
    print("\n\n" + "=" * 80)
    print("【演示 4】功能对比：旧版 vs 新版")
    print("=" * 80)
    
    source_code = EXAMPLES["2. 阶乘计算"]
    
    print("\n测试程序:")
    print(source_code)
    
    # 旧版 Parser（只检查语法）
    print("\n--- 旧版 Parser（仅语法检查）---")
    from src import parse_from_source
    result = parse_from_source(source_code)
    print(result)
    
    # 新版 ASTParser（生成 AST + 符号表检查）
    print("\n--- 新版 ASTParser（AST + 符号表）---")
    ast, errors, symbol_table = parse_to_ast(source_code)
    if ast:
        print("✓ 语法正确")
        print("✓ AST 已生成")
        print("✓ 符号表已建立")
        print(f"✓ 声明了 {len(symbol_table.get_global_scope().symbols)} 个变量")
    
    # 解释器（执行程序）
    print("\n--- 解释器（执行程序）---")
    final_state, result = run_program(source_code)
    print(f"✓ 程序执行完成")
    print(f"✓ 计算结果: fact = {final_state.get('fact', 'N/A')}")


def main():
    """主函数"""
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "Mini 语言增强功能演示" + " " * 37 + "║")
    print("║" + " " * 15 + "AST 生成 | 符号表 | 解释器 | 错误处理" + " " * 23 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # 演示 1: AST 生成
    demo_ast_generation()
    
    # 演示 2: 解释器
    demo_interpreter()
    
    # 演示 3: 错误处理
    demo_error_handling()
    
    # 演示 4: 功能对比
    demo_features_comparison()
    
    print("\n\n" + "=" * 80)
    print("演示完成！")
    print("=" * 80)
    print("\n主要改进:")
    print("  ✓ AST 生成 - 不只是识别器，而是生成完整的语法树")
    print("  ✓ 符号表 - 跟踪变量声明，检查未声明变量")
    print("  ✓ 变量声明 - 支持 var 关键字和类型声明")
    print("  ✓ 浮点数支持 - 词法分析器支持小数")
    print("  ✓ 字符串支持 - 支持字符串字面量")
    print("  ✓ 布尔类型 - true/false 关键字")
    print("  ✓ 解释器 - 可以实际执行程序并查看结果")
    print("  ✓ 增强的错误提示 - 显示错误行和指针")


if __name__ == "__main__":
    main()
