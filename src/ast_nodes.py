"""
Mini 语言抽象语法树 (AST) 节点定义
定义了所有语法结构对应的 AST 节点类
"""

from typing import List, Optional, Any
from dataclasses import dataclass
from .lexer import Token


# ==================== 基类 ====================

@dataclass
class ASTNode:
    """AST 节点基类"""
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        """访问者模式接口"""
        method_name = f'visit_{self.__class__.__name__}'
        method = getattr(visitor, method_name, None)
        if method:
            return method(self)
        return visitor.generic_visit(self)


# ==================== 程序结构 ====================

@dataclass
class Program(ASTNode):
    """程序节点: program identifier; block."""
    name: str = ""
    var_declarations: Optional['VarDeclarations'] = None
    block: Optional['Block'] = None


@dataclass
class VarDeclarations(ASTNode):
    """变量声明节点: var identifier { , identifier } : type;"""
    declarations: List['VarDecl'] = None
    
    def __post_init__(self):
        if self.declarations is None:
            self.declarations = []


@dataclass
class VarDecl(ASTNode):
    """单个变量声明"""
    name: str = ""
    var_type: str = "integer"  # 'integer', 'real', 'boolean'


@dataclass
class Block(ASTNode):
    """语句块节点: begin statement_list end"""
    statements: List['Statement'] = None
    
    def __post_init__(self):
        if self.statements is None:
            self.statements = []


# ==================== 语句 ====================

@dataclass
class Statement(ASTNode):
    """语句基类"""
    pass


@dataclass
class Assignment(Statement):
    """赋值语句: identifier := expression"""
    variable: str = ""
    expression: 'Expression' = None


@dataclass
class IfStatement(Statement):
    """条件语句: if condition then statement [else statement]"""
    condition: 'Expression' = None
    then_statement: Statement = None
    else_statement: Optional[Statement] = None


@dataclass
class WhileStatement(Statement):
    """循环语句: while condition do statement"""
    condition: 'Expression' = None
    body: Statement = None


@dataclass
class EmptyStatement(Statement):
    """空语句"""
    pass


# ==================== 表达式 ====================

@dataclass
class Expression(ASTNode):
    """表达式基类"""
    pass


@dataclass
class BinaryOp(Expression):
    """二元运算: left op right"""
    left: Expression = None
    op: Token = None  # 运算符 token
    right: Expression = None


@dataclass
class UnaryOp(Expression):
    """一元运算: op operand"""
    op: Token = None  # 运算符 token
    operand: Expression = None


@dataclass
class Number(Expression):
    """数字字面量"""
    value: float = 0.0  # 统一使用 float 存储整数和浮点数


@dataclass
class String(Expression):
    """字符串字面量"""
    value: str = ""


@dataclass
class Boolean(Expression):
    """布尔字面量"""
    value: bool = False


@dataclass
class Variable(Expression):
    """变量引用"""
    name: str = ""


# ==================== AST 访问器基类 ====================

class ASTVisitor:
    """AST 访问者基类（访问者模式）"""
    
    def generic_visit(self, node: ASTNode):
        """默认访问方法"""
        raise NotImplementedError(f"No visit method for {type(node).__name__}")
    
    # 程序结构
    def visit_Program(self, node: Program):
        pass
    
    def visit_VarDeclarations(self, node: VarDeclarations):
        pass
    
    def visit_VarDecl(self, node: VarDecl):
        pass
    
    def visit_Block(self, node: Block):
        pass
    
    # 语句
    def visit_Assignment(self, node: Assignment):
        pass
    
    def visit_IfStatement(self, node: IfStatement):
        pass
    
    def visit_WhileStatement(self, node: WhileStatement):
        pass
    
    def visit_EmptyStatement(self, node: EmptyStatement):
        pass
    
    # 表达式
    def visit_BinaryOp(self, node: BinaryOp):
        pass
    
    def visit_UnaryOp(self, node: UnaryOp):
        pass
    
    def visit_Number(self, node: Number):
        pass
    
    def visit_String(self, node: String):
        pass
    
    def visit_Boolean(self, node: Boolean):
        pass
    
    def visit_Variable(self, node: Variable):
        pass


# ==================== AST 打印器 ====================

class ASTPrinter(ASTVisitor):
    """AST 树形打印器"""
    
    def __init__(self):
        self.indent_level = 0
    
    def indent(self):
        return "  " * self.indent_level
    
    def visit_Program(self, node: Program):
        result = f"Program('{node.name}')\n"
        self.indent_level += 1
        
        if node.var_declarations:
            result += self.indent() + "Variables:\n"
            self.indent_level += 1
            result += node.var_declarations.accept(self)
            self.indent_level -= 1
        
        result += self.indent() + "Body:\n"
        self.indent_level += 1
        result += node.block.accept(self)
        self.indent_level -= 1
        
        self.indent_level -= 1
        return result
    
    def visit_VarDeclarations(self, node: VarDeclarations):
        result = ""
        for decl in node.declarations:
            result += self.indent() + decl.accept(self) + "\n"
        return result
    
    def visit_VarDecl(self, node: VarDecl):
        return f"Var({node.name}: {node.var_type})"
    
    def visit_Block(self, node: Block):
        result = self.indent() + "Block:\n"
        self.indent_level += 1
        for stmt in node.statements:
            result += self.indent() + stmt.accept(self) + "\n"
        self.indent_level -= 1
        return result
    
    def visit_Assignment(self, node: Assignment):
        result = f"Assign({node.variable} :=\n"
        self.indent_level += 1
        result += self.indent() + node.expression.accept(self)
        self.indent_level -= 1
        result += ")"
        return result
    
    def visit_IfStatement(self, node: IfStatement):
        result = "If(\n"
        self.indent_level += 1
        result += self.indent() + "condition: " + node.condition.accept(self) + "\n"
        result += self.indent() + "then: " + node.then_statement.accept(self) + "\n"
        if node.else_statement:
            result += self.indent() + "else: " + node.else_statement.accept(self) + "\n"
        self.indent_level -= 1
        result += self.indent() + ")"
        return result
    
    def visit_WhileStatement(self, node: WhileStatement):
        result = "While(\n"
        self.indent_level += 1
        result += self.indent() + "condition: " + node.condition.accept(self) + "\n"
        result += self.indent() + "body: " + node.body.accept(self) + "\n"
        self.indent_level -= 1
        result += self.indent() + ")"
        return result
    
    def visit_EmptyStatement(self, node: EmptyStatement):
        return "EmptyStatement()"
    
    def visit_BinaryOp(self, node: BinaryOp):
        return f"({node.left.accept(self)} {node.op.value} {node.right.accept(self)})"
    
    def visit_UnaryOp(self, node: UnaryOp):
        return f"({node.op.value}{node.operand.accept(self)})"
    
    def visit_Number(self, node: Number):
        return f"{node.value}"
    
    def visit_String(self, node: String):
        return f'"{node.value}"'
    
    def visit_Boolean(self, node: Boolean):
        return f"{node.value}"
    
    def visit_Variable(self, node: Variable):
        return f"Var({node.name})"


# ==================== 工具函数 ====================

def print_ast(ast: ASTNode) -> str:
    """打印 AST 树形结构"""
    printer = ASTPrinter()
    return ast.accept(printer)
