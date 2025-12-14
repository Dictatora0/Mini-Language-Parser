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
    
    # 限制常量
    MAX_LOOP_ITERATIONS = 10000
    MAX_RECURSION_DEPTH = 100
    MAX_OUTPUT_LINES = 1000
    
    def __init__(self, symbol_table: 'ScopedSymbolTable' = None, debug: bool = False):
        self.global_scope: Dict[str, Any] = {}  # 全局变量存储
        self.debug = debug
        self.symbol_table = symbol_table
        self.output_buffer = []  # 输出缓冲区
        
        # 运行时跟踪
        self.loop_iteration_count = 0
        self.recursion_depth = 0
        self.output_line_count = 0
    
    def log(self, message: str):
        """调试日志输出"""
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
        self.log("开始执行 while 循环")
        
        local_iteration = 0
        
        while True:
            # 检查条件
            try:
                condition_value = node.condition.accept(self)
            except Exception as e:
                raise RuntimeError(f"循环条件计算错误: {str(e)}", node)
            
            if not isinstance(condition_value, bool):
                condition_value = bool(condition_value)
            
            if not condition_value:
                break
            
            local_iteration += 1
            self.loop_iteration_count += 1
            
            # 边界检查：防止无限循环
            if self.loop_iteration_count > self.MAX_LOOP_ITERATIONS:
                raise RuntimeError(
                    f"程序执行超过最大循环次数限制 ({self.MAX_LOOP_ITERATIONS})，可能存在无限循环", 
                    node
                )
            
            # 边界检查：防止单个循环过多迭代
            if local_iteration > 1000:
                self.log(f"警告：单个 while 循环已执行 {local_iteration} 次")
            
            try:
                node.body.accept(self)
            except RuntimeError:
                raise  # 重新抛出运行时错误
            except Exception as e:
                raise RuntimeError(f"循环体执行错误: {str(e)}", node)
        
        self.log(f"while 循环执行了 {local_iteration} 次")
    
    def visit_EmptyStatement(self, node: EmptyStatement):
        """空语句，什么都不做"""
        pass
    
    def visit_WriteStatement(self, node: WriteStatement):
        """执行输出语句"""
        # 边界检查：输出行数限制
        self.output_line_count += 1
        if self.output_line_count > self.MAX_OUTPUT_LINES:
            raise RuntimeError(
                f"输出行数超过限制 ({self.MAX_OUTPUT_LINES})，可能存在无限循环", 
                node
            )
        
        try:
            value = node.expression.accept(self)
            # 边界检查：输出值的合理性
            if isinstance(value, float):
                if value == float('inf'):
                    print("Infinity")
                elif value == float('-inf'):
                    print("-Infinity")
                elif value != value:  # NaN check
                    print("NaN")
                else:
                    print(value)
            else:
                print(value)
            self.log(f"输出: {value}")
        except Exception as e:
            raise RuntimeError(f"输出表达式计算错误: {str(e)}", node)
    
    def visit_ReadStatement(self, node: ReadStatement):
        """执行输入语句"""
        try:
            # 获取变量的类型
            var_name = node.variable
            symbol = self.symbol_table.lookup(var_name) if self.symbol_table else None
            
            # 提示用户输入
            user_input = input(f"请输入 {var_name} 的值: ").strip()
            
            # 根据变量类型转换输入
            if symbol:
                if symbol.symbol_type == SymbolType.INTEGER:
                    try:
                        value = int(float(user_input))  # 先转浮点再转整数，支持 "10.0" 输入
                    except ValueError:
                        raise RuntimeError(f"输入格式错误: 期望整数，但得到 '{user_input}'", node)
                elif symbol.symbol_type == SymbolType.REAL:
                    try:
                        value = float(user_input)
                    except ValueError:
                        raise RuntimeError(f"输入格式错误: 期望实数，但得到 '{user_input}'", node)
                elif symbol.symbol_type == SymbolType.BOOLEAN:
                    value = user_input.lower() in ['true', '1', 'yes', 't', 'y']
                elif symbol.symbol_type == SymbolType.STRING:
                    value = str(user_input)
                else:
                    value = float(user_input)  # 默认为数值
            else:
                # 如果没有类型信息，尝试智能转换
                try:
                    value = int(float(user_input))
                except:
                    try:
                        value = float(user_input)
                    except:
                        value = user_input
            
            # 将值存入全局作用域
            self.global_scope[var_name] = value
            self.log(f"读取输入: {var_name} = {value}")
            
        except ValueError as e:
            raise RuntimeError(f"输入格式错误: {e}", node)
        except EOFError:
            raise RuntimeError("输入中断", node)
    
    # ==================== 表达式 ====================
    
    def visit_BinaryOp(self, node: BinaryOp):
        """计算二元运算"""
        try:
            left_val = node.left.accept(self)
            right_val = node.right.accept(self)
        except Exception as e:
            raise RuntimeError(f"运算数计算错误: {str(e)}", node)
        
        op = node.op.value
        
        # 边界检查：确保操作数是数值类型（对于算术运算）
        if op in ['+', '-', '*', '/']:
            if not isinstance(left_val, (int, float)):
                raise RuntimeError(f"算术运算的左操作数必须是数值类型，但得到 {type(left_val).__name__}", node)
            if not isinstance(right_val, (int, float)):
                raise RuntimeError(f"算术运算的右操作数必须是数值类型，但得到 {type(right_val).__name__}", node)
        
        # 算术运算
        if op == '+':
            result = left_val + right_val
            # 边界检查：溢出
            if isinstance(result, float) and (result == float('inf') or result == float('-inf')):
                raise RuntimeError("算术运算溢出", node)
            return result
            
        elif op == '-':
            result = left_val - right_val
            if isinstance(result, float) and (result == float('inf') or result == float('-inf')):
                raise RuntimeError("算术运算溢出", node)
            return result
            
        elif op == '*':
            result = left_val * right_val
            if isinstance(result, float) and (result == float('inf') or result == float('-inf')):
                raise RuntimeError("算术运算溢出", node)
            return result
            
        elif op == '/':
            # 边界检查：除零
            if right_val == 0 or right_val == 0.0:
                raise RuntimeError("除零错误", node)
            result = left_val / right_val
            # 边界检查：结果是否有效
            if result != result:  # NaN check
                raise RuntimeError("除法产生无效结果 (NaN)", node)
            if result == float('inf') or result == float('-inf'):
                raise RuntimeError("除法结果溢出", node)
            return result
        
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
        error_msg = "\n".join(errors)
        return {}, error_msg
    
    if not ast:
        return {}, "解析失败"
    
    # 执行程序（传递符号表）
    interpreter = Interpreter(symbol_table=symbol_table, debug=debug)
    try:
        final_state = interpreter.interpret(ast)
        
        result = "程序执行成功！\n\n=== 最终变量值 ===\n"
        for var_name in sorted(final_state.keys()):
            result += f"  {var_name} = {final_state[var_name]}\n"
        
        return final_state, result
    
    except Exception as e:
        return interpreter.global_scope, f"运行时错误: {str(e)}"
