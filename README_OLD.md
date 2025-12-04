# Mini 语言语法分析器

## 📚 项目简介

这是一个完整的 Mini 语言编译器前端实现，包含词法分析器、语法分析器、AST 生成器、符号表管理和解释器。该项目是《编译原理》课程的实验项目，不仅能检查语法正确性，还能实际执行 Mini 语言程序并查看运行结果。

### � 主要功能

- **AST 生成**：构建完整的抽象语法树
- **符号表管理**：跟踪变量声明，检测未声明和重复声明
- **变量声明**：支持 `var` 关键字和类型系统（integer, real, boolean, string）
- **程序执行**：内置解释器，可直接运行 Mini 程序
- **增强词法**：支持整数、浮点数、字符串、布尔值
- **精确错误提示**：显示错误源代码行和精确指针
- **可扩展架构**：基于访问者模式，易于扩展

### ✨ 核心特性

- ✅ **完整的词法分析**：整数、浮点数、字符串、布尔值、运算符
- ✅ **递归下降语法分析**：基于 LL(1) 文法，生成 AST
- ✅ **符号表管理**：变量声明检查、类型记录、作用域支持
- ✅ **精确的错误报告**：源码行显示 + 错误指针 + 详细信息
- ✅ **错误恢复机制**：使用同步集进行错误恢复
- ✅ **程序执行**：内置解释器，可直接运行 Mini 程序
- ✅ **完整的测试套件**：包含 40+ 个测试用例
- ✅ **多种使用方式**：语法检查、AST 生成、程序执行

---

## 🔤 Mini 语言特性

### 支持的语法结构

1. **算术表达式**

   - 运算符: `+`, `-`, `*`, `/`
   - 支持括号和一元负号
   - 正确的运算符优先级

2. **逻辑表达式**

   - 逻辑运算符: `and`, `or`, `not`
   - 关系运算符: `<`, `<=`, `>`, `>=`, `=`, `<>`
   - 支持括号改变优先级

3. **赋值语句**

   ```pascal
   identifier := expression
   ```

4. **条件语句**

   ```pascal
   if condition then statement
   if condition then statement else statement
   ```

5. **循环语句**

   ```pascal
   while condition do statement
   while condition do begin statement_list end
   ```

6. **程序结构**
   ```pascal
   program identifier;
   begin
       statement_list
   end.
   ```

---

## 📁 项目结构

```
Mini-Language-Parser/
├── README.md              # 项目说明文档
├── Makefile               # 项目管理命令
├── setup.py               # 安装配置
├── main.py                # 主程序入口
├── demo_ast.py            # 功能演示程序
├── src/                   # 核心源代码
│   ├── lexer.py           # 词法分析器
│   ├── parser.py          # 语法分析器（兼容版）
│   ├── parser_ast.py      # AST 生成器
│   ├── ast_nodes.py       # AST 节点定义
│   ├── symbol_table.py    # 符号表管理
│   └── interpreter.py     # 解释器
├── tests/                 # 测试文件
│   └── test_cases.py      # 完整测试套件
├── data/                  # 示例程序
│   ├── correct_example*.txt
│   ├── error_example*.txt
│   └── enhanced_example*.txt
└── docs/                  # 文档
    ├── GRAMMAR.md         # 完整的 EBNF 文法定义
    ├── QUICK_START.md     # 快速入门指南
    ├── IMPROVEMENTS.md    # 技术改进说明
    └── PROJECT_STRUCTURE.md # 项目结构说明
```

---

## 🚀 快速开始

### 3 分钟快速体验

#### 1. 运行完整演示

```bash
python3 demo_ast.py
```

这将展示：AST 生成、符号表、解释器、错误处理等所有功能！

#### 2. 执行 Mini 程序

```python
from src import run_program

code = """
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
"""

final_state, result = run_program(code)
print(result)
# 输出：fact = 120
```

#### 3. 生成和查看 AST

```python
from src import parse_to_ast, print_ast

ast, errors, symbol_table = parse_to_ast(code)
if not errors:
    print(print_ast(ast))  # 打印 AST 树形结构
    print(symbol_table.get_global_scope().print_table())  # 打印符号表
```

📖 **详细教程**: 查看 [快速入门指南](docs/QUICK_START.md)

---

### 环境要求

- Python 3.7+
- 无需额外依赖库

### 安装

```bash
# 克隆或下载项目到本地
cd Mini-Language-Parser
```

### 使用方法

#### 1. 交互式菜单（推荐新手）

```bash
python main.py
```

然后根据菜单选择操作：

- 运行示例程序
- 运行完整测试
- 交互式输入
- 分析文件

#### 2. 分析源代码文件

```bash
python main.py example.txt
```

#### 3. 从 Token 文件分析

