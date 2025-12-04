"""
符号表管理模块
用于记录和查询变量、类型等符号信息
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum, auto


class SymbolType(Enum):
    """符号类型"""
    INTEGER = auto()
    REAL = auto()
    BOOLEAN = auto()
    STRING = auto()


@dataclass
class Symbol:
    """符号表项"""
    name: str
    symbol_type: SymbolType
    line: int = 0
    column: int = 0
    initialized: bool = False  # 是否已初始化
    
    def __repr__(self):
        return f"Symbol({self.name}: {self.symbol_type.name})"


class SymbolTable:
    """符号表"""
    
    def __init__(self, parent: Optional['SymbolTable'] = None):
        self.symbols: Dict[str, Symbol] = {}
        self.parent = parent  # 支持作用域嵌套
    
    def define(self, symbol: Symbol) -> bool:
        """定义一个符号，如果已存在则返回 False"""
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True
    
    def lookup(self, name: str, current_scope_only: bool = False) -> Optional[Symbol]:
        """查找符号，支持向上查找父作用域"""
        symbol = self.symbols.get(name)
        if symbol:
            return symbol
        
        # 如果只查当前作用域，或没有父作用域，返回 None
        if current_scope_only or not self.parent:
            return None
        
        # 向上查找
        return self.parent.lookup(name)
    
    def exists(self, name: str) -> bool:
        """检查符号是否存在"""
        return self.lookup(name) is not None
    
    def update(self, name: str, **kwargs) -> bool:
        """更新符号属性"""
        symbol = self.lookup(name)
        if not symbol:
            return False
        
        for key, value in kwargs.items():
            if hasattr(symbol, key):
                setattr(symbol, key, value)
        return True
    
    def __repr__(self):
        return f"SymbolTable({list(self.symbols.keys())})"
    
    def print_table(self, indent: int = 0) -> str:
        """打印符号表内容"""
        result = "  " * indent + "SymbolTable:\n"
        for name, symbol in self.symbols.items():
            result += "  " * (indent + 1) + f"{name}: {symbol.symbol_type.name}\n"
        if self.parent:
            result += "  " * indent + "Parent:\n"
            result += self.parent.print_table(indent + 1)
        return result


class ScopedSymbolTable:
    """支持作用域的符号表管理器"""
    
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.scope_stack: List[SymbolTable] = [self.global_scope]
    
    def enter_scope(self):
        """进入新的作用域"""
        new_scope = SymbolTable(parent=self.current_scope)
        self.scope_stack.append(new_scope)
        self.current_scope = new_scope
    
    def exit_scope(self):
        """退出当前作用域"""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]
    
    def define(self, symbol: Symbol) -> bool:
        """在当前作用域定义符号"""
        return self.current_scope.define(symbol)
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """查找符号（会向上查找）"""
        return self.current_scope.lookup(name)
    
    def exists(self, name: str) -> bool:
        """检查符号是否存在"""
        return self.current_scope.exists(name)
    
    def get_global_scope(self) -> SymbolTable:
        """获取全局作用域"""
        return self.global_scope
    
    def get_current_scope(self) -> SymbolTable:
        """获取当前作用域"""
        return self.current_scope


# ==================== 类型检查辅助函数 ====================

def type_string_to_enum(type_str: str) -> Optional[SymbolType]:
    """将类型字符串转换为枚举"""
    mapping = {
        'integer': SymbolType.INTEGER,
        'real': SymbolType.REAL,
        'boolean': SymbolType.BOOLEAN,
        'string': SymbolType.STRING,
    }
    return mapping.get(type_str.lower())


def is_numeric_type(symbol_type: SymbolType) -> bool:
    """检查是否为数值类型"""
    return symbol_type in [SymbolType.INTEGER, SymbolType.REAL]


def can_convert(from_type: SymbolType, to_type: SymbolType) -> bool:
    """检查类型是否可以隐式转换"""
    # 整数可以转换为实数
    if from_type == SymbolType.INTEGER and to_type == SymbolType.REAL:
        return True
    # 相同类型可以转换
    if from_type == to_type:
        return True
    return False


def binary_op_result_type(left_type: SymbolType, op: str, right_type: SymbolType) -> Optional[SymbolType]:
    """根据二元运算符和操作数类型，推断结果类型"""
    # 算术运算符
    if op in ['+', '-', '*', '/']:
        if is_numeric_type(left_type) and is_numeric_type(right_type):
            # 如果有一个是 REAL，结果为 REAL
            if left_type == SymbolType.REAL or right_type == SymbolType.REAL:
                return SymbolType.REAL
            return SymbolType.INTEGER
        return None
    
    # 关系运算符
    if op in ['<', '<=', '>', '>=', '=', '<>']:
        if is_numeric_type(left_type) and is_numeric_type(right_type):
            return SymbolType.BOOLEAN
        if left_type == right_type == SymbolType.STRING and op in ['=', '<>']:
            return SymbolType.BOOLEAN
        return None
    
    # 逻辑运算符
    if op in ['and', 'or']:
        if left_type == SymbolType.BOOLEAN and right_type == SymbolType.BOOLEAN:
            return SymbolType.BOOLEAN
        return None
    
    return None
