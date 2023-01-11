#Kata - https://www.codewars.com/kata/578aa45ee9fd15ff4600090d

def sort_array(source_array):
    odd_array = sorted([value for value in source_array if value % 2 == 1], reverse = True)
    return [odd_array.pop() if value % 2 == 1 else value for value in source_array]