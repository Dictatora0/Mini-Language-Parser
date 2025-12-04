# Mini 语言编译器

编译原理课程实验项目。包含完整的编译器前端（词法、语法、语义分析）和解释器。

## 功能

### 编译器组件

- 词法分析器：识别 token，支持整数、浮点数、字符串、布尔值
- 语法分析器：递归下降解析，生成 AST
- 语义分析器：类型检查、变量声明检查、运算合法性验证
- 符号表：作用域管理、类型记录
- 解释器：执行 AST，支持 I/O 操作

### 语言特性

**数据类型**

- integer, real, boolean, string

**运算符**

- 算术：`+` `-` `*` `/`
- 关系：`<` `<=` `>` `>=` `=` `<>`
- 逻辑：`and` `or` `not`

**语句**

- 变量声明：`var x, y : integer;`
- 赋值：`x := expression`
- 条件：`if condition then statement [else statement]`
- 循环：`while condition do statement`
- I/O：`write(expression)` `read(variable)`

**程序结构**

```pascal
program name;
var
    declarations
begin
    statements
end.
```

## 安装使用

### 要求

- Python 3.7+
- 无额外依赖

### 快速开始

**1. 语法检查**

```python
from src import parse_from_source

code = "program test; var x:integer; begin x := 10 end."
result = parse_from_source(code)
print(result)
```

**2. 生成 AST**

```python
from src import parse_to_ast, print_ast

ast, errors, symbol_table = parse_to_ast(code)
if not errors:
    print(print_ast(ast))
```

**3. 执行程序**

```python
from src import run_program

code = """
program factorial;
var n, fact: integer;
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

final_state, result = run_program(code)
```

### 命令行使用

```bash
# 运行演示
python3 demo_final.py

# 运行测试
python3 main.py --test

# 交互模式
python3 main.py -i
```

## 项目结构

```
src/
├── lexer.py              # 词法分析（420 行）
├── parser_ast.py         # 语法分析 + AST 生成（730 行）
├── ast_nodes.py          # AST 节点定义（330 行）
├── semantic_analyzer.py  # 语义分析（320 行）
├── symbol_table.py       # 符号表（184 行）
└── interpreter.py        # 解释器（320 行）

tests/
└── test_cases.py         # 测试套件（40+ 用例）

*.py
├── main.py               # 主程序入口
├── demo_final.py         # 完整功能演示
├── test_robustness.py    # 鲁棒性测试
└── test_improvements.py  # 改进功能测试

data/
├── correct_example*.txt  # 正确程序示例
├── error_example*.txt    # 错误程序示例
└── enhanced_example*.txt # 增强功能示例

docs/
├── GRAMMAR.md            # 完整文法定义
├── QUICK_START.md        # 使用指南
├── IMPROVEMENTS.md       # 技术实现详解
├── ROBUSTNESS.md         # 鲁棒性文档
└── PROJECT_STRUCTURE.md  # 项目结构说明
```

## 实现细节

### 词法分析

- 手工编写的状态机
- 支持单行注释 `//` 和块注释 `{}`
- 限制：标识符 255 字符，字符串 10000 字符，数字 100 位

### 语法分析

- LL(1) 文法，递归下降实现
- 错误恢复使用同步集
- 递归深度限制 100 层，嵌套深度限制 50 层

### 语义分析

- 静态类型检查
- 检测类型不匹配、未声明变量、重复声明
- 验证运算合法性（如不能对 boolean 做算术运算）
- 检查条件表达式类型（if/while 条件必须是 boolean）

### 解释器

- AST 遍历执行
- 循环次数限制 10000 次
- 输出行数限制 1000 行
- 错误检测：除零、溢出、NaN/Infinity

## 错误处理

**词法错误示例**

```
词法错误 [行2:列5]: 标识符过长（超过 255 字符）
```

**语法错误示例**

```
语法错误 [行3:列10]: 期望 ';'
  x := 10  y := 20;
           ^
```

