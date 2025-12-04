# Mini 语言完整文法定义 (EBNF)

## 📋 文法说明

本文法为 Mini 语言的完整语法规范，已消除左递归，提取左因子，适用于 LL(1) 递归下降分析。

---

## 🔤 词法单元（Token）定义

```
关键字：program, begin, end, if, then, else, while, do, and, or, not
标识符：IDENTIFIER  (以字母开头，后跟字母或数字)
数字：   NUMBER      (整数)
运算符： + - * / := ( )
关系运算符：< <= > >= = <>
逻辑运算符：and, or, not
分隔符： ; , .
```

---

## 📐 完整 EBNF 文法

### 1. 程序结构

```ebnf
<program> ::= "program" IDENTIFIER ";" <block> "."

<block> ::= "begin" <statement_list> "end"

<statement_list> ::= <statement> { ";" <statement> }
```

**说明：**

- 程序必须以 `program` 开头，以 `.` 结尾
- `block` 用 `begin...end` 包裹
- 语句列表由分号分隔（最后一条语句后的分号可选）

---

### 2. 语句

```ebnf
<statement> ::= <assignment_stmt>
              | <if_stmt>
              | <while_stmt>
              | <block>
              | ε

<assignment_stmt> ::= IDENTIFIER ":=" <expression>

<if_stmt> ::= "if" <condition> "then" <statement> [ "else" <statement> ]

<while_stmt> ::= "while" <condition> "do" <statement>
```

**说明：**

- 支持四种语句类型：赋值、if、while、语句块
- if-else 的 else 部分是可选的
- 允许空语句（处理多余分号）

---

### 3. 表达式（算术表达式）

```ebnf
<expression> ::= <term> { ("+" | "-") <term> }

<term> ::= <factor> { ("*" | "/") <factor> }

<factor> ::= IDENTIFIER
           | NUMBER
           | "(" <expression> ")"
           | "-" <factor>
```

**说明：**

- 已消除左递归，改用右递归+迭代形式
- 优先级：`factor > term > expression`
- 即：`() > 一元负号 > */ > +-`

---

### 4. 条件表达式（逻辑表达式）

```ebnf
<condition> ::= <or_term> { "or" <or_term> }

<or_term> ::= <and_term> { "and" <and_term> }

<and_term> ::= <not_term>

<not_term> ::= [ "not" ] <comparison>

<comparison> ::= <expression> <relop> <expression>
               | "(" <condition> ")"

<relop> ::= "<" | "<=" | ">" | ">=" | "=" | "<>"
```

**说明：**

- 逻辑运算符优先级：`not > and > or`
- 支持括号改变优先级
- 关系运算符连接两个算术表达式

---

## 🎯 优先级总结

从高到低：

1. **括号** `( )`
2. **一元负号** `-`（算术）/ **not**（逻辑）
3. **乘除** `*` `/`
4. **加减** `+` `-`
5. **关系运算** `< <= > >= = <>`
6. **逻辑与** `and`
7. **逻辑或** `or`

---

## 🔄 左递归消除说明

### 原文法（含左递归）：

```
<expression> ::= <expression> "+" <term> | <term>
```

### 消除后：

```
<expression> ::= <term> { ("+" | "-") <term> }
```

通过将左递归改为**迭代**形式（使用 `{ }` 表示零次或多次），保持了相同的语义，且适用于自顶向下分析。

---

## 📊 First 和 Follow 集（部分）

### First 集合

- First(program) = {program}
- First(statement) = {IDENTIFIER, if, while, begin, ε}
- First(expression) = {IDENTIFIER, NUMBER, (, -}
- First(condition) = {IDENTIFIER, NUMBER, (, -, not}

### Follow 集合

- Follow(statement) = {;, end, else}
- Follow(expression) = {;, ), end, <, <=, >, >=, =, <>, then, do}
- Follow(condition) = {then, do, )}

---

## ✅ LL(1) 验证

本文法满足 LL(1) 条件：

1. **无左递归**：已全部消除
2. **左因子已提取**：如 if-then / if-then-else 通过可选项处理
3. **First 和 Follow 集不相交**：在每个产生式选择点，各候选式的 First 集互不相交

---

## 📝 示例程序

```pascal
program example1;
begin
    x := 10;
    y := 20;
    if x < y then
        z := x + y
    else
        z := x - y;
    while z > 0 do
    begin
        z := z - 1
    end
end.
```

---

## 🔍 语法分析思路

1. **递归下降分析**：为每个非终结符编写一个解析函数
2. **前看一个 token**：根据当前 token 选择产生式
3. **错误恢复**：使用同步集（Follow 集）跳过错误 token
4. **错误报告**：记录错误类型和位置信息

---

## 结束

本文法已准备好用于实现递归下降语法分析器。
