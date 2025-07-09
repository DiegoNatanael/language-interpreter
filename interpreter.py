import enum

# --- Token Types ---
class TokenType(enum.Enum):
    INTEGER    = 'INTEGER'
    PLUS       = 'PLUS'
    MINUS      = 'MINUS'
    MULTIPLY   = 'MULTIPLY'
    DIVIDE     = 'DIVIDE'
    LPAREN     = 'LPAREN'
    RPAREN     = 'RPAREN'
    ID         = 'ID'
    ASSIGN     = 'ASSIGN'
    EOF        = 'EOF'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type.name}, {self.value})"

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self, message="Invalid character"):
        raise Exception(f"Lexing error at position {self.pos}: {message}")

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        """Handle identifiers (variable names)."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return Token(TokenType.ID, result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            if self.current_char == '=': 
                self.advance()
                return Token(TokenType.ASSIGN, '=')

            self.error(f"Unrecognized character '{self.current_char}'")

        return Token(TokenType.EOF, None)

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST): 
    def __init__(self, left, op, right):
        self.left = left 
        self.op = op     
        self.right = right

class Var(AST): 
    def __init__(self, token):
        self.token = token 
        self.value = token.value 


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message="Invalid syntax"):
        raise Exception(f"Parsing error: {message} at token {self.current_token}")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type.name}, got {self.current_token.type.name}")

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN | ID (NEW)"""
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type == TokenType.ID:
            self.eat(TokenType.ID)
            return Var(token)
        else:
            self.error("Expected integer, left parenthesis, or identifier")

    def term(self):
        """term : factor ((MULTIPLY | DIVIDE) factor)*"""
        node = self.factor()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        """
        Parses a program, which can be an assignment statement or an expression.
        This is modified for the REPL to handle a single line of input.
        """
        if self.current_token.type == TokenType.ID and \
           self.lexer.text[self.lexer.pos] == '=': 
            node = self.assignment_statement()
        else:
            node = self.expr()

        if self.current_token.type != TokenType.EOF:
             self.error("Unexpected tokens at end of line")
        return node

    def assignment_statement(self): 
        """assignment_statement : ID ASSIGN expr"""
        left = Var(self.current_token)
        self.eat(TokenType.ID)
        op = self.current_token 
        self.eat(TokenType.ASSIGN)
        right = self.expr() 
        node = Assign(left, op, right)
        return node


# --- Interpreter ---
class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {} # Dictionary to store variable values

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIVIDE:
            right_val = self.visit(node.right)
            if right_val == 0:
                raise Exception("Runtime error: Division by zero")
            return self.visit(node.left) / right_val

    def visit_Num(self, node):
        return node.value

    def visit_Assign(self, node):
        var_name = node.left.value
        value = self.visit(node.right) 
        self.GLOBAL_SCOPE[var_name] = value 

    def visit_Var(self, node):
        var_name = node.value
        value = self.GLOBAL_SCOPE.get(var_name) 
        if value is None:
            raise Exception(f"Runtime error: Undefined variable '{var_name}'")
        return value

    def interpret(self):
        ast = self.parser.parse()
        if isinstance(ast, Assign):
            self.visit(ast) 
            return None 
        else:
            return self.visit(ast)

def main():
    print("Tiny Language REPL (Variables & Assignment)")
    print("Type 'exit' or 'quit' to end.")
    lexer = Lexer("") 
    parser = Parser(lexer)
    interpreter = Interpreter(parser)

    while True:
        try:
            text = input('calc> ')
            if text.lower() in ('exit', 'quit'):
                break
            if not text.strip(): # Skip empty input
                continue

            lexer.text = text # Update lexer with new input
            lexer.pos = 0
            lexer.current_char = lexer.text[lexer.pos] if lexer.text else None
            parser.current_token = lexer.get_next_token() # Reset parser's current token

            result = interpreter.interpret()
            if result is not None: # Only print if it's an expression
                print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
