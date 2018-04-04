import lex


def view_single(to, tabs, name):
    if isinstance(to, lex.Token):
        print('      |'*tabs+' '+name+' : '+str(to))
    elif isinstance(to, list):
        for pl, i in enumerate(to):
            view_single(i, tabs, 'list')
    else:
        print('      |'*tabs+name+' is next')
        to.display(tabs=tabs)


class Chain_op:
    name = 'None'

    def __init__(self, *chain):
        self.chain = chain

    def display(self, tabs):
        print('      |'*tabs+' op   : '+self.name)
        for pl, i in enumerate(self.chain):
            view_single(i, tabs+1, 'chain '+str(pl))


class Three_op:
    name = 'None'

    def __init__(self, pre, post, cond):
        self.pre = pre
        self.post = post
        self.cond = cond

    def display(self, tabs):
        print('      |'*tabs+' op   : '+self.name)
        view_single(self.pre, tabs+1, 'pre ')
        view_single(self.cond, tabs+1, 'cond')
        view_single(self.post, tabs+1, 'post')


class Two_op:
    name = 'None'

    def __init__(self, pre, post):
        self.pre = pre
        self.post = post
        self.set_type()

    def set_type(self):
        self.type = self.pre.type

    def display(self, tabs):
        print('      |'*tabs+' op   : '+self.name)
        view_single(self.pre, tabs+1, 'pre ')
        view_single(self.post, tabs+1, 'post')


class One_op:
    name = 'None'

    def __init__(self, pre):
        self.type = pre.type
        self.pre = pre
        self.set_type()

    def set_type(self):
        self.type = self.pre.type

    def display(self, tabs):
        print('      |'*tabs+'op   : '+self.name)
        view_single(self.pre, tabs+1, 'pre ')


class Ops:
    class Add(Two_op):
        name = 'add'

        def to_llvm(self):
            pass

    class Mul(Two_op):
        name = 'multiply'

        def to_llvm(self):
            pass

    class Sub(Two_op):
        name = 'subtract'

        def to_llvm(self):
            pass

    class Div(Two_op):
        name = 'devide'

        def to_llvm(self):
            pass

    class Pow(Two_op):
        name = 'raise to'

        def to_llvm(self):
            pass

    class Not_greater_than(Two_op):
        name = 'less than or equal'

        def to_llvm(self):
            pass

    class Not_less_than(Two_op):
        name = 'greater than or equal'

        def to_llvm(self):
            pass

    class Greater_than(Two_op):
        name = 'greater than'

        def to_llvm(self):
            pass

    class Less_than(Two_op):
        name = 'less than'

        def to_llvm(self):
            pass

    class Not_equal(Two_op):
        name = 'not equal to'

        def to_llvm(self):
            pass

    class Equal(Two_op):
        name = 'euqal to'

        def to_llvm(self):
            pass

    class And(Two_op):
        name = 'and'

        def to_llvm(self):
            pass

    class Or(Two_op):
        name = 'Or'

        def to_llvm(self):
            pass

    class Not(One_op):
        name = 'not'

        def to_llvm(self):
            pass

    class Negate(One_op):
        name = 'negate'

        def to_llvm(self):
            pass

    class Pointer(One_op):
        name = 'pointer'

        def to_llvm(self):
            pass

    class Address_of(One_op):
        name = 'address of'

        def to_llvm(self):
            pass

    class Set_equal(Two_op):
        name = 'set equal to'

        def to_llvm(self):
            pass

    class Set_add(Two_op):
        name = 'set and add'

        def to_llvm(self):
            pass

    class Set_sub(Two_op):
        name = 'set and subtract'

        def to_llvm(self):
            pass

    class Set_mul(Two_op):
        name = 'set and multiply'

        def to_llvm(self):
            pass

    class Set_div(Two_op):
        name = 'set and devide'

        def to_llvm(self):
            pass

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

class T_none:
    def __init__(self):
        pass

    def display(self, *tabs):
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


def use_var(name):
    if name in name_types:
        return name_types[name]
    print('varriable not found',name)


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
        ord_ops.append(['='])
        ord_ops.append(['+=', '-=', '*=', '/='])
        ord_ops.append(['&&', '||'])
        ord_ops.append(['<=', '>=', '<', '>'])
        ord_ops.append(['!=', '=='])
        ord_ops.append(['+', '-'])
        ord_ops.append(['*', '/'])
        ord_ops.append(['**'])
        ord_ops.append(['error'])

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
        if data in '=':
            name_types[pre.raw_data] = post.type

        math_ops = ['+', '-', '*', '/', '**']
        if data in math_ops:
            if pre.type == 'name':
                use_var(pre.raw_data)
                pre.type = name_types[pre.raw_data]
            if post.type == 'name':
                use_var(post.raw_data)
                post.type = name_types[post.raw_data]
            if pre.type != post.type:
                print('mismatch types on operator', data)
                print(pre.type, 'is not compatable with', post.type)
                exit()

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
            '=': Ops.Set_equal,
            '+=': Ops.Set_add,
            '-=': Ops.Set_sub,
            '*=': Ops.Set_mul,
            '/=': Ops.Set_div,
        }

        # set_ops = ['=', '-=', '*=', '/=', '+=']

        ret = ops_map[data](pre, post)
        return ret
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

name_types = {}
