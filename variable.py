import difflib


def notFound(name, options):
    maxerr = len(name)
    best = None
    for option in options:
        err = 0
        for pl, i in enumerate(difflib.ndiff(name, option)):
            if i[0] == '+':
                err += 1
            if i[0] == '-':
                err += 1
        if err <= maxerr:
            maxerr = err
            best = option
    print(name, 'not found perhaps you meant', best)
