from lex import tokenize
from tree import tree
file = "source.txt"
code = open(file).read()
tokens = tokenize(code)
# view_tokens(tokens)
ast = tree(tokens)
ast.display()
