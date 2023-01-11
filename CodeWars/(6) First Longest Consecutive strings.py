#Kata - https://www.codewars.com/kata/56a5d994ac971f1ac500003e

def longest_consec(strarr, k):
    res = ''
    if k > 0 and k < len(strarr):
        for i in range(len(strarr) - k + 1):
            temp = "".join(strarr[i:i + k])
            if len(temp) > len(res):
                res = temp
    return res