#Kata - https://www.codewars.com/kata/55983863da40caa2c900004e

def next_bigger(n):
    str_n = str(n)
    max_n = int(''.join(sorted(str_n, reverse = True)))
    if max_n == n:
         return -1
    else:
        for i in range(len(str_n) - 2, -1, -1):
            if str_n[i] < str_n[i + 1]:
                b = ''.join(sorted(str_n[i:]))
                ind_b = b.rindex(str_n[i]) + 1
                return int(str_n[:i] + b[ind_b] + b[:ind_b] + b[ind_b + 1:])