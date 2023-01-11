#Kata - https://www.codewars.com/kata/51c8e37cee245da6b40000bd

def strip_comments(strng, markers):
    lines = strng.split('\n')
    for marker in markers:
        lines = [line.split(marker)[0].rstrip() for line in lines]
    return '\n'.join(lines)