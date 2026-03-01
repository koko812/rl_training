import random
import math
import statistics

GAME_EPOCH = 100
GAME_LEN = 100
probs = [0.3, 0.5, 0.9]
random.shuffle(probs)
#print(probs)

def reward_func(input_num, probs):
    prob = probs[input_num]
    rand = random.random()
    if prob > rand:
        return 1
    else:
        return 0

def softmax(arr):
    sum = 0
    ret_arr = []
    for a in arr:
        sum += math.exp(a)
    
    for a in arr:
        ret_arr.append(a/sum)

    return ret_arr


def policy(mode):
    if mode=="player":
        while True:
            try:
                input_num = int(input(f"turn{i+1}: input 0,1,2: "))
                if input_num < 0 or input_num > 2:
                    raise ValueError
            except ValueError:
                print("invalid_value: input 0,1,2")
                continue
            except Exception as e:
                print(f"{e}: input 0,1,2")
            break

        return input_num

    elif mode =="agent":
        policy_logits = [1,1,1]
        policy_probs = softmax(policy_logits)
        # reward が帰ってこないとどうしようもないです．
        # ただ，player とロジックを分けたくないです．
        # reward を誰に持たせるんだ？
        
    else:
        return random.randint(0,2)


game_totals = []
for a in range(GAME_EPOCH):
    game_total = 0
    for i in range(GAME_LEN):
        input_num = policy("player")
        reward = reward_func(input_num, probs)
        game_total += reward
        print(f"turn {i+1}: reward = {reward},  game_total = {game_total}")
    print("\ngame_end")
    print(f"game_total = {game_total}")
    game_totals.append(game_total)


print("\n---- over results -----")
print(statistics.mean(game_totals))
print(statistics.variance(game_totals))
print(statistics.stdev(game_totals))