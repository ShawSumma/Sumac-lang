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
        view_single(self.pre, tabs+1, 'pre')
        view_single(self.cond, tabs+1, 'condition')
        view_single(self.post, tabs+1, 'post')


class Two_op:
    name = 'None'

    def __init__(self, pre, post):
        self.pre = pre
        self.post = post

    def display(self, tabs):
        print('      |'*tabs+' op   : '+self.name)
        view_single(self.pre, tabs+1, 'pre')
        view_single(self.post, tabs+1, 'post')


class One_op:
    name = 'None'

    def __init__(self, pre):
        self.pre = pre

    def display(self, tabs):
        print('      |'*tabs+'op   : '+self.name)
        view_single(self.pre, tabs+1, 'pre')


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
