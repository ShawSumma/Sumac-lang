from lex import tokenize
import tree
file = "source.txt"
code = open(file).read()
tokens = tokenize(code)
# view_tokens(tokens)
ast = tree.tree(tokens)
ast.display()
print(tree.name_types)
