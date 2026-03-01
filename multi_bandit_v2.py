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
        ret_arr.append(math.exp(a)/sum)

    return ret_arr


policy_logits = [1,1,1]
policy_probs = [1,1,1]

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
        global policy_logits
        global policy_probs
        policy_probs = softmax(policy_logits)
        print(f"policy_probs: {policy_probs}")
        c = random.choices([0,1,2], policy_probs, k=1)
        return random.choices([0,1,2], policy_probs, k=1)[0]

    else:
        return random.randint(0,2)


lr = 0.8
def update(action, reward):
    global policy_logits
    global policy_probs
    
    grads = [0] * len(policy_logits)
    grads[action] = 1
    grads = [grads[i]-policy_probs[i] for i in range(len(policy_logits))]
    policy_logits = [policy_logits[i]+lr*reward*grads[i] for i in range(len(policy_logits))]
    

game_totals = []
mode = "agent"
for a in range(GAME_EPOCH):
    policy_logits = [1,1,1]
    policy_probs = [1,1,1]
    game_total = 0
    for i in range(GAME_LEN):
        action = policy(mode)
        reward = reward_func(action, probs)
        if mode=="agent":
            update(action, reward)
        game_total += reward
        print(f"turn {i+1}: reward = {reward},  game_total = {game_total}")
    print("\ngame_end")
    print(f"game_total = {game_total}")
    game_totals.append(game_total)


print("\n---- over results -----")
print(statistics.mean(game_totals))
print(statistics.variance(game_totals))
print(statistics.stdev(game_totals))