**语义错误示例**

```
语义错误 [行5:列5]: 类型不匹配: 不能将 STRING 类型赋值给 INTEGER 类型的变量 'x'
  x := "hello"
       ^
```

**运行时错误示例**

```
运行时错误: 除零错误
  位置: 行7, 列15
```

## 限制和约束

| 项目       | 限制         | 说明       |
| ---------- | ------------ | ---------- |
| 源代码长度 | 1 MB         | 词法层检查 |
| 标识符长度 | 255 字符     | 词法层检查 |
| 字符串长度 | 10,000 字符  | 词法层检查 |
| 数字长度   | 100 位       | 词法层检查 |
| 整数范围   | -2³¹ ~ 2³¹-1 | 词法层检查 |
| 递归深度   | 100 层       | 语法层检查 |
| 嵌套深度   | 50 层        | 语法层检查 |
| 循环次数   | 10,000 次    | 运行时检查 |
| 输出行数   | 1,000 行     | 运行时检查 |

## 测试

**运行所有测试**

```bash
python3 main.py --test
```

**运行鲁棒性测试**

```bash
python3 test_robustness.py
```

**运行功能演示**

```bash
python3 demo_final.py
```

**测试覆盖**

- 词法分析：边界值、异常字符、长度限制
- 语法分析：各种语句组合、深层嵌套
- 语义分析：类型检查、变量声明
- 解释器：算术运算、控制流、I/O
- 鲁棒性：除零、溢出、无限循环

## 文法

完整的 EBNF 文法见 `docs/GRAMMAR.md`

核心规则：

```ebnf
<program> ::= "program" IDENTIFIER ";" [<var_decl>] <block> "."
<var_decl> ::= "var" <decl_list>
<decl_list> ::= IDENTIFIER {"," IDENTIFIER} ":" <type> ";"
<block> ::= "begin" <statement_list> "end"
<statement> ::= <assignment> | <if_stmt> | <while_stmt> | <write_stmt> | <read_stmt>
<expression> ::= <term> {("+" | "-") <term>}
<term> ::= <factor> {("*" | "/") <factor>}
<factor> ::= NUMBER | STRING | BOOLEAN | IDENTIFIER | "(" <expression> ")" | "-" <factor>
```

## API 参考

### parse_from_source(code: str) -> str

只进行语法检查，返回结果字符串。

### parse_to_ast(code: str, enable_semantic_check: bool = True) -> tuple

返回 (ast, errors, symbol_table)。

- ast: Program 对象或 None
- errors: 错误消息列表
- symbol_table: ScopedSymbolTable 对象

### run_program(code: str, debug: bool = False) -> tuple

解析并执行程序，返回 (final_state, result)。

- final_state: 变量最终值的字典
- result: 执行结果消息

### print_ast(ast: Program) -> str

将 AST 转换为树形字符串表示。

## 示例程序

**斐波那契数列**

```pascal
program fibonacci;
var n, a, b, temp, i: integer;
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
```

更多示例见 `data/` 目录。

## 已知问题

1. 解释器中所有数值统一为 float，INTEGER 类型在运行时不区分
2. 除法始终是浮点除法，无 div 运算符
3. 不支持函数和过程
4. 不支持数组和记录类型
5. read 语句在非交互环境下无法使用

## 扩展方向

- 函数和过程定义
- 数组和记录类型
- 模块系统
- 强类型运行时检查
- div 和 mod 运算符
- 中间代码生成
- 代码优化

## 开发

**代码格式化**

```bash
make format
```

**运行测试**

```bash
make test
```

**清理临时文件**

```bash
make clean
```

## 技术栈

- 语言：Python 3.7+
- 模式：访问者模式（AST 遍历）
- 文法：LL(1)
- 解析：递归下降
- 错误恢复：同步集

## 课程信息

- 课程：编译原理
- 项目：Mini 语言编译器
- 实现：完整的编译器前端 + 解释器

## 许可

教学项目，仅用于学习。
