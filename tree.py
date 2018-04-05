import lex
from code_gen import Ops  # classes of classes
from code_gen import T_line, T_code, T_token, T_function, T_return  # class
from code_gen import use_var  # functions
from code_gen import name_types, function_types  # varaibles
# from code_gen import *


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


def fold_op(a, b, o):
    t = a.type
    if t == 'int' and a.raw_data.isnumeric() and b.raw_data.isnumeric():
        a, b = int(a.raw_data), int(b.raw_data)
        if o == '+':
            ret = a + b
        elif o == '*':
            ret = a * b
        elif o == '-':
            ret = a - b
        elif o == '/':
            ret = a / b
        elif o == '%':
            ret = a % b
        elif o == '**':
            ret = a ** b
        elif o == '>=':
            ret = a >= b
        elif o == '<=':
            ret = a <= b
        elif o == '<':
            ret = a < b
        elif o == '>':
            ret = a > b
        elif o == '!=':
            ret = a != b
        elif o == '==':
            ret = a == b
        else:
            return None
        return int(ret)
    else:
        return None


def tree_expr(tokens):
    types = []
    datas = []
    for token in tokens:
        if isinstance(token, lex.Token):
            types.append(token.type)
            datas.append(token.raw_data)
        else:
            types.append('unknown')
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
        if data in ['=', '+=', '-=', '/=', '*=']:
            prexist = pre.raw_data in name_types
            if prexist:
                old_type = name_types[pre.raw_data]
            if post.type != 'name':
                name_types[pre.raw_data] = post.type
            else:
                name_types[pre.raw_data] = use_var(post.raw_data)
            if prexist:
                if old_type != name_types[pre.raw_data]:
                    print(
                        'variable type miss match',
                        pre.raw_data,
                        'should be',
                        old_type,
                        'not',
                        name_types[pre.raw_data]
                    )
                    exit()
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
            '%': Ops.Mod,
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
        pre_type = type(pre)
        post_type = type(post)
        ret = ops_map[data](pre, post)
        if pre_type == post_type:
            fold = fold_op(pre, post, data)
            # print(fold)
            if fold is not None:
                ret = pre
                ret.raw_data = str(fold)
        return ret

    if len(tokens) == 1:
        if isinstance(tokens[0], T_code) and tokens[0].type == 'tuple':
            if len(tokens[0].code) == 1:
                return tokens[0].code[0]
        return T_token(tokens[0])

    if len(tokens) > 1:
        if isinstance(tokens[-1], T_code):
            if isinstance(tokens[-2], lex.Token):
                fn_name = tokens[-2].raw_data
            else:
                print(tokens[:-1])
            ret = T_function(tree_expr(tokens[:-1]), tokens[-1])
            ret.type = function_types[fn_name]
            return ret
        if isinstance(tokens[0], lex.Token):
            name = tokens[0].raw_data
            if name == 'ret':
                return T_return(tree_expr(tokens[1:]))
    print(tokens)
    print('--error in tree--')
    exit()


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
    type = 'code' if break_upon == 'semicolon' else 'tuple'
    while [] in ret:
        del ret[ret.index([])]
    code = ret
    ret = []
    for i in code:
        ret.append(T_line(tree_expr(i)))
    ret = T_code(ret, type)
    return ret
