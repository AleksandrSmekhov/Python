#Kata - https://www.codewars.com/kata/525f3eda17c7cd9f9e000b39

import operator

ops = {"+": operator.add,
       "-": operator.sub,
       "*": operator.mul,
       "/": operator.floordiv}

def zero(*args): return 0 if not len(args) else ops[args[0][0]](0,args[0][1])
def one(*args): return 1 if not len(args) else ops[args[0][0]](1, args[0][1])
def two(*args): return 2 if not len(args) else ops[args[0][0]](2, args[0][1])
def three(*args): return 3 if not len(args) else ops[args[0][0]](3, args[0][1])
def four(*args): return 4 if not len(args) else ops[args[0][0]](4, args[0][1])
def five(*args): return 5 if not len(args) else ops[args[0][0]](5, args[0][1])
def six(*args): return 6 if not len(args) else ops[args[0][0]](6, args[0][1])
def seven(*args): return 7 if not len(args) else ops[args[0][0]](7, args[0][1])
def eight(*args): return 8 if not len(args) else ops[args[0][0]](8, args[0][1])
def nine(*args): return 9 if not len(args) else ops[args[0][0]](9, args[0][1])

def plus(*args): return "+" , args[0]
def minus(*args): return "-" , args[0]
def times(*args): return "*" , args[0]
def divided_by(*args): return "/" , args[0]