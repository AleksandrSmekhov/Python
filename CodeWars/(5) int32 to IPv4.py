#Kata - https://www.codewars.com/kata/52e88b39ffb6ac53a400022e

def int32_to_ip(int32):
    return '{}.{}.{}.{}'.format(*int32.to_bytes(4, 'big'))