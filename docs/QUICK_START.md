# Mini 语言解析器 - 快速开始

## 🚀 5 分钟上手

### 1. 基础语法检查

```python
from src import parse_from_source

code = """
program hello;
begin
    x := 10;
    y := 20;
    z := x + y
end.
"""

result = parse_from_source(code)
print(result)  # 输出："该程序符合语法要求。"
```

### 2. 生成并查看 AST

```python
from src import parse_to_ast, print_ast

code = """
program demo;
var
    x : integer;
begin
    x := 5 * 2
end.
"""

ast, errors, symbol_table = parse_to_ast(code)

if not errors:
    print(print_ast(ast))
    # 输出：
    # Program('demo')
    #   Variables:
    #     Var(x: integer)
    #   Body:
    #     Block:
    #       Assign(x :=
    #         (5.0 * 2.0))
```

### 3. 执行程序

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
print(f"阶乘结果: {final_state['fact']}")  # 输出：120
```

---

## 📝 Mini 语言语法参考

### 程序结构

```pascal
program 程序名;
var
    变量声明
begin
    语句列表
end.
```

### 变量声明

```pascal
var
    x, y : integer;    // 整数
    pi : real;         // 浮点数
    flag : boolean;    // 布尔值
    name : string;     // 字符串
```

### 语句类型

#### 赋值语句

```pascal
x := 10;
y := x + 5;
result := (a + b) * c;
```

#### 条件语句

```pascal
if x > 0 then
    y := 1;

if x > 0 then
    y := 1
else
    y := -1;
```

#### 循环语句

```pascal
while x > 0 do
    x := x - 1;

while condition do
begin
    语句1;
    语句2
end;
```

### 表达式

#### 算术运算

```pascal
x + y      // 加法
x - y      // 减法
x * y      // 乘法
x / y      // 除法
-x         // 负号
(x + y) * z  // 括号
```

#### 关系运算

```pascal
x < y      // 小于
x <= y     // 小于等于
x > y      // 大于
x >= y     // 大于等于
x = y      // 等于
x <> y     // 不等于
```

#### 逻辑运算

```pascal
(x > 0) and (y > 0)   // 与
(x > 0) or (y > 0)    // 或
not (x > 0)           // 非
```

#### 字面量

```pascal
123        // 整数
3.14       // 浮点数
true       // 布尔值
false
"hello"    // 字符串
```

---

## 🎯 完整示例

```pascal
program calculate_circle;
var
    pi : real;
    radius : real;
    area, circumference : real;
begin
    pi := 3.14159;
    radius := 5.0;

    // 计算面积
    area := pi * radius * radius;

    // 计算周长
    circumference := 2.0 * pi * radius;

    // 条件判断
    if area > 50.0 then
        radius := radius - 1.0
end.
```

执行结果:

```
area = 78.53975
circumference = 31.4159
radius = 4.0
```

---

## 🔧 高级用法

### 自定义 AST 访问者

```python
from src.ast_nodes import ASTVisitor

class MyVisitor(ASTVisitor):
    def visit_Assignment(self, node):
        print(f"发现赋值: {node.variable} := ...")

    def visit_BinaryOp(self, node):
        print(f"发现运算: {node.op.value}")
        node.left.accept(self)
        node.right.accept(self)

# 使用
ast, _, _ = parse_to_ast(code)
visitor = MyVisitor()
ast.accept(visitor)
```

### 调试模式

```python
from src import run_program

final_state, result = run_program(code, debug=True)
# 输出详细的执行过程
```

---

## ❌ 常见错误

### 未声明变量

```pascal
program error;
begin
    x := 10  // 错误：变量 'x' 未声明
end.
```

**解决方法**: 添加变量声明

```pascal
program correct;
var
    x : integer;
begin
    x := 10
end.
```

### 变量重复声明

```pascal
program error;
var
    x : integer;
    x : real;  // 错误：变量 'x' 重复声明
begin
    x := 10
end.
```

### 类型不匹配（运行时）

```pascal
x := 10 / 0;  // 运行时错误：除零
```

---

## 📚 更多资源

- [完整文法定义](GRAMMAR.md)
- [改进详情](IMPROVEMENTS.md)
- [项目结构](PROJECT_STRUCTURE.md)
- [示例程序](../data/)

---

**提示**: 运行 `python3 demo_ast.py` 查看完整功能演示！
