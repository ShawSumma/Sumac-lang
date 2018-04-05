import lex
import variable


def use_var(name):
    if name in name_types:
        return name_types[name]
    variable.notFound(name, name_types)
    # print('varriable not found', name)
    exit()


def compile_all(tree):
    global compiled
    global ctabs
    global imported
    ctabs = 0
    compiled = ''
    for header in imported:
        compiled += "#include "+header
    compiled += 'int main(){\n'
    tree.to_c()
    compiled += '}'
    return compiled


def view_single(to, tabs, name):
    if isinstance(to, lex.Token):
        print('       '*tabs+' '+name+' : '+str(to))
    elif isinstance(to, list):
        for pl, i in enumerate(to):
            view_single(i, tabs, 'list')
    else:
        print('       '*tabs+' '+name+' is next')
        to.display(tabs=tabs)


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
        print('       '*tabs+' code : '+self.type+' : '+str(len(self.code)))
        for i in self.code:
            i.display(tabs=tabs+1)
            print('       '*(tabs+1))

    def to_c(self):
        global ctabs
        ctabs += 1
        for i in self.code:
            i.to_c()
        ctabs -= 1


class T_line:

    def __init__(self, tokens):
        code = tokens
        self.code = code
        self.type = code.type

    def display(self, tabs):
        view_single(self.code, tabs, ' code')

    def __str__(self):
        return str(self.tokens)

    __repr__ = __str__

    def to_c(self):
        self.code.to_c()


class T_none:
    def __init__(self):
        pass

    def display(self, *tabs):
        pass


class T_function:
    def __init__(self, name, perams):
        self.name = name
        self.perams = perams

    def display(self, tabs):
        view_single(self.name, tabs, 'name')
        self.perams.display(tabs)

    def to_c(self):
        pass


class T_token:

    def __init__(self, token):
        self.data = token.raw_data
        self.raw_data = self.data
        self.type = token.type
        self.token = token

    def __str__(self):
        return str(self.data)

    def display(self, tabs):
        print('       '*tabs+' '+str(self.token))

    def to_c(self):
        return self.raw_data

    __repr__ = __str__


class Chain_op:
    name = 'None'

    def __init__(self, *chain):
        self.chain = chain

    def display(self, tabs):
        print('       '*tabs+'  op   : '+self.name)
        for pl, i in enumerate(self.chain):
            view_single(i, tabs+1, 'chain '+str(pl))


class Three_op:
    name = 'None'

    def __init__(self, pre, post, cond):
        self.pre = pre
        self.post = post
        self.cond = cond

    def display(self, tabs):
        print('       '*tabs+'  op   : '+self.name)
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
        print('       '*tabs+'  op   : '+self.name)
        view_single(self.pre, tabs+1, 'pre ')
        view_single(self.post, tabs+1, 'post')


class One_op:
    name = 'None'

    def __init__(self, post):
        self.type = post.type
        self.post = post
        self.set_type()

    def set_type(self):
        self.type = self.post.type

    def display(self, tabs):
        print('       '*tabs+'op   : '+self.name)
        view_single(self.post, tabs+1, 'post ')


class T_return(One_op):
    name = 'return'

    def display(self, tabs):
        print('       '*tabs+'return :')
        view_single(self.post, tabs+1, 'post ')

    def to_c(self):
        global compiled
        compiled += '\t'*ctabs + 'return ' + self.post.to_c() + ';\n'
        return ''


