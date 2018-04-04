from lex import tokenize
import tree
file = "source.txt"
code = open(file).read()
tokens = tokenize(code)
# view_tokens(tokens)
ast = tree.tree(tokens)
ast.display()
c_code = tree.compile_all(ast)
f = open('output.c', 'w').write(c_code)
print(tree.name_types)
