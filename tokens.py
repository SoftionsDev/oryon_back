import ply.lex as lex

tokens = (
   'WORD',
   'LESS_THAN',
   'GREATER_THAN',
   'LESS_EQUAL',
   'GREATER_EQUAL',
   'EQUALS',
   'NUMBER',
   'AND',
   'OR'
)

# Regular expression rules for simple tokens
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_EQUALS = r'='
t_AND = r'and'
t_OR = r'or'

# Regular expression rule with some action code (for numbers)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convert string to an integer
    return t

# Define a rule for words (alphanumeric sequences)
def t_WORD(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    import pdb; pdb.set_trace()
    next_space = t.lexer.lexdata.find(' ', t.lexer.lexpos)
    if next_space == -1:  # No space found, skip to the end of the string
        next_space = len(t.lexer.lexdata)

    # Print error message with the entire unrecognized token
    print(f"Illegal sequence '{t.lexer.lexdata[t.lexer.lexpos:next_space]}'")

    # Skip the entire unrecognized token
    t.lexer.skip(next_space - t.lexer.lexpos)
