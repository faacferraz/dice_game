import random
import operator


def percent(a,b):
    if a>b:
        return round((100*a/b)-100,2)
    if a<b:
        return round((100*b/a)-100,2)
    if a==b:
        return 100



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
        return "Player 2 by " + str(percent(p1Win, p2Win))
    else:
        return str(percent(p1Win, p2Win))



player1 = [9, 10, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 18, 19]
player2 = [9, 10, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 18, 14]
print(game(player1, player2,100000,4,5,False))
