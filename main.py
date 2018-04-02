import re


class Token:
    def __init__(self, type, match):
        global code
        global col
<<<<<<< HEAD
=======
        # print(match)
>>>>>>> 0464c084babd6dd8e5eecf892a6d9017e9fa5726
        if isinstance(match, str):
            end_pos = len(match)
        else:
            end_pos = match.span()[1]
        self.raw_data = code[:end_pos]
<<<<<<< HEAD
=======
        keywords = ['int', 'char', 'bool', 'if', 'while', 'for', 'loop',
                    'else', 'elif']
>>>>>>> 0464c084babd6dd8e5eecf892a6d9017e9fa5726
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
<<<<<<< HEAD
                code = code
                mat += code[pl]
                pl += 1
=======
                # print(code[pl])
                code = code
                mat += code[pl]
                pl += 1
            # print(mat)
>>>>>>> 0464c084babd6dd8e5eecf892a6d9017e9fa5726
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
<<<<<<< HEAD
        'semicolon': r';',
=======
        # 'operator': r'[+-*/!&<>^%]+ '
        # Make a list containing the types later
>>>>>>> 0464c084babd6dd8e5eecf892a6d9017e9fa5726
    }
    compiled_regexes = {}
    for i in match_regexes:
        compiled_regexes[i] = re.compile(match_regexes[i])

    operators = ['+', '-', '*', '/', '^', '%', '&', '&&', '||', '<', '>',
                 '<=', '>=', '+=', '-=', '*=', '/=', '=', '==', '!=']
    operators.sort(key=lambda op: 100-len(op))

    brace_types = '\{\}()[]'
    brace_names = {
        '(': 'l paren',
        ')': 'r paren',
        '{': 'l curly',
        '}': 'r curly',
        '[': 'r list',
        ']': 'l list',
    }
<<<<<<< HEAD
    return_tokens = []
    line = 1
    col = 1
    while 1:
=======
    # print(compiled_regexes)
    return_tokens = []
    line = 1
    col = 1
    # loop until no tokens
    while 1:
        # print(code)
>>>>>>> 0464c084babd6dd8e5eecf892a6d9017e9fa5726
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

<<<<<<< HEAD
        if end_flag and code[0] in brace_types:
=======
        if code[0] in brace_types:
>>>>>>> 0464c084babd6dd8e5eecf892a6d9017e9fa5726
            return_tokens.append(Token(brace_names[code[0]], code[0]))
            end_flag = True
            continue

        if end_flag:
            for i in operators:
<<<<<<< HEAD
=======
                # print(i,[code[:len(i)],i],code[:len(i)] == i)
>>>>>>> 0464c084babd6dd8e5eecf892a6d9017e9fa5726
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
<<<<<<< HEAD
=======
                    # print('found a match')
>>>>>>> 0464c084babd6dd8e5eecf892a6d9017e9fa5726
                    return_tokens.append(Token(type, matches[type]))
                    end_flag = False
                    continue
        if end_flag:
            break
    print("lex er on line %s at col %s" % (line, col))
    exit()


<<<<<<< HEAD
file = "source.txt"
code = open(file).read()
tokens = tokenize(code)
=======
tokens = tokenize('source.txt')
>>>>>>> 0464c084babd6dd8e5eecf892a6d9017e9fa5726
view_tokens(tokens)
