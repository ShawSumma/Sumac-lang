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
                code = code[:original_pl]+new_code+code[pl+1:]
        elif code[pl] in '\"\'':
            cpl = code[pl]
            pl += 1
            while pl < len(code) and code[pl] != cpl:
                pl += 1
        pl += 1
    return code


def tokenize(file):
    global code
    global line
    global col
    global keywords
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
                    return_tokens.append(Token(type, matches[type]))
                    end_flag = False
                    continue
        if end_flag:
            break
    print("lex er on line %s at col %s" % (line, col))
    exit()


file = "source.txt"
code = open(file).read()
tokens = tokenize(code)
view_tokens(tokens)
