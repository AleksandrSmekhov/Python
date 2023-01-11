#Kata - https://www.codewars.com/kata/529bf0e9bdf7657179000008

def valid_solution(board):
    for row in board:
        if len(set(row)) < 9 or 0 in row:
            return False
        
    for column in zip(*board):
        if len(set(column)) < 9:
            return False
    
    for i in range(9):
        square = [board[(i // 3) * 3 + j][(i % 3) * 3 + k] for j in range(3) for k in range(3)]
        if len(set(square)) < 9:
            return False

    return True