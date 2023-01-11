#Kata - https://www.codewars.com/kata/5287e858c6b5a9678200083c

def narcissistic( value ):
    return True if sum([int(v) ** len(str(value)) for v in str(value)]) == value else False