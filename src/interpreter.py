"""
Mini 语言解释器
遍历 AST 并执行程序
"""

from typing import Any, Dict
from .ast_nodes import *
from .symbol_table import SymbolType


class RuntimeError(Exception):
    """运行时错误"""
    def __init__(self, message: str, node: ASTNode = None):
        self.message = message
        self.node = node
        super().__init__(message)


class Interpreter(ASTVisitor):
    """AST 解释器"""
    
    def __init__(self, debug: bool = False):
        self.global_scope: Dict[str, Any] = {}  # 全局变量存储
        self.debug = debug
        self.output_buffer = []  # 输出缓冲区
    
    def log(self, message: str):
        """调试日志"""
        if self.debug:
            print(f"[DEBUG] {message}")
    
    def interpret(self, ast: Program) -> Dict[str, Any]:
        """解释执行程序"""
        try:
            ast.accept(self)
            return self.global_scope
        except RuntimeError as e:
            print(f"运行时错误: {e.message}")
            if e.node:
                print(f"  位置: 行{e.node.line}, 列{e.node.column}")
            return self.global_scope
    
    # ==================== 程序结构 ====================
    
    def visit_Program(self, node: Program):
        """执行程序"""
        self.log(f"执行程序: {node.name}")
        
        # 初始化变量（如果有声明）
        if node.var_declarations:
            node.var_declarations.accept(self)
        
        # 执行程序体
        if node.block:
            node.block.accept(self)
        
        self.log(f"程序 {node.name} 执行完成")
    
    def visit_VarDeclarations(self, node: VarDeclarations):
        """处理变量声明"""
        for decl in node.declarations:
            decl.accept(self)
    
    def visit_VarDecl(self, node: VarDecl):
        """初始化变量（使用默认值）"""
        default_values = {
            'integer': 0,
            'real': 0.0,
            'boolean': False,
            'string': ''
        }
        default_value = default_values.get(node.var_type, 0)
        self.global_scope[node.name] = default_value
        self.log(f"声明变量: {node.name} = {default_value} ({node.var_type})")
    
    def visit_Block(self, node: Block):
        """执行语句块"""
        for stmt in node.statements:
            stmt.accept(self)
    
    # ==================== 语句 ====================
    
    def visit_Assignment(self, node: Assignment):
        """执行赋值语句"""
        value = node.expression.accept(self)
        self.global_scope[node.variable] = value
        self.log(f"赋值: {node.variable} = {value}")
    
    def visit_IfStatement(self, node: IfStatement):
        """执行 if 语句"""
        condition_value = node.condition.accept(self)
        
        if not isinstance(condition_value, bool):
            # 尝试转换为布尔值
            condition_value = bool(condition_value)
        
        self.log(f"if 条件: {condition_value}")
        
        if condition_value:
            node.then_statement.accept(self)
        elif node.else_statement:
            node.else_statement.accept(self)
    
    def visit_WhileStatement(self, node: WhileStatement):
        """执行 while 循环"""
        iteration = 0
        max_iterations = 10000  # 防止无限循环
        
        while True:
            condition_value = node.condition.accept(self)
            
            if not isinstance(condition_value, bool):
                condition_value = bool(condition_value)
            
            if not condition_value:
                break
            
            iteration += 1
            if iteration > max_iterations:
                raise RuntimeError(f"循环超过最大迭代次数 ({max_iterations})", node)
            
            node.body.accept(self)
        
        self.log(f"while 循环执行了 {iteration} 次")
    
    def visit_EmptyStatement(self, node: EmptyStatement):
        """空语句，什么都不做"""
        pass
    
    # ==================== 表达式 ====================
    
    def visit_BinaryOp(self, node: BinaryOp):
        """计算二元运算"""
        left_val = node.left.accept(self)
        right_val = node.right.accept(self)
        op = node.op.value
        
        # 算术运算
        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise RuntimeError("除零错误", node)
            return left_val / right_val
        
        # 关系运算
        elif op == '<':
            return left_val < right_val
        elif op == '<=':
            return left_val <= right_val
        elif op == '>':
            return left_val > right_val
        elif op == '>=':
            return left_val >= right_val
        elif op == '=':
            return left_val == right_val
        elif op == '<>':
            return left_val != right_val
        
        # 逻辑运算
        elif op == 'and':
            return bool(left_val) and bool(right_val)
        elif op == 'or':
            return bool(left_val) or bool(right_val)
        
        else:
            raise RuntimeError(f"未知运算符: {op}", node)
    
    def visit_UnaryOp(self, node: UnaryOp):
        """计算一元运算"""
        operand_val = node.operand.accept(self)
        op = node.op.value
        
        if op == '-':
            return -operand_val
        elif op == 'not':
            return not bool(operand_val)
        else:
            raise RuntimeError(f"未知一元运算符: {op}", node)
    
    def visit_Number(self, node: Number):
        """返回数字值"""
        return node.value
    
    def visit_String(self, node: String):
        """返回字符串值"""
        return node.value
    
    def visit_Boolean(self, node: Boolean):
        """返回布尔值"""
        return node.value
    
    def visit_Variable(self, node: Variable):
        """获取变量值"""
        if node.name not in self.global_scope:
            raise RuntimeError(f"变量 '{node.name}' 未定义", node)
        value = self.global_scope[node.name]
        self.log(f"读取变量: {node.name} = {value}")
        return value


# ==================== 便捷函数 ====================

def run_program(source_code: str, debug: bool = False) -> tuple[Dict[str, Any], str]:
    """解析并执行程序"""
    from .parser_ast import parse_to_ast
    
    ast, errors, symbol_table = parse_to_ast(source_code)
    
    if errors:
        return {}, "\n".join(errors)
    
    if not ast:
        return {}, "解析失败"
    
    interpreter = Interpreter(debug=debug)
    final_state = interpreter.interpret(ast)
    
    result = "程序执行成功！\n\n"
    result += "=== 最终变量值 ===\n"
    for var_name, value in sorted(final_state.items()):
        result += f"  {var_name} = {value}\n"
    
    return final_state, result
