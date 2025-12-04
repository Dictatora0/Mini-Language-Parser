"""
Mini 语言语法分析器 - 核心模块
包含词法分析器、语法分析器、AST、符号表和解释器
"""

from .lexer import Lexer, Token, TokenType
from .parser_ast import (
    ASTParser, parse_to_ast, parse_and_print_ast,
    parse_from_source, parse_from_file
)
from .ast_nodes import (
    ASTNode, Program, Block, Statement, Expression,
    Assignment, IfStatement, WhileStatement,
    BinaryOp, UnaryOp, Number, String, Boolean, Variable,
    VarDeclarations, VarDecl,
    ASTPrinter, print_ast
)
from .symbol_table import SymbolTable, Symbol, SymbolType, ScopedSymbolTable
from .interpreter import Interpreter, run_program

__version__ = "2.0.0"
__author__ = "Compiler Principles Course"
__description__ = "Mini Language Parser - Enhanced with AST generation, symbol table, and interpreter"

__all__ = [
    # Lexer
    'Lexer', 'Token', 'TokenType',
    # Parser
    'ASTParser', 'parse_from_source', 'parse_from_file',
    'parse_to_ast', 'parse_and_print_ast',
    # AST Nodes
    'ASTNode', 'Program', 'Block', 'Statement', 'Expression',
    'Assignment', 'IfStatement', 'WhileStatement',
    'BinaryOp', 'UnaryOp', 'Number', 'String', 'Boolean', 'Variable',
    'VarDeclarations', 'VarDecl',
    'ASTPrinter', 'print_ast',
    # Symbol Table
    'SymbolTable', 'Symbol', 'SymbolType', 'ScopedSymbolTable',
    # Interpreter
    'Interpreter', 'run_program',
]
