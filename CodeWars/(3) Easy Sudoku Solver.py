#Kata - https://www.codewars.com/kata/5296bc77afba8baa690002d7

def sudoku(puzzle):
    correct = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    zeros = [[i, j] for i in range(9) for j in range(9) if puzzle[i][j] == 0]
    
    while 0 in sum(puzzle, []):
        for zero in zeros:
            impos_val = []
            for x in puzzle[zero[0]]:
                if x != 0:
                    impos_val.append(x)
            for i in range(9):
                if puzzle[i][zero[1]] != 0:
                    impos_val.append(puzzle[i][zero[1]])
            square = [puzzle[(zero[0] // 3) * 3 + j][(zero[1] // 3) * 3 + k] for j in range(3) for k in range(3)]
            for x in square:
                if x !=0:
                    impos_val.append(x)
                    
            pos_vals = correct - set(sorted(impos_val))
            if len(pos_vals) == 1:
                zeros.remove(zero)
                puzzle[zero[0]][zero[1]] = pos_vals.pop()
                
    return puzzle