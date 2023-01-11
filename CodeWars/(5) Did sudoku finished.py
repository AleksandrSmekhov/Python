#Kata - https://www.codewars.com/kata/53db96041f1a7d32dc0004d2

def done_or_not(board): 
    for row in board:
        if len(set(row)) < 9:
            return 'Try again!'
        
    for column in zip(*board):
        if len(set(column)) < 9:
            return 'Try again!'
    
    for i in range(9):
        square = [board[(i // 3) * 3 + j][(i % 3) * 3 + k] for j in range(3) for k in range(3)]
        if len(set(square)) < 9:
            return 'Try again!'

    return 'Finished!'