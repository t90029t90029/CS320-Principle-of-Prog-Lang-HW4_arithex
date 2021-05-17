#------------------------------------------------------------------------------ 
# Shang Chun,Lin  CS320 HW4
#------------------------------------------------------------------------------ 

# Arith Expr Parser (top-down)
#
# Grammar: (num is a terminal representing an integer)
#   exp    -> term {('+'|'-') term}
#   term   -> factor {('*'|'/') factor}
#   factor -> '-' factor 
#          |  '(' exp ')'
#          |  num
#
# Usage: linux> ./python3 arithex0.py 'arith exp'
#
import sys

# str is an input program, e.g. '12 + (4 * 2 - 5)'
def parse(str):
    i = 0  # idx to input string

    # lookahead next non-space char, return '$' if reaches the end
    def next():
        if i >= len(str):
            return '$'
        while str[i] == ' ':
            advance()
        if i < len(str):
            return str[i]
        return '$'

    # advance the input idx
    def advance():
        nonlocal i
        i += 1

    # exp -> term {('+'|'-') term}
    def exp():
        ast = term()
        while next() == '+' or next() == '-':
            if next() == '+':
                advance()
                ast = ['+',ast,term()]
            else:
                advance()
                ast = ['-',ast,term()]
        return ast
            
    # term -> factor {('*'|'/') factor}
    def term():
        ast = factor()
        while next() == '*' or next() == '/':
            if next() == '*':
                advance()
                ast = ['*',ast,factor()]
            else:
                advance()
                ast = ['/',ast,factor()]
        return ast

    # factor -> '-' factor | '(' exp ')' | num
    def factor():
        if next() == '-':
            advance()
            ast = ['-',factor()]

        elif next() == '(':
            advance()
            ast = exp()
            if next() != ')':
                if i == len(str):
                    raise Exception("expected a close paren at the end")
                else:
                    raise Exception("expected a close paren, got " + next())
            advance()

        else:
            c = next()
            ast = ''
            if not c.isdigit():
                raise Exception("expected a number, got " + c)
            while c.isdigit():
                ast = ast + c
                advance()
                c =  next()

        return ast

    # parsing starts here
    ast = exp()
    if i < len(str):
        raise Exception("found extra chars: " + str[i:])
    return ast

def eval(ast):
    if len(ast) == 1 and ast.isdigit() : return int(ast)
    elif len(ast) == 2: return -1 * int(ast[1])
    else:
        operator = ast[0]
        if type(ast[1]) == str:
            left = int(ast[1])
        elif type(ast[1]) == list:
            left = eval(ast[1])
        if type(ast[2]) == str:
            right = int(ast[2])
        elif type(ast[2]) == list:
            right = eval(ast[2])

        if operator == '+': return left + right
        elif operator == '-': return left - right
        elif operator == '*': return left * right
        elif operator == '/': return left / right
    raise Exception("operator got " + operator + " in eval.")

if __name__ == "__main__":
    ast = parse('12 + (4 * 2 - 5)')
    print(ast)
    print("Interpreting:", eval(ast))

    ast = parse('12 + 2 * (10 - - 4 / 2) + 6')
    print(ast)
    print("Interpreting:", eval(ast))
    # below are error cases; should test each one separately
    # parse('x')      
    # parse('1=2')   
    # parse('1++2')   
    # parse('(1+2')   
#   parse(sys.argv[1])
