"""
语义分析器 (Semantic Analyzer)
在语法分析之后、解释执行之前进行类型检查和语义验证
"""

from typing import List, Optional
from .ast_nodes import *
from .symbol_table import SymbolType, ScopedSymbolTable, binary_op_result_type, can_convert
from .lexer import TokenType


class SemanticError(Exception):
    """语义错误异常"""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
    
    def __str__(self):
        if self.line > 0:
            return f"语义错误 [行{self.line}:列{self.column}]: {self.message}"
        return f"语义错误: {self.message}"


class SemanticAnalyzer(ASTVisitor):
    """
    语义分析器
    检查类型兼容性、运算合法性、条件表达式类型等
    """
    
    def __init__(self, symbol_table: ScopedSymbolTable):
        self.symbol_table = symbol_table
        self.errors: List[str] = []
        self.current_expr_type: Optional[SymbolType] = None
    
    def add_error(self, message: str, node: ASTNode = None):
        """添加语义错误"""
        if node and hasattr(node, 'line') and node.line > 0:
            error_msg = f"语义错误 [行{node.line}:列{node.column}]: {message}"
        else:
            error_msg = f"语义错误: {message}"
        self.errors.append(error_msg)
    
    def analyze(self, program: Program) -> List[str]:
        """执行语义分析，返回错误列表"""
        self.errors = []
        if program:
            program.accept(self)
        return self.errors
    
    # ==================== 访问器方法 ====================
    
    def visit_Program(self, node: Program):
        """分析程序节点"""
        if node.var_declarations:
            node.var_declarations.accept(self)
        if node.block:
            node.block.accept(self)
    
    def visit_VarDeclarations(self, node: VarDeclarations):
        """分析变量声明"""
        for decl in node.declarations:
            decl.accept(self)
    
    def visit_VarDecl(self, node: VarDecl):
        """分析单个变量声明"""
        # 变量声明本身已经在 parser 中检查过了
        pass
    
    def visit_Block(self, node: Block):
        """分析语句块"""
        for stmt in node.statements:
            stmt.accept(self)
    
    def visit_Assignment(self, node: Assignment):
        """
        分析赋值语句
        检查：左侧变量类型 与 右侧表达式类型 是否兼容
        """
        # 获取变量声明的类型
        symbol = self.symbol_table.lookup(node.variable)
        if not symbol:
            self.add_error(f"变量 '{node.variable}' 未声明", node)
            return
        
        var_type = symbol.symbol_type
        
        # 计算右侧表达式的类型
        expr_type = self.get_expression_type(node.expression)
        
        if expr_type is None:
            self.add_error(f"无法确定表达式类型", node)
            return
        
        # 检查类型兼容性
        if not can_convert(expr_type, var_type):
            self.add_error(
                f"类型不匹配: 不能将 {expr_type.name} 类型赋值给 {var_type.name} 类型的变量 '{node.variable}'",
                node
            )
        
        # 标记变量已初始化
        symbol.initialized = True
    
    def visit_IfStatement(self, node: IfStatement):
        """
        分析 if 语句
        检查：条件表达式必须是 boolean 类型
        """
        condition_type = self.get_expression_type(node.condition)
        
        if condition_type != SymbolType.BOOLEAN:
            self.add_error(
                f"if 语句的条件必须是 boolean 类型，但得到 {condition_type.name if condition_type else 'unknown'}",
                node
            )
        
        # 检查分支语句
        if node.then_statement:
            node.then_statement.accept(self)
        if node.else_statement:
            node.else_statement.accept(self)
    
    def visit_WhileStatement(self, node: WhileStatement):
        """
        分析 while 语句
        检查：条件表达式必须是 boolean 类型
        """
        condition_type = self.get_expression_type(node.condition)
        
        if condition_type != SymbolType.BOOLEAN:
            self.add_error(
                f"while 语句的条件必须是 boolean 类型，但得到 {condition_type.name if condition_type else 'unknown'}",
                node
            )
        
        # 检查循环体
        if node.body:
            node.body.accept(self)
    
    def visit_EmptyStatement(self, node: EmptyStatement):
        """空语句无需检查"""
        pass
    
    def visit_WriteStatement(self, node: WriteStatement):
        """
        分析 write 语句
        表达式可以是任何类型
        """
        # 只需检查表达式本身是否合法
        self.get_expression_type(node.expression)
    
    def visit_ReadStatement(self, node: ReadStatement):
        """
        分析 read 语句
        检查变量是否已声明
        """
        symbol = self.symbol_table.lookup(node.variable)
        if not symbol:
            self.add_error(f"read 语句中的变量 '{node.variable}' 未声明", node)
    
    # ==================== 表达式类型推导 ====================
    
    def get_expression_type(self, expr: Expression) -> Optional[SymbolType]:
        """获取表达式的类型"""
        if isinstance(expr, Number):
            # 根据值判断是整数还是实数
            if isinstance(expr.value, int) or expr.value == int(expr.value):
                return SymbolType.INTEGER
            return SymbolType.REAL
        
        elif isinstance(expr, String):
            return SymbolType.STRING
        
        elif isinstance(expr, Boolean):
            return SymbolType.BOOLEAN
        
        elif isinstance(expr, Variable):
            symbol = self.symbol_table.lookup(expr.name)
            if symbol:
                # 可选：警告使用未初始化的变量（不作为错误，因为有默认值）
                # if not symbol.initialized:
                #     self.add_error(f"警告: 变量 '{expr.name}' 可能未初始化", expr)
                return symbol.symbol_type
            else:
                self.add_error(f"变量 '{expr.name}' 未声明", expr)
                return None
        
        elif isinstance(expr, BinaryOp):
            return self.get_binary_op_type(expr)
        
        elif isinstance(expr, UnaryOp):
            return self.get_unary_op_type(expr)
        
        return None
    
    def get_binary_op_type(self, node: BinaryOp) -> Optional[SymbolType]:
        """
        获取二元运算的结果类型
        同时检查操作数类型是否合法
        """
        left_type = self.get_expression_type(node.left)
        right_type = self.get_expression_type(node.right)
        
        if left_type is None or right_type is None:
            return None
        
        op = node.op.type
        
        # 算术运算符: +, -, *, /
        if op in [TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE]:
            # 必须是数值类型
            if left_type not in [SymbolType.INTEGER, SymbolType.REAL]:
                self.add_error(
                    f"算术运算 '{node.op.value}' 的左操作数必须是数值类型，但得到 {left_type.name}",
                    node
                )
                return None
            
            if right_type not in [SymbolType.INTEGER, SymbolType.REAL]:
                self.add_error(
                    f"算术运算 '{node.op.value}' 的右操作数必须是数值类型，但得到 {right_type.name}",
                    node
                )
                return None
            
            # 检查除零（仅对常量）
            if op == TokenType.DIVIDE and isinstance(node.right, Number):
                if node.right.value == 0 or node.right.value == 0.0:
                    self.add_error(
                        f"除零错误: 不能除以常量 0",
                        node
                    )
            
            # 使用辅助函数计算结果类型
            # 注意：binary_op_result_type 需要运算符字符串，而不是 TokenType 名称
            op_str = node.op.value  # 使用 token 的实际值（如 '+'）
            result_type = binary_op_result_type(left_type, op_str, right_type)
            # 如果辅助函数返回 None，使用默认规则
            if result_type is None:
                # 如果有 REAL 参与，结果为 REAL，否则为 INTEGER
                if left_type == SymbolType.REAL or right_type == SymbolType.REAL:
                    return SymbolType.REAL
                return SymbolType.INTEGER
            return result_type
        
        # 关系运算符: <, <=, >, >=, =, <>
        elif op in [TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE, 
                    TokenType.EQ, TokenType.NE]:
            # 两边必须是可比较的类型（数值类型）
            if left_type not in [SymbolType.INTEGER, SymbolType.REAL]:
                self.add_error(
                    f"关系运算 '{node.op.value}' 的左操作数必须是数值类型，但得到 {left_type.name}",
                    node
                )
                return None
            
            if right_type not in [SymbolType.INTEGER, SymbolType.REAL]:
                self.add_error(
                    f"关系运算 '{node.op.value}' 的右操作数必须是数值类型，但得到 {right_type.name}",
                    node
                )
                return None
            
            # 关系运算结果总是 boolean
            return SymbolType.BOOLEAN
        
        # 逻辑运算符: and, or
        elif op in [TokenType.AND, TokenType.OR]:
            # 两边必须是 boolean
            if left_type != SymbolType.BOOLEAN:
                self.add_error(
                    f"逻辑运算 '{node.op.value}' 的左操作数必须是 boolean 类型，但得到 {left_type.name}",
                    node
                )
                return None
            
            if right_type != SymbolType.BOOLEAN:
                self.add_error(
                    f"逻辑运算 '{node.op.value}' 的右操作数必须是 boolean 类型，但得到 {right_type.name}",
                    node
                )
                return None
            
            return SymbolType.BOOLEAN
        
        return None
    
    def get_unary_op_type(self, node: UnaryOp) -> Optional[SymbolType]:
        """
        获取一元运算的结果类型
        """
        operand_type = self.get_expression_type(node.operand)
        
        if operand_type is None:
            return None
        
        op = node.op.type
        
        # 负号: -
        if op == TokenType.MINUS:
            if operand_type not in [SymbolType.INTEGER, SymbolType.REAL]:
                self.add_error(
                    f"一元负号的操作数必须是数值类型，但得到 {operand_type.name}",
                    node
                )
                return None
            return operand_type
        
        # 逻辑非: not
        elif op == TokenType.NOT:
            if operand_type != SymbolType.BOOLEAN:
                self.add_error(
                    f"逻辑非的操作数必须是 boolean 类型，但得到 {operand_type.name}",
                    node
                )
                return None
            return SymbolType.BOOLEAN
        
        return None


def analyze_semantics(program: Program, symbol_table: ScopedSymbolTable) -> List[str]:
    """
    便捷函数：对程序进行语义分析
    返回错误列表（空列表表示无错误）
    """
    analyzer = SemanticAnalyzer(symbol_table)
    return analyzer.analyze(program)
