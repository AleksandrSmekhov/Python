#Kata - https://www.codewars.com/kata/56b0bc0826814364a800005a

def cyclops (n):
    i = bin(n)[2:]
    return True if len(i) % 2 == 1 and i.count('0') == 1 and i[len(i) // 2] == '0' else False