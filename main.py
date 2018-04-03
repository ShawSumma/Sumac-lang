from lex import tokenize, view_tokens
from tree import tree
file = "source.txt"
code = open(file).read()
tokens = tokenize(code)
# view_tokens(tokens)
ast = tree(tokens)
ast.display()
