import random
import operator
import time

class Simulate:

    def __init__(self, num_dice: int, num_picks: int, dice_val: int = 6, dice_rolls: tuple = (10_000, 1_000_000),
                 print_games: bool = True) -> None:
        self.num_dice = num_dice
        self.num_picks = num_picks
        self.dice_val = dice_val
        self.max_sum = num_dice * dice_val
        self.combinations_list = []
        self.dice_rolls = dice_rolls
        self.seq0_dict = {}
        self.seq1_dict = {}
        self.seqT_dict = {}
        self.simulated_rolls = []
        self.print_games = print_games

    def find_ideal_picks(self) -> list:
        """
        Simulate the game to find the ideal choice of numbers to pick
        :return: Sorted list of the ideal numbers to pick
        """

        self.combinations_list = self.get_combination_list(self.num_dice)

        sorted_combinations = sorted([(i, self.combinations_list[i]) for i in range(self.num_dice,
                                      len(self.combinations_list))],  key=lambda x: x[1], reverse=True)
        print(sorted_combinations)


        if len(sorted_combinations) >= self.num_picks:
            current_list = [sorted_combinations[i][0] for i in range(self.num_picks)]
        else:
            current_list = [sorted_combinations[i][0] for i in range(len(sorted_combinations))]

            for _ in range(self.num_picks - len(sorted_combinations)):
                current_list.append(sorted_combinations[-1][0])

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

                print("indB=-{}. ind={}".format(indB, ind))
                print("Current:", current_list)
                print("New:    ", new_list)
                print("Sorted Current:", sorted(current_list))
                print("Sorted New:    ", sorted(new_list))
                print("Count Current:", player0)
                print("Count New:    ", player1)

                # self.remove_equal_picks(player0, player1)
                # print("Reduced Current:", player0)
                # print("Reduced New:    ", player1)

                if self.combinations_list[current_list[-indB]] == self.combinations_list[new_list[-indB]] and player0[current_list[-indB]] == player1[new_list[-indB]]:
                    print("Equal probability... Skipping this game.")
                    continue

                self.simulate_dice_rolls(player0, player1)

                results = [0, 0, 0]
                for _ in range(self.dice_rolls):
                    results[self.run_game(player0, player1)] += 1

                print("Results:", results)

                if results[1] > results[0]:
                    print("New best found -", new_list)
                    current_list = new_list
                    best_found = False
                print()

        return sorted(current_list)

    def run_game(self, player0: list, player1: list) -> int:
        """
        Simulate one game between two players
        :param player0: List of picks from player0
        :param player1: List of picks from player1
        :return: Winning player (0 or 1)
        """

        num_seq = []
        p0 = player0.copy()
        p1 = player1.copy()


        while True:
            if not self.simulated_rolls:
                self.simulate_dice_rolls(player0, player1)
            sum_dice = self.simulated_rolls.pop(0)

            if p0[sum_dice] or p1[sum_dice]:
                num_seq.append(sum_dice)

            if p0[sum_dice]:
                p0[0] -= 1
                p0[sum_dice] -= 1
            if p1[sum_dice]:
                p1[0] -= 1
                p1[sum_dice] -= 1

            if p0 == p1:
                s = " ".join(str(n) for n in num_seq)
                if s not in self.seqT_dict:
                    self.seqT_dict[s] = 0
                self.seqT_dict[s] += 1
                return -1
            if not p0[0]:
                s = " ".join(str(n) for n in num_seq)
                if s not in self.seq0_dict:
                    self.seq0_dict[s] = 0
                self.seq0_dict[s] += 1
                return 0
            if not p1[0]:
                s = " ".join(str(n) for n in num_seq)
                if s not in self.seq1_dict:
                    self.seq1_dict[s] = 0
                self.seq1_dict[s] += 1
                return 1

    def get_combination_list(self, num_dice: int, n: int = 0, arr: list = None) -> list:
        """
        Get the list of possible combination of each sum, where arr[i] = number of possible combinations to get sum i
        (e.g. [0, 1, 1, 1, 1, 1, 1] for one 6-sided dice).
        :param num_dice: Initial val should be the total number of dice being used (will be decremented with recursion)
        :param n: Function variable
        :param arr: Function variable (array to be returned)
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
        Generate an array of dice
        :param player0:
        :param player1:
        :param rolls: Number of rolls to simulate
        :return:
        """

        weights = self.get_combination_list(self.num_dice).copy()
        sums = [i for i in range(len(weights))]
        for i in range(self.num_dice, len(weights)):
            if (not player0[i]) and (not player1[i]):
                weights[i] = 0

        if dice_rolls:
            rolls = random.choices(sums, weights, k=dice_rolls*2)
        else:
            rolls = random.choices(sums, weights, k=self.dice_rolls*2)

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

    sim = Simulate(num_dice=5, num_picks=22, dice_val=6, dice_rolls=10000)

    #rt = sim.simulate_dice_rolls(a, b)

    rt = sim.find_ideal_picks()

    print("\n\nIdeal pick:", rt)
    total_time = time.time() - start_time
    print("Total time:", total_time)