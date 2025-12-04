"""
Mini 语言语法分析器 - 主程序
支持命令行和交互式两种使用方式
"""

import sys
import os
from src.lexer import Lexer
from src.parser import parse_from_source, parse_from_file


def print_banner():
    """打印程序标题"""
    print("=" * 70)
    print("   Mini 语言语法分析器 (Mini Language Parser)")
    print("   编译原理课程实验 - 语法分析程序")
    print("=" * 70)


def print_usage():
    """打印使用说明"""
    print("\n使用方法:")
    print("  1. 从源文件分析:")
    print("     python main.py <source_file>")
    print("  2. 从 Token 文件分析:")
    print("     python main.py -t <token_file>")
    print("  3. 交互式输入:")
    print("     python main.py -i")
    print("  4. 运行测试:")
    print("     python main.py --test")
    print("\n示例:")
    print("  python main.py example.txt")
    print("  python main.py -t tokens.txt")
    print("  python main.py -i")


def analyze_source_file(filepath: str):
    """分析源代码文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        print(f"\n正在分析文件: {filepath}")
        print("-" * 70)
        print("源代码:")
        print(source_code)
        print("-" * 70)
        
        # 词法分析
        print("\n【词法分析】")
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        print(f"Token 总数: {len(tokens)}")
        print("Token 流:")
        for i, token in enumerate(tokens[:20]):  # 只显示前20个
            print(f"  {i+1}. {token}")
        if len(tokens) > 20:
            print(f"  ... (还有 {len(tokens) - 20} 个 tokens)")
        
        # 语法分析
        print("\n【语法分析】")
        result = parse_from_source(source_code)
        print(result)
        
        return result
        
    except FileNotFoundError:
        print(f"错误: 文件 '{filepath}' 不存在")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None


def analyze_token_file(filepath: str):
    """分析 Token 文件"""
    try:
        print(f"\n正在分析 Token 文件: {filepath}")
        print("-" * 70)
        
        result = parse_from_file(filepath)
        print("\n【语法分析结果】")
        print(result)
        
        return result
        
    except FileNotFoundError:
        print(f"错误: 文件 '{filepath}' 不存在")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None


def interactive_mode():
    """交互式输入模式"""
    print("\n进入交互式模式")
    print("请输入 Mini 语言源代码（输入 'END' 单独一行结束输入）:")
    print("-" * 70)
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    
    source_code = '\n'.join(lines)
    
    if not source_code.strip():
        print("错误: 输入为空")
        return
    
    print("-" * 70)
    print("\n【输入的源代码】")
    print(source_code)
    
    print("\n【语法分析结果】")
    result = parse_from_source(source_code)
    print(result)


def run_tests():
    """运行测试套件"""
    print("\n运行测试套件...")
    print("-" * 70)
    try:
        from tests.test_cases import run_all_tests
        run_all_tests()
    except ImportError:
        print("错误: 无法导入测试模块 tests/test_cases.py")


def run_demo():
    """运行示例程序"""
    print("\n运行示例程序...")
    print("-" * 70)
    
    demo_programs = [
        {
            "name": "示例1: 简单赋值和条件",
            "code": """
program example1;
begin
    x := 10;
    y := 20;
    if x < y then
        z := x + y
    else
        z := x - y
end.
            """
        },
        {
            "name": "示例2: 循环和嵌套",
            "code": """
program example2;
begin
    i := 10;
    sum := 0;
    while i > 0 do
    begin
        sum := sum + i;
        i := i - 1
    end
end.
            """
        },
        {
            "name": "示例3: 错误程序（表达式错误）",
            "code": """
program error_example;
begin
    i := 1 + 
end.
            """
        },
    ]
    
    for demo in demo_programs:
        print(f"\n{'=' * 70}")
        print(f"{demo['name']}")
        print('=' * 70)
        print("源代码:")
        print(demo['code'])
        print("\n分析结果:")
        result = parse_from_source(demo['code'])
        print(result)


def main():
    """主函数"""
    print_banner()
    
    if len(sys.argv) == 1:
        # 无参数，显示使用说明并运行示例
        print_usage()
        
        while True:
            print("\n" + "=" * 70)
            print("请选择操作:")
            print("  1. 运行示例程序")
            print("  2. 运行完整测试")
            print("  3. 交互式输入")
            print("  4. 分析文件")
            print("  0. 退出")
            print("=" * 70)
            
            choice = input("请输入选项 (0-4): ").strip()
            
            if choice == '1':
                run_demo()
            elif choice == '2':
                run_tests()
            elif choice == '3':
                interactive_mode()
            elif choice == '4':
                filepath = input("请输入文件路径: ").strip()
                if filepath:
                    analyze_source_file(filepath)
            elif choice == '0':
                print("\n感谢使用！")
                break
            else:
                print("无效选项，请重新选择")
    
    elif sys.argv[1] == '-i':
        # 交互式模式
        interactive_mode()
    
    elif sys.argv[1] == '--test':
        # 运行测试
        run_tests()
    
    elif sys.argv[1] == '--demo':
        # 运行示例
        run_demo()
    
    elif sys.argv[1] == '-t':
        # 从 Token 文件分析
        if len(sys.argv) < 3:
            print("错误: 请指定 Token 文件路径")
            print_usage()
            sys.exit(1)
        analyze_token_file(sys.argv[2])
    
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        # 显示帮助
        print_usage()
    
    else:
        # 分析源文件
        analyze_source_file(sys.argv[1])


if __name__ == "__main__":
    main()
