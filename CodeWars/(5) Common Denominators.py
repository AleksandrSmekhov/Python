#Kata - https://www.codewars.com/kata/54d7660d2daf68c619000d95

from math import gcd

def convert_fracts(lst):
    LCM = 1
    for numerator, denominator in lst:
        LCM *= denominator // gcd(LCM, denominator)
    
    return [[numerator * (LCM // denominator), LCM] for numerator, denominator in lst]