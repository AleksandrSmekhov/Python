#Kata - https://www.codewars.com/kata/550498447451fbbd7600041c

def comp(a, b):
    try:
        return sorted([i ** 2 for i in a]) == sorted(b)
    except:
        return False