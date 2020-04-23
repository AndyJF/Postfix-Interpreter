from stack import *
from typing import List, Dict, Tuple, Any
import string


def tokenize(line: str,
            specials: str,
            whitespace: str) -> List[str]:
    '''
    Given an expression (a string), break it up into tokens.
    Inputs:
        expression: a string
        specials:   single-character tokens (usually operators)
        whitespace: characters that separate tokens (usually space)
    Return: a list of strings (each is a token)
    '''

    '''
    Method: implement a state machine, with three states:
    - OPERAND
    - SPECIAL
    - WHITESPACE
    Each character in the expression causes a transition among
    these three states.
    '''
    # The states
    IDLE       = 0
    OPERAND    = IDLE    + 1
    WHITESPACE = OPERAND + 1

    # Intial state
    state = IDLE

    # The list of tokens
    tokens = []
    for c in line:
        if state == IDLE:

            # Here, I handle some transitions for you.
            # Notice that, in each case, I take some action,
            # and (optionally) change the state
            if c in whitespace:
                state = WHITESPACE
                continue
            elif c in specials:
                state = IDLE
                tokens.append(c)
            else: # It's an operand character.  Start an operand
                state = OPERAND
                operand = c

        # Task 1:
        # Now, you must handle the remaining cases
        # When you are done, remove most of the 'pass' statements.
        elif state == OPERAND:
            if c in whitespace:
                # save the operand
                state = WHITESPACE
                tokens.append(operand)
                
            elif c in specials:
                # save the operand, save the special
                state = IDLE
                tokens.append(operand)
                tokens.append(c)
            else:
                # extend the operand
                state = OPERAND
                operand += c


        elif state == WHITESPACE:
            if c in whitespace:
                # do nothing
                continue
            elif c in specials:
                # save the special
                state = IDLE
                tokens.append(c)
            else:
                # start an operand
                state = OPERAND
                operand = c

    # Task 2: Check if we need to save the last operand

    if state == OPERAND:
        tokens.append(operand)
        
    return tokens

def precedence(operator: str) -> int:
    '''
    Precedence of operators.
    * / : highest
    + - : middle
    = () : lowest

    Returns a number (the precedence)
    '''
    if operator in "*/":
        precedence = 2
        return precedence
    elif operator in "+-":
        precedence = 1
        return precedence
    elif operator in "=()":
        precedence = 0
        return precedence
    else:
        return -1

def lexer(tokens: List[str]) -> List[Tuple[str, Any]]:
    '''
    Given a list of tokens, perform lexical analysis, and classify them.

    Return a list of tuples.  Each tuple has two values (lexical_type, token)
    The lexical_type is 'number', 'variable', 'operator', or 'unknown'
    '''
    lexer_list = []

    for token in tokens:
        lex_type = 'unknown'
        lex_value = token
        operators = "+-*/=()"
        if token in operators:
            lex_type = "operator"
        else:
            try:
                x = float(token)
                lex_type = "number"
            # Checks if token is a variable, based on the criteria that
            # python uses for variables (e.g., can't start with a number).
            except ValueError:
                if token[0] in string.ascii_letters + "_" and token[1:].isascii or token[1:].isdigit or token[1:] in "_":
                    lex_type = 'variable'
        lexer_list.append(tuple((lex_value, lex_type)))
    return lexer_list
        

def to_postfix(infix_expression: str) -> List[str]:
    '''
    Convert an infix expression into a postfix expression (one string)
    Return a list of lexemes (each one is tuple (lexical_tupe, token))

    Proceed thus:
    - call tokenize to convert the infix_expression into a list of tokens
    - call lexer to classify the tokens into a list of lexemes
    - use a stack-based algorithm to convert the infix list
      into a postfix list of strings, and return that.
    '''
    s = Stack()
    postfix_expr = []

    tokens = tokenize(infix_expression, '+-*/=()', ' \t')
    lexemes = lexer(tokens)

    for token, lex_type in lexemes:
        if token == '(':
            s.push(token)
        # Token is an operand
        elif lex_type != "operator":
            postfix_expr.append(token)
        # While stack is not empty and top isn't '(',
        # pop stack, append to postfix expression.
        elif token == ')':
            while not s.empty() and s.top() != '(':
                postfix_expr.append(s.pop())
            s.pop()
        # Token is an operator
        else:
            # While stack is not empty and precedence of top value in stack
            # is >= token's precedence, pop top of stack, append to postfix
            # expression.
            # Special case exists for when multiple "=" operators are encountered.
            # In this case, we should not pop from the stack.
            while not s.empty() and precedence(s.top()) >= precedence(token) and token != "=" and s.top() != "=":
                postfix_expr.append(s.pop())
            s.push(token)
    # Stack may have pending operators, so we pop them
    # and append to postfix expression.
    while not s.empty():
        postfix_expr.append(s.pop())

    return postfix_expr


