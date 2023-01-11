#Kata - https://www.codewars.com/kata/5672682212c8ecf83e000050

def dbl_linear(n):
    u = [1]
    x, y = 0, 0
    for i in range(n):
        nextX = 2 * u[x] + 1
        nextY = 3 * u[y] + 1
        if (nextX <= nextY):
            u.append(nextX)
            x += 1
            if nextX == nextY:
                y += 1
        else:
            u.append(nextY)
            y += 1
    return u[n]