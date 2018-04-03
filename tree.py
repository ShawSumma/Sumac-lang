import lex
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
        print('    |'*tabs+'code: '+self.type+' : '+str(len(self.code)))
        for pl,i in enumerate(self.code):
            i.display(tabs=tabs+1)
            print('    |'*(tabs+1))

class T_line:

    def __init__(self, tokens):
        self.tokens = tokens

    def display(self, tabs):
        for i in self.tokens:
            if isinstance(i, lex.Token):
                print('    |'*tabs+str(i))
            else:
                i.display(tabs+1)

    def __str__(self):
        return str(self.tokens)

    __repr__ = __str__


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


def invert_pair(list, items):
    ret = {}
    hold = {}
    depth = 0
    for pl, i in enumerate(list):
        if i.raw_data == items[0]:
            depth += 1
            hold[depth] = pl
        if i.raw_data == items[1]:
            ret[pl] = hold[depth]
            depth -= 1
    return ret


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
