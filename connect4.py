import random

row = 6
col = 7 
grid = [0]*row*col

def is_filled(state):
    filled = True
    grid = state[0]
    for i in grid:
        if i == 0:
            filled = False
            break

    return filled

def game_judge(state):
    # 4x4 のグリッドを作ってその中で判定をした方が楽だったのかもしれない
    # これは 3目並べにも言えるのか？この divide and conquer は普通に天才的かも
    grid = state[0]
    turn = state[1]
    done = False
    winner = 0
    # row
    for i in range(len(grid)):
        if i%col <= col-4:
            if abs(sum(grid[i:i+4])) == 4:
                winner = turn%2*2-1
                done = True
                break
    # col
    for i in range(len(grid)):
        if i/col <= row-4:
            if abs(sum([grid[j] for j in [i+7*k for k in range(4)]])) == 4:
                winner = turn%2*2-1
                done = True
                break

    # diagonal
    for i in range(len(grid)):
        if i%col <= col-4 and i/col <= row-4:
            # こういうきったない実装を駆逐したい，クソが．
            # 大体，7 とかを直接入れるのは，明らかにアウトで，row を使うとかの工夫が欲しい
            # あとは connect の数も抽象化できるようにするとか．
            # あと，上下の考え方がややこしくて，そこは脳に負荷がかかったので避けたいところ
            # これは多分他の落ちモノ系は全部同じことになると思う
            opp_sum = abs(sum([grid[j] for j in [i+7*k+k for k in range(4)]]))
            rev_sum = abs(sum([grid[j] for j in [i+7*(3-k)+k for k in range(4)]]))
            
            if opp_sum == 4 or rev_sum == 4:
                winner = turn%2*2-1
                done = True
                break

    if is_filled(state):
        done = True

    return done, winner

def get_gohote(state):
    grid = state[0]
    gohote = [i for i in range(col) if grid[col*(row-1)+i]==0]
    return gohote

def get_player_input(gohote):
    # ちょっと書き方がダサいので改善の余地ありだな
    while True:
        print(f"open is {gohote}")
        num = input("input row, col as 1 [0-6]: ")
        try:
            r = int(num)
        except Exception as e:
            print("invalid_input")
            continue

        if (r < 0 or 6 < r):
            print("out of grid")
            continue
        
        te = r

        if te in gohote:
            break
        else:
            print("can't put the math")

    return te

def policy(state, mode="player"):
    grid = state[0].copy()
    turn = state[1]
    gohote = get_gohote(state)

    if mode=="player":
        te = get_player_input(gohote)


    if mode=="random":
        te = random.choice(gohote)

    if mode=="itteyomi":
        pass

    return te
        

def disp(state):
    grid=state[0]
    turn=state[1]
    print(f"\n--- turn {turn} ---")
    for i in range(row):
        print(" ".join([koma[grid[(row-i-1)*col+j]] for j in range(col)]))


def step(state, action):
    grid=state[0].copy()
    turn=state[1]

    for i in range(row):
        if grid[i*col+action]==0:
            grid[i*col+action] = turn%2*2-1
            break

    next_state = (grid, turn+1)
    reward = 0
    done, winner = game_judge(next_state)
    return next_state, reward, done, winner

turn = 0
states = [] 
koma = {1:"X", -1:"O", 0:"."}
state = (grid, 0)
done = False

while not done:
    states.append(state)
    turn = state[1]
    if turn%2==0:
        action = policy(state, "random")
    else:
        action = policy(state, "random")

    next_state, reward, done, winner = step(state, action)
    state = next_state
    print(reward, done, winner)
    
    disp(state)

print("\n--- results ---")
if winner!=0:
    print(f"winner is {koma[winner*-1]}")
    print(f"total turn {turn+1}")
else:
    print("Draw")

# しかし，設計思想がちゃんとしてると，改変しやすい感じがしていいな．
# ぜひともこれを続けていきたい，というかいろんなパターンを覚えたい．