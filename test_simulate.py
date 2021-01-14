from simulate import Simulate
from itertools import combinations
from random import choices
import time

def get_probability_list(dice_size, dice_num, n=0, arr=None):
    if not arr:
        arr = [0]*(dice_size*dice_num + 1)

    if not dice_num:
        arr[n] += 1
        return arr

    for d in range(dice_size):
        get_probability_list(dice_size, dice_num - 1, n=n+d+1, arr=arr)
    return arr

def test_random_choice():
    weights = get_probability_list(6, 4)[4:]
    sums = [i for i in range(4, len(weights)+4)]
    results = [0]*25
    tmp = choices(sums, weights, k=1000000)
    for i in tmp:
        results[i] += 1
    print(results)

def test_random_choice2():
    weights = get_probability_list(6, 2)[2:]
    sums = [i for i in range(2, len(weights)+2)]

    results = [0]*13
    for _ in range(10000):
        results[choices(sums, weights)[0]] += 1
    print(results)


def test_random_choice3():
    weights = get_probability_list(6, 4)
    sums = [i for i in range(len(weights))]

    results = [0]*25
    tmp = choices(sums, weights, k=1000000)
    for i in tmp:
        results[i] += 1
    print(results)

# rt = get_probability_list(6, 6)
# print(rt)

start = time.time()
test_random_choice()
print("Time:", time.time()-start)

print()
start = time.time()
test_random_choice3()
print("Time:", time.time()-start)


