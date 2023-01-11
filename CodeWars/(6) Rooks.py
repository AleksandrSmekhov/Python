#kata - https://www.codewars.com/kata/5bc2c8e230031558900000b5

def rooks(n, k):
    if k == 0:
        return 1
    elif k > n:
        return 0
    else:
        result = 1
        for i in range(k):
            result *= ((n - i) ** 2) / (i + 1)
        return int(result)