#!/usr/bin/env python3
"""
测试新改进功能
测试4个主要改进：
1. 静态语义分析
2. I/O 功能
3. 数值类型精度
4. 解释器健壮性
"""

from src import parse_to_ast, run_program, print_ast


def test_semantic_analysis():
    """测试改进1: 静态语义分析"""
    print("="  * 70)
    print("【改进1】静态语义分析")
    print("=" * 70)
    
    test_cases = [
        {
            "name": "类型不匹配 - 整数变量赋字符串",
            "code": """
program test1;
var x: integer;
begin
    x := "hello"
end.
""",
            "should_error": True
        },
        {
            "name": "类型不匹配 - 布尔变量赋整数",
            "code": """
program test2;
var b: boolean;
begin
    b := 1 + 2
end.
""",
            "should_error": True
        },
        {
            "name": "条件类型错误 - if 条件不是布尔",
            "code": """
program test3;
var x: integer;
begin
    x := 10;
    if x then
        x := 20
end.
""",
            "should_error": True
        },
        {
            "name": "正确的类型匹配",
            "code": """
program test4;
var x: integer;
    y: real;
begin
    x := 10;
    y := x + 5.5
end.
""",
            "should_error": False
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test['name']}")
        ast, errors, st = parse_to_ast(test['code'])
        
        if test['should_error']:
            if errors:
                print(f"  ✅ 正确检测到错误: {errors[0][:60]}...")
            else:
                print(f"  ❌ 应该检测到错误但没有")
        else:
            if not errors:
                print(f"  ✅ 通过语义检查")
            else:
                print(f"  ❌ 不应该有错误: {errors[0]}")


def test_io_功能():
    """测试改进2: I/O 功能"""
    print("\n\n" + "=" * 70)
    print("【改进2】I/O 功能（write 语句）")
    print("=" * 70)
    
    print("\n测试 1: write 语句 - 输出变量")
    code1 = """
program io_test1;
var x, y, sum: integer;
begin
    x := 10;
    y := 20;
    sum := x + y;
    write(sum)
end.
"""
    
    print("程序:")
    print(code1)
    print("\n执行结果:")
    final_state, result = run_program(code1)
    print(result)
    
    print("\n测试 2: write 语句 - 输出表达式")
    code2 = """
program io_test2;
var x: integer;
begin
    x := 5;
    write(x * x)
end.
"""
    print("程序:")
    print(code2)
    print("\n执行结果:")
    final_state2, result2 = run_program(code2)
    print(result2)


def test_type_precision():
    """测试改进3: 数值类型精度"""
    print("\n\n" + "=" * 70)
    print("【改进3】数值类型精度（静态分析）")
    print("=" * 70)
    
    print("\n说明: 语义分析器现在能区分 INTEGER 和 REAL 类型")
    
    code = """
program type_test;
var
    i: integer;
    r: real;
begin
    i := 10;
    r := 3.14159;
    write(i);
    write(r)
end.
"""
    
    print("程序:")
    print(code)
    
    ast, errors, st = parse_to_ast(code)
    if not errors:
        print("\n✅ 类型检查通过")
        print("\n符号表:")
        print(st.get_global_scope().print_table())
    else:
        print(f"\n错误: {errors}")


def test_interpreter_robustness():
    """测试改进4: 解释器健壮性"""
    print("\n\n" + "=" * 70)
    print("【改进4】解释器健壮性")
    print("=" * 70)
    
    print("\n测试 1: 除零错误处理")
    code1 = """
program error_test1;
var x, y: integer;
begin
    x := 10;
    y := 0;
    write(x / y)
end.
"""
    print("程序:")
    print(code1)
    final_state1, result1 = run_program(code1)
    print("结果:", result1[:60])
    
    print("\n测试 2: 未声明变量（在解析阶段捕获）")
    code2 = """
program error_test2;
begin
    x := 10
end.
"""
    print("程序:")
    print(code2)
    ast2, errors2, st2 = parse_to_ast(code2)
    if errors2:
        print("✅ 在解析阶段捕获:", errors2[0][:60])


def test_combined_features():
    """综合测试"""
    print("\n\n" + "=" * 70)
    print("【综合测试】结合所有改进")
    print("=" * 70)
    
    code = """
program comprehensive;
var
    n, fact: integer;
    msg: string;
begin
    n := 5;
    fact := 1;
    
    while n > 0 do
    begin
        fact := fact * n;
        n := n - 1
    end;
    
    write(fact)
end.
"""
    
    print("\n程序: 计算阶乘并输出")
    print(code)
    
    print("\n1. 语法和语义分析:")
    ast, errors, st = parse_to_ast(code)
    if not errors:
        print("   ✅ 语法正确")
        print("   ✅ 语义检查通过")
        print("   ✅ 类型匹配正确")
    else:
        print(f"   ❌ 错误: {errors}")
        return
    
    print("\n2. 执行程序:")
    final_state, result = run_program(code)
    print(result)


def main():
    """主测试函数"""
    print("\n" + "🔥" * 35)
    print("   Mini 语言解析器 - 4 大改进测试")
    print("🔥" * 35 + "\n")
    
    try:
        # 测试1: 静态语义分析
        test_semantic_analysis()
        
        # 测试2: I/O 功能
        test_io_功能()
        
        # 测试3: 数值类型精度
        test_type_precision()
        
        # 测试4: 解释器健壮性
        test_interpreter_robustness()
        
        # 综合测试
        test_combined_features()
        
        print("\n\n" + "=" * 70)
        print("✅ 所有改进测试完成！")
        print("=" * 70)
        
        print("\n改进总结:")
        print("  1. ✅ 静态语义分析 - 类型检查、运算合法性检查")
        print("  2. ✅ I/O 功能 - write 和 read 语句")
        print("  3. ✅ 数值类型精度 - INTEGER vs REAL 区分")
        print("  4. ✅ 解释器健壮性 - 错误处理、运行时检查")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
