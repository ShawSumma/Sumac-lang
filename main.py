from lex import tokenize
import tree
from code_gen import compile_all
file = "source.txt"
code = open(file).read()
tokens = tokenize(code)
ast = tree.tree(tokens)
# ast.display()
c_code = compile_all(ast)
f = open('output.c', 'w').write(c_code)
# print(tree.name_types)
