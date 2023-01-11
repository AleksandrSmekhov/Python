#Kata - https://www.codewars.com/kata/55bf01e5a717a0d57e0000ec

def persistence(n):
    if n < 10:
        return 0
    else:
        res = 1
        for val in str(n):
            res *= int(val)
        return 1 + persistence(res)