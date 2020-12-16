import time
import random

n=0.7
number=0
wrong = False
num = 0
input1 = input2 = input1l = input2l = 0
pick1 = pick2 = pick1p = pick2p = 0

row1 = [1,2,3,4]
row2 = [5,6,7,8]
list = []
rounds=0

for n in range(0,4):
    p = random.choice(row1)
    list.append(p)
    row1.remove(p)
    p = random.choice(row2)
    list.append(p)
    row2.remove(p)
    print(list)

startTime = time.time()

while not wrong:
    num = ((num + 1) % 2)
    pick1 = random.choice([list[num], list[num + 2]])
    input1 = input("\n"+ str(pick1) + " \n")

    pick1p = pick1

    list[list.index(pick1)] = list[5 - ((num + 1) % 2)]
    list[5 - ((num + 1) % 2)] = list[7 - ((num + 1) % 2)]
    list[7 - ((num + 1) % 2)] = pick1p

    rounds+=1
    if (str(input1) != str(pick1)):
        wrong = True


print("Rounds: " + str(rounds))
print("Time played: " + str(abs(time.time()-startTime)))
print()
print("Score: " + str(((rounds)/abs(time.time()-startTime))*400))

