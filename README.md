# Dice Game Solution Algorithm

This is a simulation of a generilized version of a dice game problem I solved using Python in 2018 when I had little knowledge of code. Recently, I decided to improve and optimize the code I had but the logic of my algorithm is still the same. Here, I will explain the problem, my algorithm to solve it and the optimizations I made in the code.

_____
### The Original Game

##### How it works
Imagine a game where there are only two players and each player picks 5 numbers between 2 and 12. For example, one can pick the sequence “5, 6, 6, 9, 12”. Now that both players have picked their combination of numbers, two dice are rolled and their results are summed. If the sum is 6, for instance, you can cross it off once from your list, if it is in it. If the sum is a number you don’t have on your list, you do nothing. Whoever crosses all numbers first wins. 
Since the initial was very simple, all I had to do was find the best combination of 5 picks. The aspect of this problem that makes it interesting is the fact that we cannot just choose the 5 of the most likely values, because repetitions limit the possible permutations you can have between your numbers. That is, if you have five 7’s, there is only one possible order you can get your numbers (7, 7, 7, 7, 7), while if you have 5 distinct numbers, you can have a lot more (5! = 120), which makes it a lot more likely to happen (at least in this case). So, the interesting part of the problem is figuring out when to use distinct numbers and when to repeat a more likely sum.

To better understand the problem, it is very important to understand the probabilities that revolve around it. By this, I mean the probabilities of getting each of the sums. So, let us understand where they come from.

IMAGE1

By reading this table, we can get a better understanding of how likely each of the sums is to occur. 
Since there are a total of 36 permutations and the sum of 2 only happens once, we say P(2) = 1/36 = 2.78%. 
The sum of 5, as another example, happens 4 times. Therefore P(5) = 4/36 = 11.11%. 
From this, we get:
```
P(2) = 2.78%, P(3) = 5.55%, P(4) = 8.33%, P(5): 11.11%, P(6): 13.89%, **P(7): 16.67%**, P(8): 13.89%, P(9): 11.11%, P(10): 8.33%, P(11): 5.55%, P(12): 2.78%
```


##### Solution of the Original Game
Now, with the probabilities of each of the sums in hand, we can come up with a first possible best option. For this, I suggest we pick the 5 different sums that simply have the highest probabilities of occurring.
For this problem (5 picks, 2 dice, 6-sided), the obvious option is [5, 6, 7, 8, 9], as they have the highest values.
Now, it obviously makes no sense to switch any of these numbers with a number that has a lower probability of happening (such as 12). Also, if we do want to switch a number, the logical one to remove is one with the lowest probabilities, that is, 5 or 9. Also very clearly, the first best option to switch one of these numbers by is 7, as it has the highest probability of occurring, which might be enough to overcome the problem of repeating values (and losing permutations of results).
So, all I did was simulate this game to compare the combinations [5, 6, 7, 8, 9] and [5, 6, 7, 8, 7].

IMAGE2

Since the initial combination is better than the best other option, it is clearly the ideal combination of picks for this game.
_____
### The Generalized Version of the Game

##### What is Generalized?

In the original game, using **6-sided dice**, we have **two dice** and each player has **five picks** on their lists. 
The way I generalized this problem was to allow for **k-sided dice**, using **N dice** and each player has **M picks** on their lists, all variables of the function for more interesting results.

##### Solution of the Generalized Game
I made it so that the initial list of elements contained all the most individually probable sums in decreasing order of probability.
For example, [5, 6, 7, 8, 9] is written [7, 8, 6, 9, 5].
This way I can easily keep track of which element I am currently trying to substitute (simply the last element on the list which I have not yet found a better number).
The logic behind this process is simplified in the figure:

IMAGE 3 - SUBSTITUTION LOGIC

Where 0 will be the index of the sum with the highest probability and the lower the value, the higher the probability. So, we will first switch 7, the last (and worst) element, with 0, the best one. If 0 “loses”, that is, if the combination with 7 is better than the one with a second 0, then we can already finish and say [0, 1, 2, 3, 4, 5, 6, 7] is the best combination. This is because there is no other logical option to substitute 7. Since the element 0 is the most probable sum and there isn’t more 0’s than other elements in the list, so no other option would be better than either 7 or 0 for this case.
Now, if 0 “wins”, we will make the last element of the list equal to 0 and start substituting the second to last, 6. For this, since we already have two 0’s in our list, we must start also test 1, as getting a “second 1” might be more beneficial than a “third 0” because of it has more permutations than three 0's and also has a higher probability than 6. So, we check to see if 0 is better than 6. If yes, switch 6 by 0 and check if 1 is better than that. This order follows the greyscale in the figure above from darker to lighter, until we get an index that is not substituted by any other.
For example, if 4 wins against 0, 1, 2 and 3 above, that would give us the final best result with 4 in and whatever results were best for the last 3 elements, leaving the first ones unchanged.

_____

### Code Optimizations

##### Count Array
Initially, I used regular arrays to represent the lists of 2 players (e.g. [5, 6, 7, 8, 9). So, the operations of checking if an element i was in the lists had time complexity O(len(array)), which was not optimal.
The first and simplest optimization I did was to represent the competing arrays as count arrays when simulating a game, where count_array[i] = original_array.count(i). This was done so that we can check if a rolled dice sum is in any of the competing arrays and subtract from the arrays at constant time. The change is space complexity is negligible since it is equal to the highest sum we can get, which is never very big.
Since count_array[0] would always be 0 (because you can't get a 0 roll of the dice), we use count_array[0] to represent the sum of all count_array[i] for i>0. This is done so that we can check in constant time if an array has crossed all numbers of their list (by checking if count_array[0] = 0).

```
An example transformation from original array to count array:
[5, 6, 7, 7, 8] --> [5, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0]
```

##### Determining Ties
A quick optimization I made was the way I determined ties. Originally, I would check if both lists had all their picks crossed out and if so, that would be a tie. To improve this, I simply checked if both lists were equal because if at any point both lists are equal, a tie is inevitable so I can simply end the game at that point. This optimization was very impactful in games where the lists were very big and therefore most games ended up in a tie.

##### Simulating the Dice Rolls
This was the change with the most drastic impact in the run time of my program. Originally, I would simulate each dice individually and sum up the results to check between lists. The change I made was to simulate multiple dice rolls in advance using the probability of each sum occurring. I was already calculating these probabilities in order to properly sort the original array according to the probabilities of the sum (as described in the section "Solution of the Original Game"). Therefore, with these probabilities, I could very quickly simulate a multitude of dice sum results using random.choices (simulating multiple ones at once is much faster than one at a time) and simply add them to a queue. What I could also do with this method is skip results that weren't in either one of the lists, as they would not have an impact in the game.

##### Using a Variable Number of Dice Rolls
For every "match" between two lists, I would simulate X games (usually 100,000 games) so that I would have a large enough number of results to be confident in the winner between the 2 lists. However, some of the matches could be easily determined with fewer games, as one of the lists was much better than the other. Therefore, I introduced 3 variables: _min_dice_rolls_, _max_dice_rolls_ and _decisive_win_percentage_. This way I would simulate _min_dice_rolls_ (e.g. 10,000) games and if one player had won more than _decisive_win_percentage_ (e.g. 60%) of the games, then that would be enough to determine the winner. If the percentage was less that _decisive_win_percentage_, I would then simulate 9x more games than what I had previsouly simulated (so that if I had rolled 10,000 games so far, I would simulate a total of 10,000+90,000=100,000) and check the percentage again until the total number of dice rolls is greater or equal to _max_dice_rolls_.