def eval_postfix(postfix_expression: List[str],
                 symbol_table: Dict[str,float]) -> float:
    '''
    Evaluate a postfix expression.
    Inputs: the postfix expression (a list of strings)
            the symbol table (maps str names to floats)
    Output: a float (the expressions's value)

    Proceed as follows:
    - call lexer to classify the postfix expresion into a list of lexemes
    - use a stack-based algorithm to evaluate the expression.
    - when done, return the top of the stack.
    '''
    s = Stack()
    lexemes = lexer(postfix_expression)

    for token, lex_type in lexemes:
        if lex_type == "number":
            s.push(token)

        elif lex_type == "variable":
            s.push(token)

        elif lex_type == "operator":
            right_operand = s.pop()
            left_operand = s.pop()
            
            if token == "+":
                try:
                    right_operand = float(right_operand)
                # If right operand is a variable
                except ValueError:
                    # Get value of right_operand from symbol table
                    right_operand = symbol_table.get(right_operand)

                try:
                    left_operand = float(left_operand)
                # If left operand is a variable
                except ValueError:
                    # Get value of left_operand from symbol table
                    left_operand = symbol_table.get(left_operand)

                result = left_operand + right_operand
                s.push(result)

            elif token == "-":
                try:
                    right_operand = float(right_operand)
                # If right operand is a variable
                except ValueError:
                    # Get value of right_operand from symbol table
                    right_operand = symbol_table.get(right_operand)

                try:
                    left_operand = float(left_operand)
                # If left operand is a variable
                except ValueError:
                    # Get value of left_operand from symbol table
                    left_operand = symbol_table.get(left_operand)
                    
                result = left_operand - right_operand
                s.push(result)

            elif token == "*":
                try:
                    right_operand = float(right_operand)
                # If right operand is a variable
                except ValueError:
                    # Get value of right_operand from symbol table
                    right_operand = symbol_table.get(right_operand)

                try:
                    left_operand = float(left_operand)
                # If left operand is a variable
                except ValueError:
                    # Get value of left_operand from symbol table
                    left_operand = symbol_table.get(left_operand)

                result = left_operand * right_operand
                s.push(result)

            elif token == "/":
                try:
                    right_operand = float(right_operand)
                # If right operand is a variable
                except ValueError:
                    # Get value of right_operand from symbol table
                    right_operand = symbol_table.get(right_operand)

                try:
                    left_operand = float(left_operand)
                # If left operand is a variable
                except ValueError:
                    # Get value of left_operand from symbol table
                    left_operand = symbol_table.get(left_operand)

                result = left_operand / right_operand
                s.push(result)

            elif token == "=":
                try:
                    right_operand = float(right_operand)
                # If right operand is a variable
                except ValueError:
                    # Set value of right operand to value of right
                    # operand in symbol table.
                    right_operand = symbol_table.get(right_operand)

                try:
                    left_operand = float(left_operand)
                # If left operand is a variable
                except ValueError:
                    # Set value (right operand) of left_operand in symbol table
                    symbol_table[left_operand] = right_operand

                s.push(right_operand)

    value = s.pop()

    # Handles cases where only a variable is entered into
    # the interpreter.  If value is a number, we return it,
    # and when value is a variable, we look up its value
    # in the symbol table and return it.
    try:
        value = float(value)
    except ValueError:
        value = symbol_table.get(value)

    return value


def main():
    # Debug
    #print(tokenize(input('Tokens: '), '+-*/=()', " \t"))
    #print(lexer(tokenize(input("Tokens: "), '+-*/=()', " \t")))
    #print(to_postfix(input("Infix expr: ")))

    symbol_table: Dict[str,float] = dict()
    while True:
        try:
            expression = input('>>> ')
        except EOFError:
            print()
            break

        if expression[0] == '#':
            # Comment line.  Print it, and ignore it.
            print(expression)
            continue

        postfix: List[Tuple[str,Any]] = to_postfix(expression)
        value: float = eval_postfix(postfix, symbol_table)
        print (value)


if __name__ == '__main__':
    main()