```bash
# 先生成 Token 文件
python lexer.py

# 然后分析 Token 文件
python main.py -t tokens.txt
```

#### 4. 交互式输入

```bash
python main.py -i
```

然后输入 Mini 语言代码，以 `END` 结束。

#### 5. 运行测试套件

```bash
python main.py --test
```

#### 6. 运行示例程序

```bash
python main.py --demo
```

---

## 📖 使用示例

### 示例 1: 正确的程序

**输入:**

```pascal
program example1;
begin
    x := 10;
    y := 20;
    if x < y then
        z := x + y
    else
        z := x - y
end.
```

**输出:**

```
该程序符合语法要求。
```

### 示例 2: 表达式错误

**输入:**

```pascal
program test;
begin
    i := 1 +
end.
```

**输出:**

```
语法错误 [行3:列18]: 表达式错误: 期望标识符、数字或表达式，但得到 'end'
```

### 示例 3: 缺少 then

**输入:**

```pascal
program test;
begin
    if x > 0
        y := 1
end.
```

**输出:**

```
语法错误 [行4:列9]: if 语句缺少 'then'
```

### 示例 4: 复杂嵌套

**输入:**

```pascal
program complex;
begin
    x := 10;
    while x > 0 do
    begin
        if x > 5 then
            y := x * 2
        else
        begin
            y := x + 1;
            z := y - 1
        end;
        x := x - 1
    end
end.
```

**输出:**

```
该程序符合语法要求。
```

---

## 🎯 语法分析实现细节

### 1. 文法设计

完整的 EBNF 文法请参见 [GRAMMAR.md](GRAMMAR.md)

**核心文法规则:**

```ebnf
<program> ::= "program" IDENTIFIER ";" <block> "."
<block> ::= "begin" <statement_list> "end"
<statement> ::= <assignment> | <if_stmt> | <while_stmt> | <block>
<expression> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= IDENTIFIER | NUMBER | "(" <expression> ")" | "-" <factor>
```

### 2. 递归下降分析

为每个非终结符实现一个解析函数：

- `program()` - 解析程序结构
- `block()` - 解析 begin-end 块
- `statement()` - 解析语句
- `expression()` - 解析算术表达式
- `condition()` - 解析条件表达式
- `term()`, `factor()` - 解析项和因子

### 3. 错误处理策略

#### 错误检测

- 在每个 `expect()` 调用处检测语法错误
- 记录详细的错误信息（类型、位置）

#### 错误恢复

使用**同步集（Synchronization Set）**进行错误恢复：

```python
def synchronize(self, sync_set: Set[TokenType]):
    """跳过 token 直到遇到同步集中的 token"""
    while not self.match(TokenType.EOF) and \
          self.current_token.type not in sync_set:
        self.advance()
```

**同步集设计：**

- 语句级别: `{SEMICOLON, END}`
- 表达式级别: `{SEMICOLON, RPAREN, THEN, DO}`
- 程序级别: `{BEGIN, END, DOT}`

### 4. 优先级处理

通过文法结构自然表达优先级：

```
优先级（从高到低）:
1. 括号 ()
2. 一元运算符 -, not
3. 乘除 *, /
4. 加减 +, -
5. 关系运算 <, <=, >, >=, =, <>
6. 逻辑与 and
7. 逻辑或 or
```

---

## 🧪 测试说明

### 测试用例分类

1. **正确程序** (10 个测试)

   - 简单赋值和算术运算
   - if-then / if-then-else
   - while-do / while-do-begin-end
   - 嵌套结构
   - 逻辑表达式

2. **表达式错误** (4 个测试)

   - 算术表达式不完整
   - 缺少运算数
   - 括号不匹配

3. **语句错误** (5 个测试)

   - 缺少赋值运算符
   - 缺少分号
   - if 缺少 then
   - while 缺少 do
   - 条件表达式错误

4. **结构错误** (6 个测试)

   - 缺少关键字（program, begin, end）
   - 缺少标点符号
   - begin-end 不匹配

5. **边界情况** (4 个测试)
   - 空程序
   - 单语句程序
   - 深层嵌套

### 运行测试

```bash
# 运行完整测试套件
python3 main.py --test

# 或使用 Make 命令
make test
```

**预期输出：**

```
测试总结: 29/29 通过
🎉 所有测试通过！
```

---

## 🔗 与词法分析器对接

### Token 文件格式

词法分析器生成的 Token 文件格式：

```
TOKEN_TYPE    VALUE    LINE    COLUMN
PROGRAM       program  1       1
IDENTIFIER    example  1       9
SEMICOLON     ;        1       16
...
EOF                    10      5
```

### 对接方式

#### 方式 1: 直接从源代码分析（推荐）

```python
from src import parse_from_source

source_code = """
program test;
begin
    x := 1
end.
"""

result = parse_from_source(source_code)
print(result)
```

