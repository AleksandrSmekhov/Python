#Kata - https://www.codewars.com/kata/52597aa56021e91c93000cb0

def move_zeros(lst):
    a = [x for x in lst if x != 0]
    return a + [0] * (len(lst) - len(a))