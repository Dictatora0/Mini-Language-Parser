"""
Mini 语言词法分析器
用于将源代码转换为 Token 流
"""

import re
from enum import Enum, auto
from typing import List, Optional, Tuple


class TokenType(Enum):
    """Token 类型枚举"""
    # 关键字
    PROGRAM = auto()
    BEGIN = auto()
    END = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    WHILE = auto()
    DO = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # 标识符和字面量
    IDENTIFIER = auto()
    NUMBER = auto()
    
    # 运算符
    PLUS = auto()        # +
    MINUS = auto()       # -
    MULTIPLY = auto()    # *
    DIVIDE = auto()      # /
    ASSIGN = auto()      # :=
    
    # 关系运算符
    LT = auto()          # <
    LE = auto()          # <=
    GT = auto()          # >
    GE = auto()          # >=
    EQ = auto()          # =
    NE = auto()          # <>
    
    # 分隔符
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    SEMICOLON = auto()   # ;
    COMMA = auto()       # ,
    DOT = auto()         # .
    
    # 特殊
    EOF = auto()
    ERROR = auto()


class Token:
    """Token 类"""
    def __init__(self, token_type: TokenType, value: str, line: int, column: int):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"
    
    def __str__(self):
        return f"<{self.type.name}, {self.value}>"


class Lexer:
    """词法分析器"""
    
    # 关键字映射
    KEYWORDS = {
        'program': TokenType.PROGRAM,
        'begin': TokenType.BEGIN,
        'end': TokenType.END,
        'if': TokenType.IF,
        'then': TokenType.THEN,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'do': TokenType.DO,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        """获取当前字符"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """向前看 offset 个字符"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        """前进一个字符"""
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        """跳过空白字符"""
        while self.current_char() and self.current_char() in ' \t\n\r':
            self.advance()
    
    def skip_comment(self):
        """跳过注释（支持 // 单行注释和 { } 块注释）"""
        if self.current_char() == '/' and self.peek_char() == '/':
            # 单行注释
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            if self.current_char() == '\n':
                self.advance()
            return True
        
        if self.current_char() == '{':
            # 块注释
            self.advance()
            while self.current_char():
                if self.current_char() == '}':
                    self.advance()
                    return True
                self.advance()
            return True
        
        return False
    
    def read_number(self) -> Token:
        """读取数字"""
        start_line = self.line
        start_column = self.column
        num_str = ''
        
        while self.current_char() and self.current_char().isdigit():
            num_str += self.current_char()
            self.advance()
        
        return Token(TokenType.NUMBER, num_str, start_line, start_column)
    
    def read_identifier(self) -> Token:
        """读取标识符或关键字"""
        start_line = self.line
        start_column = self.column
        id_str = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        # 检查是否为关键字
        id_lower = id_str.lower()
        token_type = self.KEYWORDS.get(id_lower, TokenType.IDENTIFIER)
        
        return Token(token_type, id_str, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        """执行词法分析，返回 Token 列表"""
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # 跳过注释
            if self.skip_comment():
                continue
            
            char = self.current_char()
            start_line = self.line
            start_column = self.column
            
            # 数字
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # 标识符或关键字
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # 运算符和分隔符
            if char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_column))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_column))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', start_line, start_column))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', start_line, start_column))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_column))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_column))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_column))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_column))
                self.advance()
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, '.', start_line, start_column))
                self.advance()
            elif char == ':':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.ASSIGN, ':=', start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.ERROR, char, start_line, start_column))
                    self.advance()
            elif char == '<':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.LE, '<=', start_line, start_column))
                    self.advance()
                    self.advance()
                elif self.peek_char() == '>':
                    self.tokens.append(Token(TokenType.NE, '<>', start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.LT, '<', start_line, start_column))
                    self.advance()
            elif char == '>':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.GE, '>=', start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.GT, '>', start_line, start_column))
                    self.advance()
            elif char == '=':
                self.tokens.append(Token(TokenType.EQ, '=', start_line, start_column))
                self.advance()
            else:
                # 未知字符
                self.tokens.append(Token(TokenType.ERROR, char, start_line, start_column))
                self.advance()
        
        # 添加 EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def save_tokens_to_file(self, filename: str):
        """将 Token 流保存到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            for token in self.tokens:
                f.write(f"{token.type.name}\t{token.value}\t{token.line}\t{token.column}\n")


def main():
    """测试词法分析器"""
    # 测试代码
    test_code = """
    program example;
    begin
        x := 10;
        y := 20;
        if x < y then
            z := x + y
        else
            z := x - y
    end.
    """
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    print("=== Token 流 ===")
    for token in tokens:
        print(token)
    
    # 保存到文件
    lexer.save_tokens_to_file("tokens.txt")
    print("\nToken 流已保存到 tokens.txt")


if __name__ == "__main__":
    main()
