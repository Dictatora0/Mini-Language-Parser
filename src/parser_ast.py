"""
Mini 语言递归下降语法分析器 (AST 生成版本)
在解析的同时构建抽象语法树 (AST)
"""

from typing import List, Optional, Set
from .lexer import Token, TokenType, Lexer
from .ast_nodes import *
from .symbol_table import Symbol, SymbolType, ScopedSymbolTable, type_string_to_enum


class ParseError(Exception):
    """语法分析错误异常"""
    def __init__(self, message: str, token: Token, source_line: str = ""):
        self.message = message
        self.token = token
        self.source_line = source_line
        super().__init__(self.format_error())
    
    def format_error(self) -> str:
        """格式化错误信息，包含源代码行和指针"""
        result = f"语法错误 [行{self.token.line}:列{self.token.column}]: {self.message}\n"
        if self.source_line:
            result += f"  {self.source_line}\n"
            result += f"  {' ' * (self.token.column - 1)}^\n"
        return result


class ASTParser:
    """
    AST 生成器
    在解析的同时构建抽象语法树
    """
    
    # 限制常量
    MAX_RECURSION_DEPTH = 100
    MAX_NESTING_DEPTH = 50
    MAX_EXPRESSION_DEPTH = 50
    
    def __init__(self, tokens: List[Token], source_code: str = ""):
        self.tokens = tokens
        self.source_code = source_code
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
        self.errors: List[str] = []
        self.success = True
        
        # 符号表
        self.symbol_table = ScopedSymbolTable()
        
        # 递归深度跟踪
        self.recursion_depth = 0
        self.nesting_depth = 0
        self.expression_depth = 0
        self.source_lines = source_code.split('\n') if source_code else []
    
    def get_source_line(self, line_number: int) -> str:
        """获取源代码的特定行"""
        if 0 < line_number <= len(self.source_lines):
            return self.source_lines[line_number - 1]
        return ""
    
    def check_recursion_depth(self, context: str = ""):
        """检查递归深度，防止栈溢出"""
        if self.recursion_depth >= self.MAX_RECURSION_DEPTH:
            self.error(f"递归层次过深（超过 {self.MAX_RECURSION_DEPTH} 层）{context}")
            return False
        return True
    
    def check_nesting_depth(self):
        """检查嵌套深度"""
        if self.nesting_depth >= self.MAX_NESTING_DEPTH:
            self.error(f"嵌套层次过深（超过 {self.MAX_NESTING_DEPTH} 层）")
            return False
        return True
    
    def check_expression_depth(self):
        """检查表达式深度"""
        if self.expression_depth >= self.MAX_EXPRESSION_DEPTH:
            self.error(f"表达式嵌套过深（超过 {self.MAX_EXPRESSION_DEPTH} 层）")
            return False
        return True
    
    def advance(self):
        """移动到下一个 token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        """向前看 offset 个 token"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def check(self, *token_types: TokenType) -> bool:
        """检查当前 token 是否匹配给定类型（不消费）"""
        return self.current_token and self.current_token.type in token_types
    
    def match(self, *token_types: TokenType) -> bool:
        """检查并消费 token（如果匹配）"""
        if self.check(*token_types):
            self.advance()
            return True
        return False
    
    def expect(self, token_type: TokenType, error_msg: str = None) -> Optional[Token]:
        """期望当前 token 为指定类型，否则报错"""
        if not self.check(token_type):
            if error_msg is None:
                error_msg = f"期望 {token_type.name}，但得到 {self.current_token.type.name}"
            self.error(error_msg)
            return None
        token = self.current_token
        self.advance()
        return token
    
    def error(self, message: str):
        """记录错误"""
        source_line = self.get_source_line(self.current_token.line)
        error_info = ParseError(message, self.current_token, source_line).format_error()
        self.errors.append(error_info)
        self.success = False
    
    def synchronize(self, sync_set: Set[TokenType]):
        """错误恢复：跳过 token 直到遇到同步集中的 token"""
        while not self.check(TokenType.EOF) and self.current_token.type not in sync_set:
            self.advance()
    
    # ==================== 语法分析函数 (生成 AST) ====================
    
    def parse(self) -> Optional[Program]:
        """解析入口：<program>"""
        try:
            ast = self.program()
            if not self.check(TokenType.EOF):
                self.error(f"程序结束后有多余的内容: {self.current_token.value}")
            return ast if self.success else None
        except ParseError as e:
            self.errors.append(str(e))
            return None
    
    def program(self) -> Optional[Program]:
        """
        <program> ::= "program" IDENTIFIER ";" [<var_declarations>] <block> "."
        """
        if not self.expect(TokenType.PROGRAM, "程序必须以 'program' 关键字开头"):
            return None
        
        name_token = self.expect(TokenType.IDENTIFIER, "program 后应跟程序名标识符")
        if not name_token:
            return None
        program_name = name_token.value
        
        if not self.expect(TokenType.SEMICOLON, "程序名后缺少分号 ';'"):
            self.synchronize({TokenType.VAR, TokenType.BEGIN})
        
        # 可选的变量声明
        var_declarations = None
        if self.check(TokenType.VAR):
            var_declarations = self.var_declarations()
        
        # 程序体
        block = self.block()
        
        if not self.expect(TokenType.DOT, "程序必须以 '.' 结尾"):
            return None
        
        return Program(
            name=program_name,
            var_declarations=var_declarations,
            block=block,
            line=name_token.line,
            column=name_token.column
        )
    
    def var_declarations(self) -> Optional[VarDeclarations]:
        """
        <var_declarations> ::= "var" <var_decl> { ";" <var_decl> } ";"
        <var_decl> ::= IDENTIFIER { "," IDENTIFIER } ":" <type>
        """
        if not self.expect(TokenType.VAR):
            return None
        
        declarations = []
        
        while True:
            # 读取变量名列表
            var_names = []
            name_token = self.expect(TokenType.IDENTIFIER, "期望变量名")
            if not name_token:
                break
            var_names.append((name_token.value, name_token.line, name_token.column))
            
            while self.match(TokenType.COMMA):
                name_token = self.expect(TokenType.IDENTIFIER, "逗号后期望变量名")
                if not name_token:
                    break
                var_names.append((name_token.value, name_token.line, name_token.column))
            
            # 期望冒号
            if not self.expect(TokenType.COLON, "变量名后期望 ':'"):
                break
            
            # 期望类型
            type_token = None
            if self.check(TokenType.INTEGER_TYPE, TokenType.REAL_TYPE, 
                         TokenType.BOOLEAN_TYPE, TokenType.STRING_TYPE):
                type_token = self.current_token
                self.advance()
            else:
                self.error("期望类型关键字 (integer, real, boolean, string)")
                break
            
            # 创建声明节点并添加到符号表
            var_type = type_token.value.lower()
            for var_name, line, col in var_names:
                decl = VarDecl(name=var_name, var_type=var_type, line=line, column=col)
                declarations.append(decl)
                
                # 添加到符号表
                symbol_type = type_string_to_enum(var_type)
                if symbol_type:
                    symbol = Symbol(var_name, symbol_type, line, col)
                    if not self.symbol_table.define(symbol):
                        self.error(f"变量 '{var_name}' 重复声明")
            
            # 期望分号
            if not self.expect(TokenType.SEMICOLON, "变量声明后期望 ';'"):
                break
            
            # 如果下一个不是标识符，结束声明
            if not self.check(TokenType.IDENTIFIER):
                break
        
        return VarDeclarations(declarations=declarations)
    
    def block(self) -> Optional[Block]:
        """
        <block> ::= "begin" <statement_list> "end"
        """
        if not self.expect(TokenType.BEGIN, "缺少 'begin'"):
            return None
        
        statements = self.statement_list()
        
        if not self.expect(TokenType.END, "缺少 'end'"):
            self.synchronize({TokenType.DOT, TokenType.SEMICOLON})
        
        return Block(statements=statements)
    
    def statement_list(self) -> List[Statement]:
        """
        <statement_list> ::= <statement> { ";" <statement> }
        """
        statements = []
        
        # 处理空语句块
        if self.check(TokenType.END):
            return statements
        
        stmt = self.statement()
        if stmt:
            statements.append(stmt)
        
        # 处理后续语句
        while self.match(TokenType.SEMICOLON):
            # 检查是否为语句块结束（允许末尾多余分号）
            if self.check(TokenType.END):
                break
            
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def statement(self) -> Optional[Statement]:
        """
        <statement> ::= <assignment_stmt>
                      | <if_stmt>
                      | <while_stmt>
                      | <block>
                      | <write_stmt>
                      | <read_stmt>
                      | ε
        """
        if self.check(TokenType.IDENTIFIER):
            return self.assignment_stmt()
        elif self.check(TokenType.IF):
            return self.if_stmt()
        elif self.check(TokenType.WHILE):
            return self.while_stmt()
        elif self.check(TokenType.BEGIN):
            return self.block()
        elif self.check(TokenType.WRITE):
            return self.write_stmt()
        elif self.check(TokenType.READ):
            return self.read_stmt()
        elif self.check(TokenType.END, TokenType.SEMICOLON):
            # 空语句
            return EmptyStatement()
        else:
            if not self.check(TokenType.END, TokenType.EOF):
                self.error(f"无效的语句开始: {self.current_token.value}")
                self.synchronize({TokenType.SEMICOLON, TokenType.END})
            return EmptyStatement()
    
    def assignment_stmt(self) -> Optional[Assignment]:
        """
        <assignment_stmt> ::= IDENTIFIER ":=" <expression>
        """
        var_token = self.expect(TokenType.IDENTIFIER)
        if not var_token:
            return None
        var_name = var_token.value
        
        # 检查变量是否已声明
        if not self.symbol_table.exists(var_name):
            self.error(f"变量 '{var_name}' 未声明")
        
        if not self.expect(TokenType.ASSIGN, "赋值语句缺少 ':=' 运算符"):
            self.synchronize({TokenType.SEMICOLON, TokenType.END})
            return None
        
        expr = self.expression()
        if not expr:
            self.error("赋值语句右侧表达式错误")
            self.synchronize({TokenType.SEMICOLON, TokenType.END})
            return None
        
        return Assignment(
            variable=var_name,
            expression=expr,
            line=var_token.line,
            column=var_token.column
        )
    
    def if_stmt(self) -> Optional[IfStatement]:
        """
        <if_stmt> ::= "if" <condition> "then" <statement> [ "else" <statement> ]
        """
        if_token = self.current_token
        if not self.expect(TokenType.IF):
            return None
        
        condition = self.condition()
        if not condition:
            self.error("if 语句条件表达式错误")
            self.synchronize({TokenType.THEN})
        
        if not self.expect(TokenType.THEN, "if 语句缺少 'then'"):
            self.synchronize({TokenType.IDENTIFIER, TokenType.IF, TokenType.WHILE, 
                            TokenType.BEGIN, TokenType.SEMICOLON})
            return None
        
        then_stmt = self.statement()
        
        # 可选的 else 部分
        else_stmt = None
        if self.match(TokenType.ELSE):
            else_stmt = self.statement()
        
        return IfStatement(
            condition=condition,
            then_statement=then_stmt,
            else_statement=else_stmt,
            line=if_token.line,
            column=if_token.column
        )
    
    def while_stmt(self) -> Optional[WhileStatement]:
        """
        <while_stmt> ::= "while" <condition> "do" <statement>
        """
        while_token = self.current_token
        if not self.expect(TokenType.WHILE):
            return None
        
        condition = self.condition()
        if not condition:
            self.error("while 语句条件表达式错误")
            self.synchronize({TokenType.DO})
        
        if not self.expect(TokenType.DO, "while 语句缺少 'do'"):
            self.synchronize({TokenType.IDENTIFIER, TokenType.IF, TokenType.WHILE, 
                            TokenType.BEGIN, TokenType.SEMICOLON})
            return None
        
        body = self.statement()
        
        return WhileStatement(
            condition=condition,
            body=body,
            line=while_token.line,
            column=while_token.column
        )
    
    def write_stmt(self) -> Optional[WriteStatement]:
        """
        <write_stmt> ::= "write" "(" <expression> ")"
        """
        write_token = self.current_token
        if not self.expect(TokenType.WRITE):
            return None
        
        if not self.expect(TokenType.LPAREN, "write 语句后期望 '('"):
            self.synchronize({TokenType.SEMICOLON, TokenType.END})
            return None
        
        expr = self.expression()
        if not expr:
            self.error("write 语句中缺少表达式")
            self.synchronize({TokenType.RPAREN, TokenType.SEMICOLON})
            return None
        
        if not self.expect(TokenType.RPAREN, "write 语句缺少 ')'"):
            self.synchronize({TokenType.SEMICOLON, TokenType.END})
        
        return WriteStatement(
            expression=expr,
            line=write_token.line,
            column=write_token.column
        )
    
    def read_stmt(self) -> Optional[ReadStatement]:
        """
        <read_stmt> ::= "read" "(" IDENTIFIER ")"
        """
        read_token = self.current_token
        if not self.expect(TokenType.READ):
            return None
        
        if not self.expect(TokenType.LPAREN, "read 语句后期望 '('"):
            self.synchronize({TokenType.SEMICOLON, TokenType.END})
            return None
        
        var_token = self.expect(TokenType.IDENTIFIER, "read 语句中期望变量名")
        if not var_token:
            self.synchronize({TokenType.RPAREN, TokenType.SEMICOLON})
            return None
        
        var_name = var_token.value
        
        # 检查变量是否已声明
        if not self.symbol_table.exists(var_name):
            self.error(f"变量 '{var_name}' 未声明")
        
        if not self.expect(TokenType.RPAREN, "read 语句缺少 ')'"):
            self.synchronize({TokenType.SEMICOLON, TokenType.END})
        
        return ReadStatement(
            variable=var_name,
            line=read_token.line,
            column=read_token.column
        )
    
    def condition(self) -> Optional[Expression]:
        """
        <condition> ::= <or_term> { "or" <or_term> }
        """
        left = self.or_term()
        if not left:
            return None
        
        while self.check(TokenType.OR):
            op_token = self.current_token
            self.advance()
            right = self.or_term()
            if not right:
                self.error("'or' 运算符后缺少有效的条件表达式")
                return None
            left = BinaryOp(left=left, op=op_token, right=right)
        
        return left
    
    def or_term(self) -> Optional[Expression]:
        """
        <or_term> ::= <and_term> { "and" <and_term> }
        """
        left = self.and_term()
        if not left:
            return None
        
        while self.check(TokenType.AND):
            op_token = self.current_token
            self.advance()
            right = self.and_term()
            if not right:
                self.error("'and' 运算符后缺少有效的条件表达式")
                return None
            left = BinaryOp(left=left, op=op_token, right=right)
        
        return left
    
    def and_term(self) -> Optional[Expression]:
        """
        <and_term> ::= <not_term>
        """
        return self.not_term()
    
    def not_term(self) -> Optional[Expression]:
        """
        <not_term> ::= [ "not" ] <comparison>
        """
        if self.match(TokenType.NOT):
            op_token = self.tokens[self.pos - 1]  # 获取刚消费的 NOT token
            operand = self.comparison()
            if not operand:
                return None
            return UnaryOp(op=op_token, operand=operand)
        
        return self.comparison()
    
    def comparison(self) -> Optional[Expression]:
        """
        <comparison> ::= <expression> <relop> <expression>
                       | "(" <condition> ")"
        """
        # 处理括号中的条件
        if self.match(TokenType.LPAREN):
            expr = self.condition()
            if not expr:
                self.error("括号内条件表达式错误")
                return None
            if not self.expect(TokenType.RPAREN, "条件表达式缺少右括号 ')'"):
                return None
            return expr
        
        # 处理关系表达式
        left = self.expression()
        if not left:
            return None
        
        # 关系运算符
        if self.check(TokenType.LT, TokenType.LE, TokenType.GT, 
                     TokenType.GE, TokenType.EQ, TokenType.NE):
            op_token = self.current_token
            self.advance()
            right = self.expression()
            if not right:
                self.error("关系运算符后缺少表达式")
                return None
            return BinaryOp(left=left, op=op_token, right=right)
        else:
            self.error("条件表达式缺少关系运算符")
            return None
    
    def expression(self) -> Optional[Expression]:
        """
        <expression> ::= <term> { ("+" | "-") <term> }
        """
        left = self.term()
        if not left:
            return None
        
        while self.check(TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token
            self.advance()
            right = self.term()
            if not right:
                self.error("运算符 '+'/'-' 后缺少项")
                return None
            left = BinaryOp(left=left, op=op_token, right=right)
        
        return left
    
    def term(self) -> Optional[Expression]:
        """
        <term> ::= <factor> { ("*" | "/") <factor> }
        """
        left = self.factor()
        if not left:
            return None
        
        while self.check(TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self.current_token
            self.advance()
            right = self.factor()
            if not right:
                self.error("运算符 '*'/'/' 后缺少因子")
                return None
            left = BinaryOp(left=left, op=op_token, right=right)
        
        return left
    
    def factor(self) -> Optional[Expression]:
        """
        <factor> ::= IDENTIFIER
                   | INTEGER | REAL | STRING
                   | TRUE | FALSE
                   | "(" <expression> ")"
                   | "-" <factor>
        """
        # 标识符（变量）
        if self.check(TokenType.IDENTIFIER):
            token = self.current_token
            self.advance()
            
            # 检查变量是否已声明
            if not self.symbol_table.exists(token.value):
                self.error(f"变量 '{token.value}' 未声明")
            
            return Variable(name=token.value, line=token.line, column=token.column)
        
        # 整数
        if self.check(TokenType.INTEGER):
            token = self.current_token
            self.advance()
            return Number(value=float(token.value), line=token.line, column=token.column)
        
        # 浮点数
        if self.check(TokenType.REAL):
            token = self.current_token
            self.advance()
            return Number(value=float(token.value), line=token.line, column=token.column)
        
        # 字符串
        if self.check(TokenType.STRING):
            token = self.current_token
            self.advance()
            return String(value=token.value, line=token.line, column=token.column)
        
        # 布尔值
        if self.check(TokenType.TRUE):
            token = self.current_token
            self.advance()
            return Boolean(value=True, line=token.line, column=token.column)
        
        if self.check(TokenType.FALSE):
            token = self.current_token
            self.advance()
            return Boolean(value=False, line=token.line, column=token.column)
        
        # 括号表达式
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            if not expr:
                self.error("括号内表达式错误")
                return None
            if not self.expect(TokenType.RPAREN, "表达式缺少右括号 ')'"):
                return None
            return expr
        
        # 负号
        if self.match(TokenType.MINUS):
            op_token = self.tokens[self.pos - 1]
            operand = self.factor()
            if not operand:
                return None
            return UnaryOp(op=op_token, operand=operand)
        
        # 错误情况
        self.error(f"表达式错误: 期望标识符、数字或表达式，但得到 '{self.current_token.value}'")
        return None
    
    def get_result(self) -> str:
        """获取分析结果"""
        if self.success and len(self.errors) == 0:
            return "该程序符合语法要求。"
        else:
            return "\n".join(self.errors)


# ==================== 便捷函数 ====================

def parse_to_ast(source_code: str, enable_semantic_check: bool = True) -> tuple[Optional[Program], List[str], ScopedSymbolTable]:
    """
    从源代码解析并生成 AST
    
    Args:
        source_code: 源代码字符串
        enable_semantic_check: 是否启用语义检查（默认启用）
    
    Returns:
        (ast, errors, symbol_table) 元组
    """
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    # 检查词法错误
    errors = []
    for token in tokens:
        if token.type == TokenType.ERROR:
            errors.append(f"词法错误 [行{token.line}:列{token.column}]: 无法识别的字符 '{token.value}'")
    
    if errors:
        return None, errors, None
    
    # 语法分析
    parser = ASTParser(tokens, source_code)
    ast = parser.parse()
    
    # 如果语法分析有错误，直接返回
    if parser.errors:
        return ast, parser.errors, parser.symbol_table
    
    # 语义分析（可选）
    if enable_semantic_check and ast and parser.symbol_table:
        from .semantic_analyzer import analyze_semantics
        semantic_errors = analyze_semantics(ast, parser.symbol_table)
        if semantic_errors:
            # 合并错误
            all_errors = parser.errors + semantic_errors
            return ast, all_errors, parser.symbol_table
    
    return ast, parser.errors, parser.symbol_table


def parse_and_print_ast(source_code: str) -> str:
    """解析并打印 AST"""
    ast, errors, symbol_table = parse_to_ast(source_code)
    
    if errors:
        return "\n".join(errors)
    
    if ast:
        result = "语法分析成功！\n\n"
        result += "=== 抽象语法树 (AST) ===\n"
        result += print_ast(ast)
        result += "\n=== 符号表 ===\n"
        result += symbol_table.get_global_scope().print_table()
        return result
    else:
        return "解析失败"


# ==================== 兼容函数（保持向后兼容）====================

def parse_from_source(source_code: str) -> str:
    """
    从源代码解析（兼容旧版接口）
    只返回语法检查结果，不生成 AST
    """
    ast, errors, _ = parse_to_ast(source_code)
    
    if errors:
        return "\n".join(errors)
    
    if ast:
        return "该程序符合语法要求。"
    else:
        return "解析失败"


def parse_from_file(token_file: str) -> str:
    """从 token 文件读取并解析（兼容旧版接口）"""
    tokens = []
    try:
        with open(token_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) >= 4:
                    token_type = TokenType[parts[0]]
                    value = parts[1]
                    line_num = int(parts[2])
                    column = int(parts[3])
                    tokens.append(Token(token_type, value, line_num, column))
    except Exception as e:
        return f"读取 token 文件失败: {e}"
    
    parser = ASTParser(tokens)
    parser.parse()
    return parser.get_result()
