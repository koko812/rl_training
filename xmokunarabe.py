import random

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


def is_filled(grid):
    filled = True
    for col in grid:
        if col == 0:
            filled = False
            break
    return filled

    
    
def game_result(grid):
    done = False
    winner = 0
    for wg in win_grids:
        total = sum([c * w for c,w in zip(grid, wg)])
        if abs(total)==3:
            winner = total//3
            done = True

    if is_filled(grid):
        done = True

    return (done, winner)


def get_gohote(grid):
    open_math = [i for i in range(len(grid)) if grid[i]==0]
    return open_math


def policy(state, mode):
    grid = state[0].copy()
    turn = state[1]
    gohote = get_gohote(grid)
    te = 0

    if mode=="player":
        while True:
            print(f"open is {gohote}")
            num = input("input row, col as 12: ")
            try:
                r = int(num[0])
                c = int(num[1])
            except:
                print("invalid_input")
                continue

            if (r < 0 or 2 < r) or (c < 0 or 2 < c):
                print("out of grid")
                continue
            
            te = r*3+c

            if te in gohote:
                break
            else:
                print("can't put the math")
        
                
    elif mode=="random":
        te = random.choice(gohote)
        #grid[te]=turn%2*2-1

    return te


def step(state, action):
    grid = state[0].copy()
    turn = state[1]
    winner = 0
    reward = 0

    grid[action] = turn%2*2-1
    turn += 1

    next_state = (grid, turn)
    done, winner = game_result(grid)

    if winner != 0:
        reward = 1
    
    return next_state, reward, done, winner
        

turn = 0
grid = [0]*9
states = [] 
koma = {1:"X", -1:"O", 0:"."}
state = (grid, 0)
done = False


while not done:
    states.append(state)
    print(f"--- turn {turn+1} ---")

    if turn%2 == 0:
        action = policy(state, "player")
    else:
        action = policy(state, "random")

    next_state, reward, done, winner = step(state, action)
    state = next_state

    for i in range(3):
        print(" ".join([koma[state[0][3*i+j]] for j in range(3)]))


    turn+=1

if winner != 0:
    print(f"the winner is {koma[winner]}")
print("states:")
print(states)
