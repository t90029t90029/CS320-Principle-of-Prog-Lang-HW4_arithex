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
        # ... add code to skip spaces
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
        term()
        while next() == '+' or next() == '-':
            advance()
            term()
            
    # term -> factor {('*'|'/') factor}
    def term():
        # ... add code
        factor()
        while next() == '*' or next() == '/':
            advance()
            factor()

    # factor -> '-' factor | '(' exp ')' | num
    def factor():
        if next() == '-':
            # ... add code
            advance()
            factor()

        elif next() == '(':
            # ... add code
            advance()
            exp()
            if next() != ')':
                if i == len(str):
                    raise Exception("expected a close paren at the end")
                else:
                    raise Exception("expected a close paren, got " + next())
            advance()

        else:
            c = next()
            if not c.isdigit():
                raise Exception("expected a number, got " + c)
            # ... add code to collect all digits
            while c.isdigit():
                advance()
                c = next()
           
    # parsing starts here
    exp()
    if i < len(str):
        raise Exception("found extra chars: " + str[i:])
    print("OK")   # parsing successful

if __name__ == "__main__":
    parse('12 + (4 * 2 - 5)')
    parse('12 + 2 * (10 - - 4 / 2) + 6')
    # below are error cases; should test each one separately
    parse('x')      
    # parse('1=2')   
    # parse('1++2')   
    # parse('(1+2')   
#   parse(sys.argv[1])
