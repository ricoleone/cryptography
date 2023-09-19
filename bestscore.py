import random

# given an array of numbers, return them sorted

def fitness(arr):
    score =0
    for i in range(len(arr)):
        for j in range(i):
            if arr[j] < arr[i]:
                score +=1
    return score

ct = [random.randint(0, 100000) for i in range(100)]
random.shuffle(ct)
best_score = 0
prev_score = 0
best_run = 0
tg = ct.copy()
ct[0] = 1000
print(tg)
best_i = 0
best_j = 0
while best_run < 3:
    for i in range(len(tg)):
        for j in range(len(tg)):
            tmp = tg.copy()
            tmp[i] = tg[j]
            tmp[j] = tg[i]
            tmp_score = fitness(tmp)
            #print("tmp_score = ", tmp_score)
            if tmp_score > best_score:
                best_i = i
                best_j = j
                best_score = tmp_score
    temp = tg[best_i]
    tg[best_i] = tg[best_j]
    tg[best_j] = temp
    # print("tg[",best_i,"] = ", tg[best_i])
    # print("tg[",best_j,"] = ", tg[best_j])
    # print("best score = ", best_score)
    if best_score > prev_score:
        best_run = 0
        prev_score = best_score
    else:
        best_run +=1
print("best score = ", best_score)
print("previous score = ", prev_score)
print(tg)