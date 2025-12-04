# Mini 语言语法分析器

## 📚 项目简介

这是一个完整的 Mini 语言编译器前端实现，包括词法分析器和语法分析器。该项目是《编译原理》课程的实验项目，实现了对 Mini 语言源程序的语法正确性检查，并能精确报告错误位置和类型。

### ✨ 主要特性

- ✅ **完整的词法分析**：支持 Mini 语言的所有关键字、运算符和标识符
- ✅ **递归下降语法分析**：基于 LL(1) 文法实现
- ✅ **精确的错误报告**：详细的错误位置（行号、列号）和错误类型
- ✅ **错误恢复机制**：使用同步集进行错误恢复
- ✅ **完整的测试套件**：包含 30+ 个测试用例
- ✅ **多种使用方式**：命令行、交互式、文件输入

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
Parser/
├── README.md           # 项目说明文档
├── GRAMMAR.md          # 完整的 EBNF 文法定义
├── lexer.py            # 词法分析器
├── parser.py           # 语法分析器（递归下降）
├── main.py             # 主程序入口
├── test_cases.py       # 完整测试套件
├── examples/           # 示例程序（可选）
│   ├── correct/        # 正确的示例程序
│   └── errors/         # 错误的示例程序
└── docs/               # 额外文档（可选）
    └── design.md       # 设计文档
```

---

## 🚀 快速开始

### 环境要求

- Python 3.7+
- 无需额外依赖库

### 安装

```bash
# 克隆或下载项目到本地
cd Parser
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
python main.py --test

# 或直接运行测试文件
python test_cases.py
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
from parser import parse_from_source

source_code = """
program test;
begin
    x := 1
end.
"""

result = parse_from_source(source_code)
print(result)
```

#### 方式 2: 从 Token 文件分析

```python
from parser import parse_from_file

result = parse_from_file("tokens.txt")
print(result)
```

#### 方式 3: 传递 Token 列表

```python
from lexer import Lexer
from parser import Parser

lexer = Lexer(source_code)
tokens = lexer.tokenize()

parser = Parser(tokens)
parser.parse()
print(parser.get_result())
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

### 可能的扩展方向

1. **语义分析**

   - 符号表管理
   - 类型检查
   - 作用域分析

2. **中间代码生成**

   - 三地址码
   - 抽象语法树（AST）

3. **代码优化**

   - 常量折叠
   - 死代码消除

4. **目标代码生成**

   - 生成汇编代码
   - 生成虚拟机指令

5. **增强功能**
   - 添加函数和过程
   - 支持数组和记录
   - 支持更多数据类型

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

**最后更新**: 2024 年

**联系方式**: 如有问题，请查阅代码注释或相关文档。

---

## 附录

### A. 完整示例程序

见 `examples/` 目录

### B. 文法完整定义

见 `GRAMMAR.md`

### C. 测试用例详情

见 `test_cases.py`

---

**祝学习顺利！** 🎉
