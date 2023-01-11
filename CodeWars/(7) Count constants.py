#Kata - https://www.codewars.com/kata/564e7fc20f0b53eb02000106

def consonant_count(s):
    return sum([1 for x in s if x.lower() not in 'aeiou' and x.isalpha()])