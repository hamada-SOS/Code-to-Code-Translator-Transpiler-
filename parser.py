class ASTNode:
    pass

class Assignment(ASTNode):
    def __init__(self, var, value):
        self.var = var
        self.value = value

class Print(ASTNode):
    def __init__(self, value):
        self.value = value

class Read(ASTNode):
    def __init__(self, var):
        self.var = var

class ReadStr(ASTNode):
    def __init__(self, var):
        self.var = var

class ForLoop(ASTNode):
    def __init__(self, var, start, end, body):
        self.var = var
        self.start = start
        self.end = end
        self.body = body

class IfElse(ASTNode):
    def __init__(self, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def eat(self, expected_type):
        tok_type, value = self.current()
        if tok_type == expected_type:
            self.pos += 1
            return value
        raise SyntaxError(f"Expected {expected_type}, got {tok_type}")

    def parse(self):
        statements = []
        while self.current()[0] != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return Program(statements)

    def statement(self):
        tok = self.current()
        if tok[0] == 'SET':
            self.eat('SET')
            var = self.eat('ID')
            self.eat('EQ')
            val = self.expression()
            return Assignment(var, val)
        elif tok[0] == 'READ':
            self.eat('READ')
            var = self.eat('ID')
            return Read(var)
        elif tok[0] == 'READSTR':
            self.eat('READSTR')
            var = self.eat('ID')
            return ReadStr(var)
        elif tok[0] == 'PRINT':
            self.eat('PRINT')
            val = self.current()
            if val[0] == 'STRING':
                return Print(self.eat('STRING'))
            else:
                return Print(self.eat('ID'))
        elif tok[0] == 'FOR':
            self.eat('FOR')
            var = self.eat('ID')
            self.eat('FROM')
            start = self.eat('NUMBER')
            self.eat('TO')
            end = self.eat('NUMBER')
            body = []
            while self.current()[0] not in ('END', 'EOF', 'ELSE'):
                body.append(self.statement())
            self.eat('END')
            self.eat('FOR')
            return ForLoop(var, start, end, body)
        elif tok[0] == 'IF':
            self.eat('IF')
            left = self.eat('ID')
            op = self.eat('OP')
            tok = self.current()
            if tok[0] == 'NUMBER':
                right = self.eat('NUMBER')
            elif tok[0] == 'ID':
                right = self.eat('ID')
            else:
                raise SyntaxError(f"Expected NUMBER or ID, got {tok[0]}")
            condition = BinaryOp(left, op, right)
            if_body = []
            else_body = []
            while self.current()[0] not in ('ELSE', 'END', 'EOF'):
                if_body.append(self.statement())
            if self.current()[0] == 'ELSE':
                self.eat('ELSE')
                while self.current()[0] not in ('END', 'EOF'):
                    else_body.append(self.statement())
            self.eat('END')
            self.eat('IF')
            return IfElse(condition, if_body, else_body)
        else:
            raise SyntaxError(f"Unknown statement: {tok}")

    def expression(self):
        tok = self.current()
        if tok[0] == 'ID':
            left = self.eat('ID')
        elif tok[0] == 'NUMBER':
            left = self.eat('NUMBER')
        else:
            raise SyntaxError(f"Expected ID or NUMBER, got {tok[0]}")

        if self.current()[0] == 'OP':
            op = self.eat('OP')
            right_tok = self.current()
            if right_tok[0] == 'NUMBER':
                right = self.eat('NUMBER')
            elif right_tok[0] == 'ID':
                right = self.eat('ID')
            else:
                raise SyntaxError(f"Expected ID or NUMBER, got {right_tok[0]}")
            return BinaryOp(left, op, right)

        return left

