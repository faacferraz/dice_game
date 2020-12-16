import time
import random

wrong = False
num = 0
input1 = input2 = input1l = input2l = 0
pick1 = pick2 = pick1p = pick2p = 0

row1 = [1,2,3]
row2 = [4,5,6]
row3 = [7,8,9]
list = []
rounds=0

for n in range(0,3):
    p = random.choice(row1)
    list.append(p)
    row1.remove(p)
    p = random.choice(row2)
    list.append(p)
    row2.remove(p)
    p = random.choice(row3)
    list.append(p)
    row3.remove(p)
    print(list)

startTime = time.time()

while not wrong:

    rounds+=1
    if (str(input1) != str(pick1)):
        wrong = True


print("Rounds: " + str(rounds))
print("Time played: " + str(abs(time.time()-startTime)))
print()
print("Score: " + str(((rounds)/abs(time.time()-startTime))*400))