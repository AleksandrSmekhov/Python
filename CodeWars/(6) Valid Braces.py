#Kata - https://www.codewars.com/kata/5277c8a221e209d3f6000b56

def valid_braces(string):
    while ("{}" in string) or ("[]" in string) or ("()" in string):
        string = string.replace("{}", "")
        string = string.replace("[]", "")
        string = string.replace("()", "")
    return string == ""