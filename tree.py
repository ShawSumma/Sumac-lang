import lex
from llvm_ops import Ops


class T_code:

    def __init__(self, code, type='code'):
        while [] in code:
            del code[code.index([])]
        ret = []
        for i in code:
            # print(i)
            ret.append(T_line(i))
        # print(ret)
        self.code = ret
        self.type = type

    def display(self, *tabs):
        if len(tabs) == 0:
            tabs = 0
        else:
            tabs = tabs[0]
        print('      |'*tabs+' code : '+self.type+' : '+str(len(self.code)))
        for i in self.code:
            i.display(tabs=tabs+1)
            print('      |'*(tabs+1))

    def to_llvm(self):
        pass


class T_line:

    def __init__(self, tokens):
        code = tree_expr(tokens)
        self.code = code

    def display(self, tabs):
        self.code.display(tabs)

    def __str__(self):
        return str(self.tokens)

    __repr__ = __str__

    def to_llvm(self):
        pass

def pair(list, items):
    ret = {}
    hold = {}
    depth = 0
    for pl, i in enumerate(list):
        if i.raw_data == items[0]:
            depth += 1
            hold[depth] = pl
        if i.raw_data == items[1]:
            ret[hold[depth]] = pl
            depth -= 1
    return ret


def tree_expr(tokens):
    types = []
    datas = []
    for token in tokens:
        if isinstance(token, lex.Token):
            types.append(token.type)
            datas.append(token.raw_data)
        else:
            types.apepnd('unknown')
            datas.append(token)
    if 'operator' in types:
        ord_ops = []
        ord_ops.append(['&&', '||'])
        ord_ops.append(['<=', '>=', '<', '>'])
        ord_ops.append(['!=', '=='])
        ord_ops.append(['+', '-'])
        ord_ops.append(['*', '/'])
        ord_ops.append(['**'])
        ord_ops.append(['error'])
        # ord_ops = ord_ops[::-1]
        found = False
        for order in ord_ops:
            for data in datas:
                if data in order:
                    found = True
                    break
            if found:
                break
        else:
            print('unknown operator')
            exit()
        index = datas.index(data)
        pre = tokens[:index]
        post = tokens[index+1:]
        pre = tree_expr(pre)
        post = tree_expr(post)
        ops_map = {
            '+': Ops.Add,
            '*': Ops.Mul,
            '-': Ops.Sub,
            '/': Ops.Div,
            '**': Ops.Pow,
            '&&': Ops.And,
            '||': Ops.Sub,
            '>=': Ops.Not_less_than,
            '<=': Ops.Not_greater_than,
            '>': Ops.Greater_than,
            '<': Ops.Less_than,
            '!=': Ops.Not_equal,
            '==': Ops.Equal,
        }
        return ops_map[data](pre, post)
    if len(tokens) == 1:
        return tokens[0]


def tree(tokens, break_upon='semicolon'):
    curly_mat = pair(tokens, ['{', '}'])
    paren_mat = pair(tokens, ['(', ')'])
    list_mat = pair(tokens, ['[', ']'])
    # print(curly_mat)
    types = []
    for i in tokens:
        if isinstance(i, lex.Token):
            types.append(i.type)
        else:
            types.append(None)
    ret = [[]]
    pl = 0
    while pl < len(tokens):
        cur = types[pl]
        if cur == 'l curly':
            cur = tree(tokens[pl+1:curly_mat[pl]])
            ret[-1].append(cur)
            pl = curly_mat[pl]
            pass
        elif cur == 'l paren':
            # cur = tree(tokens[pl+1:paren_mat[pl]], break_upon='comma')
            cur = tokens[pl+1:paren_mat[pl]]
            cur = tree(cur, break_upon='comma')
            ret[-1].append(cur)
            pl = paren_mat[pl]
            pass
        elif cur == 'l list':
            cur = tree(tokens[pl+1:list_mat[pl]], break_upon='comma')
            ret[-1].append(cur)
            pl = list_mat[pl]
            pass
        elif cur == break_upon:
            ret.append([])
        else:
            ret[-1].append(tokens[pl])
        pl += 1
        # print(pl, i)
    # print(ret)
    type = 'code' if break_upon == 'semicolon' else 'tuple'
    ret = T_code(ret, type)
    return ret
