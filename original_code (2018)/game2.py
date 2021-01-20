import random

def percent(a,b):
    if a>b:
        return round((100*a/b),2)
    if a<b:
        return round((100*b/a),2)
    if a==b:
        return 100

d1=d2=d3=d4=d5=d6=0
s2=s3=s4=s5=s6=s7=s8=s9=s10=s11=s12=0
p1Win=p2Win=tie=0


rollTimes = 1000000


player1 = [5,6,7,8,9]
player2 = [5,6,7,8,7]


p1 = player1[:]
p2 = player2[:]

for n in range(0,rollTimes):
    dice1 = random.randint(1,6)  # Dice 1 roll between 1 and 6
    dice2 = random.randint(1,6)  # Dice 2 roll

    if dice1 == 1 or dice2== 1:
        d1+=1
        if dice1==dice2:
            d1+=1
    if dice1 == 2 or dice2== 2:
        d2+=1
        if dice1==dice2:
            d2+=1
    if dice1 == 3 or dice2== 3:
        d3+=1
        if dice1==dice2:
            d3+=1
    if dice1 == 4 or dice2== 4:
        d4+=1
        if dice1==dice2:
            d4+=1
    if dice1 == 5 or dice2== 5:
        d5+=1
        if dice1==dice2:
            d5+=1
    if dice1 == 6 or dice2== 6:
        d6+=1
        if dice1==dice2:
            d6+=1

    if (dice1+dice2)==2:
        s2+=1
    if (dice1+dice2)==3:
        s3+=1
    if (dice1+dice2)==4:
        s4+=1
    if (dice1+dice2)==5:
        s5+=1
    if (dice1+dice2)==6:
        s6+=1
    if (dice1+dice2)==7:
        s7+=1
    if (dice1+dice2)==8:
        s8+=1
    if (dice1+dice2)==9:
        s9+=1
    if (dice1+dice2)==10:
        s10+=1
    if (dice1+dice2)==11:
        s11+=1
    if (dice1+dice2)==12:
        s12+=1


    if (dice1+dice2) in player1:
        player1.remove(dice1+dice2)

    if (dice1+dice2) in player2:
        player2.remove(dice1+dice2)

    # print()
    # print("Rolled a " + str(dice1+dice2))
    # print("p1: " + str(player1) + str(len(player1)))
    # print("p2: " + str(player2) + str(len(player2)))
    # print()

    if not player1 and not player2:  #tie
        player1 = p1[:]
        player2 = p2[:]
        tie+=1
        #p2Win += 1
        #p1Win += 1
        #print("tie")

    elif not player1:
        player1 = p1[:]
        player2 = p2[:]
        p1Win += 1
        #print("p1 won")

    elif not player2:
        player1 = p1[:]
        player2 = p2[:]
        p2Win += 1
        #print("p2 won")









print()
print()
print ("Dice 1: " + str(d1))
print ("Dice 2: " + str(d2))
print ("Dice 3: " + str(d3))
print ("Dice 4: " + str(d4))
print ("Dice 5: " + str(d5))
print ("Dice 6: " + str(d6))
print ()
print ("Sum of 2: " + str(s2) + "  - " + str(round(100*s2/rollTimes, 2)) + "%")
print ("Sum of 3: " + str(s3) + "  - " + str(round(100*s3/rollTimes, 2)) + "%")
print ("Sum of 4: " + str(s4) + "  - " + str(round(100*s4/rollTimes, 2)) + "%")
print ("Sum of 5: " + str(s5) + " - " + str(round(100*s5/rollTimes, 2)) + "%")
print ("Sum of 6: " + str(s6) + " - " + str(round(100*s6/rollTimes, 2)) + "%")
print ("Sum of 7: " + str(s7) + " - " + str(round(100*s7/rollTimes, 2)) + "%")
print ("Sum of 8: " + str(s8) + " - " + str(round(100*s8/rollTimes, 2)) + "%")
print ("Sum of 9: " + str(s9) + " - " + str(round(100*s9/rollTimes, 2)) + "%")
print ("Sum of 10: " + str(s10) + " - " + str(round(100*s10/rollTimes, 2)) + "%")
print ("Sum of 11: " + str(s11) + " - " + str(round(100*s11/rollTimes, 2)) + "%")
print ("Sum of 12: " + str(s12) + " - " + str(round(100*s12/rollTimes, 2)) + "%")



print()
print()
print()
print()
print()
print()
print()
print(str(p1) + " Wins: " + str(p1Win))
print(str(p2) + " Wins: " + str(p2Win))
if (p1Win and p2Win) > 0:
    print("Ratio: " + str(percent(p2Win,p1Win)) + "%")

print("Games played:  " + str(p1Win + p2Win + tie))
