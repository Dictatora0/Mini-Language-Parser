"""
Mini 语言递归下降语法分析器
实现对 Token 流的语法分析，检查语法正确性并报告错误
"""

from typing import List, Optional, Set
from lexer import Token, TokenType, Lexer


class ParseError(Exception):
    """语法分析错误异常"""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(self.format_error())
    
    def format_error(self) -> str:
        return f"语法错误 [行{self.token.line}:列{self.token.column}]: {self.message}"


class Parser:
    """递归下降语法分析器"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
        self.errors: List[str] = []
        self.success = True
    
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
    
    def match(self, *token_types: TokenType) -> bool:
        """检查当前 token 是否匹配给定类型"""
        return self.current_token and self.current_token.type in token_types
    
    def expect(self, token_type: TokenType, error_msg: str = None):
        """期望当前 token 为指定类型，否则报错"""
        if not self.match(token_type):
            if error_msg is None:
                error_msg = f"期望 {token_type.name}，但得到 {self.current_token.type.name}"
            self.error(error_msg)
            return False
        self.advance()
        return True
    
    def error(self, message: str):
        """记录错误"""
        error_info = f"语法错误 [行{self.current_token.line}:列{self.current_token.column}]: {message}"
        self.errors.append(error_info)
        self.success = False
    
    def synchronize(self, sync_set: Set[TokenType]):
        """错误恢复：跳过 token 直到遇到同步集中的 token"""
        while not self.match(TokenType.EOF) and self.current_token.type not in sync_set:
            self.advance()
    
    # ==================== 语法分析函数 ====================
    
    def parse(self) -> bool:
        """解析入口：<program>"""
        try:
            self.program()
            if not self.match(TokenType.EOF):
                self.error(f"程序结束后有多余的内容: {self.current_token.value}")
            return self.success
        except ParseError as e:
            self.errors.append(str(e))
            return False
    
    def program(self):
        """
        <program> ::= "program" IDENTIFIER ";" <block> "."
        """
        if not self.expect(TokenType.PROGRAM, "程序必须以 'program' 关键字开头"):
            return
        
        if not self.expect(TokenType.IDENTIFIER, "program 后应跟程序名标识符"):
            return
        
        if not self.expect(TokenType.SEMICOLON, "程序名后缺少分号 ';'"):
            self.synchronize({TokenType.BEGIN})
        
        self.block()
        
        if not self.expect(TokenType.DOT, "程序必须以 '.' 结尾"):
            return
    
    def block(self):
        """
        <block> ::= "begin" <statement_list> "end"
        """
        if not self.expect(TokenType.BEGIN, "缺少 'begin'"):
            return
        
        self.statement_list()
        
        if not self.expect(TokenType.END, "缺少 'end'"):
            self.synchronize({TokenType.DOT, TokenType.SEMICOLON})
    
    def statement_list(self):
        """
        <statement_list> ::= <statement> { ";" <statement> }
        """
        # 处理空语句块
        if self.match(TokenType.END):
            return
        
        self.statement()
        
        # 处理后续语句
        while self.match(TokenType.SEMICOLON):
            self.advance()  # 消耗分号
            
            # 检查是否为语句块结束（允许末尾多余分号）
            if self.match(TokenType.END):
                break
            
            self.statement()
    
    def statement(self):
        """
        <statement> ::= <assignment_stmt>
                      | <if_stmt>
                      | <while_stmt>
                      | <block>
                      | ε
        """
        if self.match(TokenType.IDENTIFIER):
            self.assignment_stmt()
        elif self.match(TokenType.IF):
            self.if_stmt()
        elif self.match(TokenType.WHILE):
            self.while_stmt()
        elif self.match(TokenType.BEGIN):
            self.block()
        elif self.match(TokenType.END, TokenType.SEMICOLON):
            # 空语句（允许多余分号）
            pass
        else:
            # 可能是空语句或错误
            if not self.match(TokenType.END, TokenType.EOF):
                self.error(f"无效的语句开始: {self.current_token.value}")
                self.synchronize({TokenType.SEMICOLON, TokenType.END})
    
    def assignment_stmt(self):
        """
        <assignment_stmt> ::= IDENTIFIER ":=" <expression>
        """
        if not self.expect(TokenType.IDENTIFIER):
            return
        
        if not self.expect(TokenType.ASSIGN, "赋值语句缺少 ':=' 运算符"):
            self.synchronize({TokenType.SEMICOLON, TokenType.END})
            return
        
        if not self.expression():
            self.error("赋值语句右侧表达式错误")
            self.synchronize({TokenType.SEMICOLON, TokenType.END})
    
    def if_stmt(self):
        """
        <if_stmt> ::= "if" <condition> "then" <statement> [ "else" <statement> ]
        """
        if not self.expect(TokenType.IF):
            return
        
        if not self.condition():
            self.error("if 语句条件表达式错误")
            self.synchronize({TokenType.THEN})
        
        if not self.expect(TokenType.THEN, "if 语句缺少 'then'"):
            self.synchronize({TokenType.IDENTIFIER, TokenType.IF, TokenType.WHILE, TokenType.BEGIN, TokenType.SEMICOLON})
            return
        
        self.statement()
        
        # 可选的 else 部分
        if self.match(TokenType.ELSE):
            self.advance()
            self.statement()
    
    def while_stmt(self):
        """
        <while_stmt> ::= "while" <condition> "do" <statement>
        """
        if not self.expect(TokenType.WHILE):
            return
        
        if not self.condition():
            self.error("while 语句条件表达式错误")
            self.synchronize({TokenType.DO})
        
        if not self.expect(TokenType.DO, "while 语句缺少 'do'"):
            self.synchronize({TokenType.IDENTIFIER, TokenType.IF, TokenType.WHILE, TokenType.BEGIN, TokenType.SEMICOLON})
            return
        
        self.statement()
    
    def condition(self) -> bool:
        """
        <condition> ::= <or_term> { "or" <or_term> }
        """
        if not self.or_term():
            return False
        
        while self.match(TokenType.OR):
            self.advance()
            if not self.or_term():
                self.error("'or' 运算符后缺少有效的条件表达式")
                return False
        
        return True
    
    def or_term(self) -> bool:
        """
        <or_term> ::= <and_term> { "and" <and_term> }
        """
        if not self.and_term():
            return False
        
        while self.match(TokenType.AND):
            self.advance()
            if not self.and_term():
                self.error("'and' 运算符后缺少有效的条件表达式")
                return False
        
        return True
    
    def and_term(self) -> bool:
        """
        <and_term> ::= <not_term>
        """
        return self.not_term()
    
    def not_term(self) -> bool:
        """
        <not_term> ::= [ "not" ] <comparison>
        """
        if self.match(TokenType.NOT):
            self.advance()
        
        return self.comparison()
    
    def comparison(self) -> bool:
        """
        <comparison> ::= <expression> <relop> <expression>
                       | "(" <condition> ")"
        """
        # 处理括号中的条件
        if self.match(TokenType.LPAREN):
            self.advance()
            if not self.condition():
                self.error("括号内条件表达式错误")
                return False
            if not self.expect(TokenType.RPAREN, "条件表达式缺少右括号 ')'"):
                return False
            return True
        
        # 处理关系表达式
        if not self.expression():
            return False
        
        # 关系运算符
        if self.match(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE, TokenType.EQ, TokenType.NE):
            self.advance()
            if not self.expression():
                self.error("关系运算符后缺少表达式")
                return False
        else:
            self.error("条件表达式缺少关系运算符")
            return False
        
        return True
    
    def expression(self) -> bool:
        """
        <expression> ::= <term> { ("+" | "-") <term> }
        """
        if not self.term():
            return False
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            self.advance()
            if not self.term():
                self.error("运算符 '+'/'-' 后缺少项")
                return False
        
        return True
    
    def term(self) -> bool:
        """
        <term> ::= <factor> { ("*" | "/") <factor> }
        """
        if not self.factor():
            return False
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            self.advance()
            if not self.factor():
                self.error("运算符 '*'/'/' 后缺少因子")
                return False
        
        return True
    
    def factor(self) -> bool:
        """
        <factor> ::= IDENTIFIER
                   | NUMBER
                   | "(" <expression> ")"
                   | "-" <factor>
        """
        # 标识符
        if self.match(TokenType.IDENTIFIER):
            self.advance()
            return True
        
        # 数字
        if self.match(TokenType.NUMBER):
            self.advance()
            return True
        
        # 括号表达式
        if self.match(TokenType.LPAREN):
            self.advance()
            if not self.expression():
                self.error("括号内表达式错误")
                return False
            if not self.expect(TokenType.RPAREN, "表达式缺少右括号 ')'"):
                return False
            return True
        
        # 负号
        if self.match(TokenType.MINUS):
            self.advance()
            return self.factor()
        
        # 错误情况
        self.error(f"表达式错误: 期望标识符、数字或表达式，但得到 '{self.current_token.value}'")
        return False
    
    def get_result(self) -> str:
        """获取分析结果"""
        if self.success and len(self.errors) == 0:
            return "该程序符合语法要求。"
        else:
            return "\n".join(self.errors)


def parse_from_file(token_file: str) -> str:
    """从 token 文件读取并解析"""
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
    
    parser = Parser(tokens)
    parser.parse()
    return parser.get_result()


def parse_from_source(source_code: str) -> str:
    """直接从源代码解析"""
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    # 检查词法错误
    for token in tokens:
        if token.type == TokenType.ERROR:
            return f"词法错误 [行{token.line}:列{token.column}]: 无法识别的字符 '{token.value}'"
    
    parser = Parser(tokens)
    parser.parse()
    return parser.get_result()


def main():
    """测试语法分析器"""
    
    print("=" * 60)
    print("Mini 语言语法分析器测试")
    print("=" * 60)
    
    # 测试用例 1：正确的程序
    test1 = """
    program example1;
    begin
        x := 10;
        y := 20;
        if x < y then
            z := x + y
        else
            z := x - y
    end.
    """
    
    print("\n【测试1】正确的程序")
    print("源代码:")
    print(test1)
    print("\n分析结果:")
    print(parse_from_source(test1))
    
    # 测试用例 2：表达式错误
    test2 = """
    program test2;
    begin
        i := 1 + 
    end.
    """
    
    print("\n" + "=" * 60)
    print("【测试2】表达式错误")
    print("源代码:")
    print(test2)
    print("\n分析结果:")
    print(parse_from_source(test2))
    
    # 测试用例 3：缺少分号
    test3 = """
    program test3;
    begin
        x := 10
        y := 20
    end.
    """
    
    print("\n" + "=" * 60)
    print("【测试3】缺少分号")
    print("源代码:")
    print(test3)
    print("\n分析结果:")
    print(parse_from_source(test3))
    
    # 测试用例 4：if 语句缺少 then
    test4 = """
    program test4;
    begin
        if x > 0
            y := 1
    end.
    """
    
    print("\n" + "=" * 60)
    print("【测试4】if 语句缺少 then")
    print("源代码:")
    print(test4)
    print("\n分析结果:")
    print(parse_from_source(test4))
    
    # 测试用例 5：复杂的嵌套结构
    test5 = """
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
    """
    
    print("\n" + "=" * 60)
    print("【测试5】复杂的嵌套结构")
    print("源代码:")
    print(test5)
    print("\n分析结果:")
    print(parse_from_source(test5))
    
    # 测试用例 6：逻辑表达式
    test6 = """
    program logic;
    begin
        if (x > 0) and (y < 10) or not (z = 5) then
            result := 1
    end.
    """
    
    print("\n" + "=" * 60)
    print("【测试6】逻辑表达式")
    print("源代码:")
    print(test6)
    print("\n分析结果:")
    print(parse_from_source(test6))


if __name__ == "__main__":
    main()
