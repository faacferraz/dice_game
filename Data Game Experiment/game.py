import random


sum = 0  #Amount of money you have
h = 0  #Number of heads
t = 0  #Number of Tails
HorT = 0  #Heads or Tails
needed = 4  #Consecutive tails needed to lose
paying = (2**needed)
current = 0   #Current streak of tails
hcurrent = 0  #Highest streak of tails
gamesPlayed = 10000 #Amount of games you want to play
highestSum = 0
lowestSum = 0


for n in range (0,gamesPlayed):
    current = 0
    hcurrent = 0
    sum -= paying
    while current < needed:
        HorT = random.randint(0,1) #Flip the coin for Heads or Tails (0=Tails, 1=Heads)

        if sum<lowestSum:
            lowestSum = sum
        if sum>highestSum:
            highestSum = sum

        if HorT == 1:   #if Heads
            h+=1        #add 1 to Heads sum
            sum+=1      #add $1 to sum
            current = 0 #reset streak

        if HorT == 0:   #if Tails
            t+=1        #add 1 to Tails sum
            current+=1  #add 1 to fail streak

        if (current > hcurrent):
            hcurrent = current
            #print(hcurrent) #In case the "needed" you are using is super big, this might be fun to use

print()
print("Times Ran: " +str(gamesPlayed))
print("Paying: $"+str(paying))
print ("Heads: "+str(h))
print ("Tails: "+str(t))
print ("Difference: "+ str(abs(t-h)) + ". (" + str(abs(round(100-(h*100/t),2)))+"%)")  #Just to make sure the rolls were random
print()
print("Sum: " + str(sum))
print("Highest Sum: " + str(highestSum))
print("Lowest Sum: " + str(lowestSum))
print(sum)