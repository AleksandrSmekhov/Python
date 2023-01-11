#Kata - https://www.codewars.com/kata/56747fd5cb988479af000028

def get_middle(s):
    half_len = len(s) // 2
    return s[half_len] if len(s) % 2 == 1 else s[half_len - 1 : half_len + 1]