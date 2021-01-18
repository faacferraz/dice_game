import random
import time

class Simulate:

    def __init__(self, num_dice: int, num_picks: int, dice_val: int = 6, dice_rolls: tuple = (10_000, 1_000_000),
                 decisive_win_percentage: float = 0.60, print_games: bool = True) -> None:
        """
        :param num_dice: Number of dices in the game
        :param num_picks: Number of picks each player makes
        :param dice_val: Size of dice (1 to dice_val)
        :param dice_rolls: Tuple of the form (min_dice_rolls, max_dice_rolls) where each represent the min/max amount
                           of games we should simulate for each competing combination of picks
        :param decisive_win_percentage: What win percentage is good enough to not increase the dice rolls (each increase
                                        is done by 9x so the total dice rolls between each check is (n, 10n, 100n, ...)
        :param print_games: if we should print information of the games being played
        """

        self.num_dice = num_dice
        self.num_picks = num_picks
        self.dice_val = dice_val
        self.max_sum = num_dice * dice_val
        self.combinations_list = []
        self.dice_rolls = dice_rolls
        self.rolls = dice_rolls[0]
        self.simulated_rolls = []
        self.decisive_win_percentage = decisive_win_percentage
        self.print_games = print_games

    def find_ideal_picks(self) -> list:
        """
        Find the ideal picks a player should do given the contraints of the game (number of dice, number of picks,
        maximum dice value (1-dice_val).
        :return: Sorted list of the ideal numbers to pick
        """

        self.combinations_list = self.get_combination_list(self.num_dice)

        sorted_combinations = sorted([(i, self.combinations_list[i]) for i in range(self.num_dice,
                                      len(self.combinations_list))],  key=lambda x: x[1], reverse=True)

        if len(sorted_combinations) >= self.num_picks:
            current_list = [sorted_combinations[i][0] for i in range(self.num_picks)]
        else:
            current_list = [sorted_combinations[i][0] for i in range(len(sorted_combinations))]

            for _ in range(self.num_picks - len(sorted_combinations)):
                current_list.append(sorted_combinations[-1][0])

        if self.print_games:
            print(sorted_combinations)
            print(current_list)

        indB = 0

        best_found = False

        while not best_found:
            indB += 1
            best_found = True
            for ind in range(indB):
                new_list = current_list.copy()
                new_list[-indB] = sorted_combinations[ind][0]

                # Skip this game if we are trying to swap a sum for one with the same probability

                player0 = self.convert_to_count_array(current_list)
                player1 = self.convert_to_count_array(new_list)

                if self.print_games:
                    #print("indB=-{}. ind={}".format(indB, ind))
                    print("\n\nCurrent:", current_list)
                    print("New:    ", new_list)
                    print("Sorted Current:", sorted(current_list))
                    print("Sorted New:    ", sorted(new_list))
                    print("Count Current:", player0)
                    print("Count New:    ", player1)

                if self.combinations_list[current_list[-indB]] == self.combinations_list[new_list[-indB]] and \
                        player0[current_list[-indB]] == player1[new_list[-indB]]:
                    if self.print_games:
                        print("Equal probability... Skipping this game.")
                    continue


                results = [0, 0, 0]
                decisive_win = False
                self.rolls = self.dice_rolls[0]
                while not decisive_win:
                    self.simulate_dice_rolls(player0, player1, dice_rolls=self.rolls)

                    for _ in range(self.rolls):
                        results[self.run_game(player0, player1)] += 1
                    self.rolls *= 9
                    if max(results[:2])/sum(results[:2]) >= self.decisive_win_percentage or \
                            self.rolls > self.dice_rolls[1]:
                        decisive_win = True

                if self.print_games:
                    print("Results:", results)

                if results[1] > results[0]:
                    if self.print_games:
                        print("New best found -", new_list)
                    current_list = new_list
                    best_found = False

        return sorted(current_list)

    def run_game(self, player0: list, player1: list) -> int:
        """
        Simulate one game between two players
        :param player0: List of picks from player0
        :param player1: List of picks from player1
        :return: Winning player (0 or 1) or a tie (-1)
        """

        p0 = player0.copy()
        p1 = player1.copy()

        while True:
            if not self.simulated_rolls:
                self.simulate_dice_rolls(player0, player1, self.rolls)
            sum_dice = self.simulated_rolls.pop(0)

            if p0[sum_dice]:
                p0[0] -= 1
                p0[sum_dice] -= 1
            if p1[sum_dice]:
                p1[0] -= 1
                p1[sum_dice] -= 1

            if p0 == p1:
                return -1
            if not p0[0]:
                return 0
            if not p1[0]:
                return 1

    def get_combination_list(self, num_dice: int, n: int = 0, arr: list = None) -> list:
        """
        Get the list of possible combination of each sum, where arr[i] = number of possible combinations to get sum i
        (e.g. [0, 1, 1, 1, 1, 1, 1] for one 6-sided dice).
        :param num_dice: Initial val should be the total number of dice being used (will be decremented with recursion)
        :param n: Function variable
        :param arr: Function variable
        :return: Combination array
        """

        if not arr:
            arr = [0] * (self.dice_val * self.num_dice + 1)

        if not num_dice:
            arr[n] += 1
            return arr

        for d in range(self.dice_val):
            self.get_combination_list(num_dice - 1, n=n + d + 1, arr=arr)

        return arr

    def convert_to_count_array(self, l: list) -> list:
        """
        Convert list l to be an array rt where rt[i] = l.count(i).
        Since rt[0] would always be 0, we use rt[0] to represent the sum of all rt[i] for i>0.
        :param l: Original list of picks
        :return: Converted count array
        """

        rt = [0]*(self.max_sum + 1)
        for n in l:
            rt[n] += 1
        rt[0] = self.num_picks
        return rt

    def simulate_dice_rolls(self, player0: list, player1: list, dice_rolls: int = None) -> None:
        """
        Generate an array of simulated dice rolls for a game between player0 and player1. These dice rolls will only
        give a number that is on either list
        :param player0:
        :param player1:
        :param dice_rolls: Number of rolls to simulate
        :return:
        """

        if self.combinations_list:
            weights = self.combinations_list.copy()
        else:
            weights = self.get_combination_list(self.num_dice)

        sums = [i for i in range(len(weights))]
        for i in range(self.num_dice, len(weights)):
            if (not player0[i]) and (not player1[i]):
                weights[i] = 0

        if dice_rolls:
            rolls = random.choices(sums, weights, k=dice_rolls*2)
        else:
            rolls = random.choices(sums, weights, k=self.rolls*2)

        self.simulated_rolls = rolls
        return rolls

    @staticmethod
    def remove_equal_picks(player0: list, player1: list) -> None:
        """
        Removes the picks from the lists if they are the same and adjust the first element of both lists to
        represent new num_picks (Total number of picks)
        :param player0: List of picks from player0
        :param player1: List of picks from player1
        """

        for i in range(1, len(player0)):
            if player0[i] == player1[i]:
                player0[0] = player1[0] = player0[0] - player0[i]
                player0[i] = player1[i] = 0


if __name__ == '__main__':
    start_time = time.time()

    sim = Simulate(num_dice=5, num_picks=22, dice_val=6, dice_rolls=(10_000, 10_000))

    #rt = sim.simulate_dice_rolls(a, b)

    picks = sim.find_ideal_picks()

    print("\n\nIdeal pick:", picks)
    total_time = time.time() - start_time
    print("Total time:", total_time)