class Ops:
    class Add(Two_op):
        name = 'add'

        def to_c(self):
            return "{0} + {1}".format(self.pre.to_c(), self.post.to_c())

    class Mul(Two_op):
        name = 'multiply'

        def to_c(self):
            return "{0} * {1}".format(self.pre.to_c(), self.post.to_c())

    class Sub(Two_op):
        name = 'subtract'

        def to_c(self):
            return "{0} * {1}".format(self.pre.to_c(), self.post.to_c())

    class Div(Two_op):
        name = 'devide'

        def to_c(self):
            return "{0} / {1}".format(self.pre.to_c(), self.post.to_c())

    class Pow(Two_op):
        name = 'raise to'

        def to_c(self):
            imported.append("<math.h>")
            return "pow({0}, {1})".format(self.pre.to_c(), self.post.to_c())

    class Mod(Two_op):
        name = 'modulo'

        def to_c(self):
            return "{0} % {1}".format(self.pre.to_c(), self.pos.to_c())

    class Not_greater_than(Two_op):
        name = 'less than or equal'

        def to_c(self):
            return "{0} <= {1}".format(self.pre.to_c(), self.post.to_c())

    class Not_less_than(Two_op):
        name = 'greater than or equal'

        def to_c(self):
            return "{0} >= {1}".format(self.pre.to_c(), self.post.to_c())

    class Greater_than(Two_op):
        name = 'greater than'

        def to_c(self):
            return "{0} > {1}".format(self.pre.to_c(), self.post.to_c())

    class Less_than(Two_op):
        name = 'less than'

        def to_c(self):
            return "{0} < {1}".format(self.pre.to_c(), self.post.to_c())

    class Not_equal(Two_op):
        name = 'not equal to'

        def to_c(self):
            return "{0} != {1}".format(self.pre.to_c(), self.post.to_c())

    class Equal(Two_op):
        name = 'euqal to'

        def to_c(self):
            return "{0} == {1}".format(self.pre.to_c(), self.post.to_c())

    class And(Two_op):
        name = 'and'

        def to_c(self):
            return "{0} && {1}".format(self.pre.to_c(), self.post.to_c())

    class Or(Two_op):
        name = 'Or'

        def to_c(self):
            return "{0} || {1}".format(self.pre.to_c(), self.post.to_c())

    class Not(One_op):
        name = 'not'

        def to_c(self):
            return "!{1}".format(self.post.to_c())

    class Negate(One_op):
        name = 'negate'

        def to_c(self):
            return "-{1}".format(self.post.to_c())

    class Pointer(One_op):
        name = 'pointer'

        def to_c(self):
            return "*{1}".format(self.post.to_c())

    class Address_of(One_op):
        name = 'address of'

        def to_c(self):
            return "&{1}".format(self.post.to_c())

    class Set_equal(Two_op):
        name = 'set equal to'

        def to_c(self):
            global compiled
            typeof = name_types[self.pre.data]
            compiled += '\t'*ctabs
            compiled += typeof+" {0} = {1};".format(self.pre.to_c(),
                                                    self.post.to_c())
            compiled += '\n'

    class Set_add(Two_op):
        name = 'set and add'

        def to_c(self):
            global compiled
            typeof = name_types[self.pre.data]
            compiled += '\t'*ctabs
            compiled += typeof+" {0} += {1};".format(self.pre.to_c(),
                                                     self.post.to_c())
            compiled += '\n'

    class Set_sub(Two_op):
        name = 'set and subtract'

        def to_c(self):
            global compiled
            typeof = name_types[self.pre.data]
            compiled += '\t'*ctabs
            compiled += typeof+" {0} -= {1};".format(self.pre.to_c(),
                                                     self.post.to_c())
            compiled += '\n'

    class Set_mul(Two_op):
        name = 'set and multiply'

        def to_c(self):
            global compiled
            typeof = name_types[self.pre.data]
            compiled += '\t'*ctabs
            compiled += typeof+" {0} *= {1};".format(self.pre.to_c(),
                                                     self.post.to_c())
            compiled += '\n'

    class Set_div(Two_op):
        name = 'set and devide'

        def to_c(self):
            global compiled
            typeof = name_types[self.pre.data]
            compiled += '\t'*ctabs
            compiled += typeof+" {0} /= {1};".format(self.pre.to_c(),
                                                     self.post.to_c())
            compiled += '\n'


imported = []
name_types = {}
function_types = {
    'int': 'int',
    'str': 'str',
}
