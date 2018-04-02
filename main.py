import re

class Token:
    def __init__(self, type, match):
        global code
        #print(match)
        if isinstance(match,str):
            end_pos = len(match)
        else:
            end_pos = match.span()[1]
        self.raw_data = code[:end_pos]
        if self.raw_data in ['int','char','bool','if','while','for','loop','else','elif']:
            type = 'keyword'
        self.type = type
        self.line = line
        code = code[end_pos:]
    def __str__(self):
        return 'token({}) : {}'.format(self.type,self.raw_data)
    __repr__ = __str__

def view_tokens(tokens):
    for i in tokens:
        print(i)

def tokenize(file):
    global code
    global line
    code = open(file).read()

    match_regexes = {
        'name': r'[a-zA-Z_]+[a-zA-Z]*',
        'int': r'[0-9]+',
        'float': r'([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)',
        #'operator': r'[+-*/!&<>^%]+ ', # make a list containing the types later

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
    #print(compiled_regexes)
    return_tokens = []
    line = 1

    #loop until no tokens
    while 1:
        print(code)
        end_flag = True

        while len(code) > 0 and code[0] in '\n\t ':
            if code[0] == '\n':
                line += 1
            code = code[1:]
        matches = {}

        for i in operators:
            #print(i,[code[:len(i)],i],code[:len(i)] == i)
            if code[:len(i)] == i:
                return_tokens.append(Token('operator',i))
                end_flag = False
                continue
        if end_flag:
            for i in compiled_regexes:
                matches[i] = compiled_regexes[i].match(code)

        if end_flag:
            for type in matches:
                if matches[type] != None:
                    #print('found a match')
                    return_tokens.append(Token(type,matches[type]))
                    end_flag = False
                    continue

        if end_flag:
            break
    return return_tokens
tokens = tokenize('source.txt')
view_tokens(tokens)
