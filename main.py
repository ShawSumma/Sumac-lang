import re


class Token:
    def __init__(self, type, match):
        global code
        global col
        if isinstance(match, str):
            end_pos = len(match)
        else:
            end_pos = match.span()[1]
        self.raw_data = code[:end_pos]
        if self.raw_data in keywords:
            type = 'keyword'
        self.type = type
        self.line = line
        col += end_pos
        code = code[end_pos:]

    def __str__(self):
        return 'token({}) : {}'.format(self.type, self.raw_data)
    __repr__ = __str__


def view_tokens(tokens):
    for i in tokens:
        print(i)


def macro(code):
    global defined
    pl = 0
    while pl < len(code):
        if code[pl] == '`':
            original_pl = pl
            pl += 1
            mat = ''
            while pl < len(code) and code[pl] != '`':
                code = code
                mat += code[pl]
                pl += 1

            if mat.startswith('include'):
                fopen = open(mat[len('include')+1:])
                new_code = fopen.read()
                fopen.close()
                new_code = macro(new_code)
                code = code[:original_pl]+new_code+code[pl+1:]

            elif mat.startswith('define'):
                to_define = mat.split()[1]
                set_to = mat[8+len(to_define):]
                if set_to != '':
                    defined[to_define] = set_to
                else:
                    defined[to_define] = 'Empty Definition'
                code = code[:original_pl]+code[pl+1:]

            elif mat.startswith('undefine'):
                to_define = mat.split()[1]
                set_to = mat[7+len(to_define):]
                if to_define in defined:
                    del defined[to_define]
                code = code[:original_pl]+code[pl+1:]

            elif mat.startswith('print'):
                print_out = mat.split()[1]
                if print_out == '*':
                    for i in defined:
                        print(i, ':', defined[i])
                elif print_out in defined:
                    print(print_out, ':', defined[print_out])
                else:
                    print(print_out, ': Not defined')
                code = code[:original_pl]+code[pl+1:]

            elif mat.startswith('putstr'):
                print(mat[7:])
                code = code[:original_pl]+code[pl+1:]

            elif mat.startswith('if'):
                perams = mat.split()[1:]
                invert = perams[0] == 'not'
                if invert:
                    perams = perams[1:]
                if perams[0] == 'defined':
                    cond = perams[1] in defined
                elif perams[0] == 'equal':
                    if perams[2] != 'expr':
                        if perams[1] in defined:
                            var_pre = defined[perams[1]]
                        else:
                            var_pre = None
                        if perams[2] in defined:
                            var_post = defined[perams[2]]
                        else:
                            var_post = None
                        cond = var_pre == var_post
                else:
                    exit()
                if invert:
                    cond = not cond
                code = code[:original_pl]+code[pl+1:]
                depth = 1
                interm = ''
                while depth > 0:
                    if code[original_pl:].startswith('`if'):
                        depth += 1
                    elif code[original_pl:].startswith('`end if'):
                        depth -= 1
                    interm += code[original_pl+1]
                    code = code[:original_pl]+code[original_pl+1:]
                interm = interm[:-2]
                if cond:
                    # print('--now interm--')
                    # print(interm)
                    # print('--end interm--')
                    interm = macro(interm)
                else:
                    interm = ''
                pre = code[:original_pl]
                post = code[original_pl:]
                code = pre+interm+post[7:]
            pl = original_pl
        elif code[pl] in '\"\'':
            cpl = code[pl]
            pl += 1
            while pl < len(code) and code[pl] != cpl:
                pl += 1
        pl += 1
    # print('--now code--')
    # print(code)
    # print('--end code--')
    return code


def tokenize(file):
    global code
    global line
    global col
    global keywords
    global defined
    defined = {}
    keywords = [
        'int',
        'char',
        'bool',
        'if',
        'while',
        'for',
        'loop',
        'else',
        'elif'
    ]
    code = macro(code)
    match_regexes = {
        'name': r'[a-zA-Z_]+[a-zA-Z]*',
        'int': r'[0-9]+',
        'float': r'([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)',
        'semicolon': r';',
    }
    compiled_regexes = {}
    for i in match_regexes:
        compiled_regexes[i] = re.compile(match_regexes[i])

    operators = ['+', '-', '*', '/', '^', '%', '&', '&&', '||', '<', '>',
                 '<=', '>=', '+=', '-=', '*=', '/=', '=', '==', '!=']
    operators.sort(key=lambda op: 100-len(op))

    brace_types = '{}()[]'
    brace_names = {
        '(': 'l paren',
        ')': 'r paren',
        '{': 'l curly',
        '}': 'r curly',
        '[': 'r list',
        ']': 'l list',
    }
    return_tokens = []
    line = 1
    col = 1
    while 1:
        end_flag = True
        while len(code) > 0 and code[0] in '\n\t ':
            if code[0] == '\n':
                line += 1
                col = 0
            code = code[1:]
            col += 1
        matches = {}
        if len(code) == 0:
            return return_tokens
        if code[0] in '\"\'':
            pl = 1
            while len(code) > pl and code[pl] not in '\"\'':
                pl += 1
            new_token = Token('string', code[:pl+1])
            return_tokens.append(new_token)
            end_flag = True
            continue

        if end_flag and code[0] in brace_types:
            return_tokens.append(Token(brace_names[code[0]], code[0]))
            end_flag = True
            continue

        if end_flag:
            for i in operators:
                if code[:len(i)] == i:
                    return_tokens.append(Token('operator', i))
                    end_flag = False
                    continue

        if end_flag:
            for i in compiled_regexes:
                matches[i] = compiled_regexes[i].match(code)

        if end_flag:
            for type in matches:
                if matches[type] is not None:
                    if type != 'name':
                        return_tokens.append(Token(type, matches[type]))
                    else:
                        span = matches['name'].span()[1]
                        data = code[:span]
                        if data in defined:
                            code = defined[data]+code[span:]
                        else:
                            return_tokens.append(Token(type, matches[type]))
                    end_flag = False
                    continue
        if end_flag:
            break
    print("lexer error")
    exit()


file = "source.txt"
code = open(file).read()
tokens = tokenize(code)
view_tokens(tokens)
