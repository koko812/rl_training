grid = [0]*9
win_grids = [
            [1,1,1,0,0,0,0,0,0],
            [0,0,0,1,1,1,0,0,0],
            [0,0,0,0,0,0,1,1,1],
            [1,0,0,1,0,0,1,0,0],
            [0,1,0,0,1,0,0,1,0],
            [0,0,1,0,0,1,0,0,1],
            [1,0,0,0,1,0,0,0,1],
            [0,0,1,0,1,0,1,0,0],
            ]

def is_filled():
    filled = True
    for col in grid:
        if col == 0:
            filled = False
            break
    return filled

def game_result():
    for wg in win_grids:
        total = sum([c * w for c,w in zip(grid, wg)])
        if abs(total)==3:
            return total//3
    return 0

def get_gohote(grid):
    open_math = [i for i in range(len(grid)) if grid[i]==0]
    return open_math

turn = 0
states = [] 
koma = {1:"X", -1:"O", 0:"."}
while not is_filled():
    states.append((grid.copy(), turn))
    open_math = get_gohote(states[-1])
    print(f"open is {open_math}")
    num = input("input row, col as 12: ")
    r = int(num[0])
    c = int(num[1])
    grid[r*3+c]=turn%2*2-1
    for i in range(3):
        print(" ".join([koma[grid[3*i+j]] for j in range(3)]))

    if game_result() != 0: 
        print(f"the winner is {koma[turn%2*2-1]}")
        break

    turn+=1