#### 方式 2: AST 生成

```python
from src import parse_to_ast, print_ast

ast, errors, symbol_table = parse_to_ast(source_code)
if not errors:
    print(print_ast(ast))
```

#### 方式 3: 程序执行

```python
from src import run_program

final_state, result = run_program(source_code)
print(result)
print(f"变量值: {final_state}")
```

---

## 📊 技术实现总结

### 核心算法

| 模块     | 算法           | 时间复杂度 |
| -------- | -------------- | ---------- |
| 词法分析 | 有限状态自动机 | O(n)       |
| 语法分析 | 递归下降       | O(n)       |
| 错误恢复 | 同步集法       | O(n)       |

其中 n 为输入长度。

### 文法特性

- **文法类型**: LL(1)
- **左递归**: 已消除
- **左因子**: 已提取
- **二义性**: 无

### 错误处理能力

- ✅ 检测所有语法错误
- ✅ 精确报告错误位置（行号、列号）
- ✅ 提供有意义的错误信息
- ✅ 错误恢复（能继续检测后续错误）

---

## 🎓 学习要点

### 编译原理概念

本项目实践了以下编译原理概念：

1. **词法分析**

   - Token 识别
   - 关键字表
   - 有限状态自动机

2. **语法分析**

   - 上下文无关文法
   - 递归下降分析
   - LL(1) 分析
   - First/Follow 集合

3. **错误处理**

   - 错误检测
   - 错误报告
   - 错误恢复（同步集）

4. **编译器设计**
   - 模块化设计
   - 接口设计
   - 测试驱动开发

---

## 📝 实验报告要点

使用本项目完成实验报告时，建议包含以下内容：

### 1. 文法设计

- 完整的 EBNF 文法（见 GRAMMAR.md）
- 左递归消除过程
- 左因子提取说明
- First/Follow 集合计算

### 2. 程序设计

- 模块划分（词法分析、语法分析）
- 数据结构设计（Token, Parser）
- 核心函数流程图

### 3. 错误处理

- 错误类型分类
- 同步集设计
- 错误恢复示例

### 4. 测试结果

- 测试用例设计
- 测试结果截图
- 覆盖率分析

### 5. 总结与改进

- 实现难点
- 遇到的问题及解决
- 可能的改进方向

---

## 🔧 扩展与改进

### 已实现功能 ✅

1. **语义分析**

   - ✅ 符号表管理
   - ✅ 变量声明检查
   - ✅ 未声明变量检测
   - ✅ 重复声明检测

2. **AST 生成**

   - ✅ 14 种 AST 节点类型
   - ✅ 访问者模式架构
   - ✅ AST 打印和可视化

3. **程序执行**
   - ✅ 完整的解释器
   - ✅ 所有语句和表达式支持
   - ✅ 变量赋值和计算

### 未来扩展方向

1. **类型系统增强**

   - 强类型检查
   - 类型推导
   - 类型转换规则

2. **中间代码生成**

   - 三地址码
   - SSA 形式

3. **代码优化**

   - 常量折叠
   - 死代码消除
   - 循环优化

4. **目标代码生成**

   - 汇编代码
   - 字节码

5. **增强功能**
   - 函数和过程
   - 数组和记录
   - 模块系统

---

## 🐛 常见问题

### Q1: 为什么我的程序提示"表达式错误"？

**A:** 检查以下几点：

- 运算符后是否有操作数
- 括号是否匹配
- 是否使用了非法字符

### Q2: 如何处理多个错误？

**A:** 程序会尽可能检测多个错误，使用错误恢复机制继续分析。

### Q3: 支持注释吗？

**A:** 支持，词法分析器支持：

- 单行注释: `// ...`
- 块注释: `{ ... }`

### Q4: Token 文件格式是什么？

**A:** 每行一个 Token，格式为：`TOKEN_TYPE\tVALUE\tLINE\tCOLUMN`

---

## 👥 作者信息

**课程**: 编译原理
**项目**: Mini 语言语法分析器
**实现**: 完整的词法分析器 + 递归下降语法分析器

---

## 📄 许可证

本项目仅用于教学和学习目的。

---

## 🙏 致谢

感谢编译原理课程提供的理论基础和实验指导。

---

**项目维护**: 持续更新

**联系方式**: 如有问题，请查阅代码注释或相关文档。

---

## 附录

### A. 完整示例程序

见 `data/` 目录

### B. 文法完整定义

见 `docs/GRAMMAR.md`

### C. 测试用例详情

见 `tests/test_cases.py`

### D. 技术文档

- `docs/QUICK_START.md` - 快速入门指南
- `docs/IMPROVEMENTS.md` - 技术改进说明
- `docs/PROJECT_STRUCTURE.md` - 项目结构说明

---

**祝学习顺利！** 🎉
