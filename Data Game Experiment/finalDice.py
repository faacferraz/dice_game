import random
import operator

def percent(a,b):
    if a>b:
        return round((100*a/b)-100,2)
    if a<b:
        return round((100*b/a)-100,2)
    if a==b:
        return 100


# Defining the function game() to determine the winner between two "players" with the specified game conditions
def game(pl1, pl2, rollTimes, dieNum, dieVal, tieCount):
    player1 = pl1[:]
    player2 = pl2[:]
    p1 = player1[:]
    p2 = player2[:]
    p1Win = p2Win = 0

    for n in range(0, rollTimes):
        sumDie = 0
        for n in range(0,dieNum):
            sumDie+=random.randint(1,dieVal)

        if (sumDie) in player1:
            player1.remove(sumDie)

        if (sumDie) in player2:
            player2.remove(sumDie)

        if not player1 and not player2:  # Tie
            player1 = p1[:]     # "Reset the board"
            player2 = p2[:]
            if tieCount:        # Only in case tieCount is on, we would add 1 win to each player in case there is a tie
                p2Win += 1
                p1Win += 1

        elif not player1:       # If it was not a tie and player1 is empty, Player 1 one!
            player1 = p1[:]
            player2 = p2[:]     # "Reset the board"
            p1Win += 1          # Add 1 to Player 1 Wins

        elif not player2:       # Same thing for Player 2
            player1 = p1[:]
            player2 = p2[:]
            p2Win += 1

    # Returning the result of the winner
    if percent(p1Win, p2Win) <= 5:
        return "too close"
    elif p1Win > p2Win:
        return "Player 1"
    elif p2Win > p1Win:
        return "Player 2"
    else:
        return str(percent(p1Win, p2Win))



print("\nOnly two dice from 1-6")
print("Pick your numbers (type 0 to stop).")


dieVal = 6
dieNum = int(input("Number of dice (1 to 5): "))
maxSum = dieNum*dieVal
numNum = int(input("Number of numbers to pick (from " + str(dieNum) + " to " + str(maxSum) + "): "))
#rollTimes = int(input("Roll each dice how many times? (Recommended = 1000000, more for bigger games):"))
print("One second!\n")

maxSum = dieNum*dieVal
numSums = maxSum - dieNum
dictSums = {} #dictionary to keep track of how many times each of the sums happen
dictProb = {}

numComb=dieVal**dieNum
if dieNum == 1:
    probList = [1, 1, 1, 1, 1, 1]
    nH=3
elif dieNum == 2:
    probList = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
    nH=7
elif dieNum == 3:
    probList = [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 5, 3, 1]
    nH=10
elif dieNum == 4:
    probList = [1, 4, 10, 20, 35, 56, 80, 104, 125, 140, 146, 140, 125, 104, 80, 56, 35, 20, 10, 4, 1]
    nH=14
elif dieNum == 5:
    probList = [1, 5, 15, 35, 70, 126, 205, 305, 420, 540, 651, 735, 780, 780, 735, 651, 540, 420, 305, 205, 126, 70,
                35, 15, 5, 1]
    nH=17
else:
    print("NO")

for k in range(numNum):
    print("nH = " + str(nH))
    dictProb[nH]=probList[nH-dieNum]/numComb
    nH=nH+((-1)**k)*(k+1)

sorted_dict = sorted(dictProb.items(), key=operator.itemgetter(1), reverse=True)
for i in sorted_dict:
    print (i)



currentList=[]
newList=[]
for i in sorted_dict:
    currentList.append(i[0])

print()
print(currentList)
print(sorted(currentList))

# Playing the game to find better combinations of numbers

p1Win=p2Win=0


rollTimes = 1000000

best_found = False
otherOption = []

bestList = currentList[:]
attempt = 0
indW = -1    # How far into the "worst" elements we'll switch by better ones
indB = 0        # How far into the "better" elements we'll test (The first elements on the list)


while not best_found:
    allIndB = 0
    for currentIndB in range(0,indB+1):
        attempt += 1
        newList = bestList[:]
        newList[indW] = currentList[currentIndB]

        if bestList == newList:
            print("Same lists")
            # indB += 1
            # newList = bestList[:]
            # newList[indW] = bestList[indB]

        winner = game(bestList, newList, rollTimes, dieNum, dieVal, False)

        print("\nAttempt " + str(attempt) + ", indB=" + str(indB)+ ", currentIndB=" + str(currentIndB) + ", indW=" + str(indW) + ", allIndB = " + str(allIndB) + ": ")
        print("Player 1: ", end='')
        print(bestList)
        print("Player 2: ", end='')
        print(newList)

        if winner == "Player 1":
            print("Player 1 won")
            allIndB += 1

        elif winner == "Player 2":
            print("Player 2 won")
            bestList = newList[:]
            if currentIndB == indB:
                indB += 1

        elif winner == "too close":
            otherOption = newList[:]
            print("Other option")
            print(sorted(otherOption))


        else:
            print("Winner")
            print(winner)

        if allIndB == indB:
            best_found = True



    indW -= 1





print()
print()
print("BEST LIST IS:")
print(sorted(bestList))
if len(otherOption) > 0:
    print("\nOTHER OPTION:")
    print(sorted(otherOption))