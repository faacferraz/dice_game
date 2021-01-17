import random
import operator
import time


class Simulate:

    def __init__(self, num_dice: int, num_picks: int, dice_val: int = 6, dice_rolls: int = 100000) -> None:
        self.num_dice = num_dice
        self.num_picks = num_picks
        self.dice_val = dice_val
        self.max_sum = num_dice * dice_val
        self.combinations_list = []
        self.dice_rolls = dice_rolls
        self.seq0_dict = {}
        self.seq1_dict = {}
        self.seqT_dict = {}

    def find_ideal_picks(self) -> list:
        """
        Simulate the game to find the ideal choice of numbers to pick
        :return: Sorted list of the ideal numbers to pick
        """

        self.combinations_list = self.get_combination_list(self.num_dice)

        sorted_combinations = sorted([(i, self.combinations_list[i]) for i in range(self.num_dice,
                                                                                    len(self.combinations_list))],
                                     key=lambda x: x[1], reverse=True)
        print(sorted_combinations)

        current_list = [sorted_combinations[i][0] for i in range(self.num_picks)]

        print(current_list)

        # indW = 0  # How far into the "worst" elements we'll switch by better ones (1 = Last element of list)
        # indB = len(current_list) - 1  # How far into the "better" elements we'll test (1 = First element of list)

        indB = 0

        best_found = False

        while not best_found:
            indB += 1
            best_found = True
            for ind in range(indB):
                new_list = current_list.copy()
                # new_list[ind] = sorted_combinations[-1*indW][0]
                new_list[-indB] = sorted_combinations[ind][0]

                player0 = self.convert_to_count_array(current_list)
                player1 = self.convert_to_count_array(new_list)

                print("Current:", sorted(current_list))
                print("New:    ", sorted(new_list))
                print("Count Current:", player0)
                print("Count New:    ", player1)

                # self.remove_equal_picks(player0, player1)
                #
                # print("Reduced Current:", player0)
                # print("Reduced New:    ", player1)

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
            sum_dice = 0
            for _ in range(self.num_dice):
                sum_dice += random.randint(1, self.dice_val)

            if p0[sum_dice] or p1[sum_dice]:
                num_seq.append(sum_dice)

            if p0[sum_dice]:
                p0[0] -= 1
                p0[sum_dice] -= 1
            if p1[sum_dice]:
                p1[0] -= 1
                p1[sum_dice] -= 1

            if not p0[0] and not p1[0]:
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

        rt = [0] * (self.max_sum + 1)
        for n in l:
            rt[n] += 1
        rt[0] = self.num_picks
        return rt

    def simulate_dice_rolls(self, player0: list, player1: list, rolls: int = 100000) -> None:
        """
        Generate an array of dice
        :param player0:
        :param player1:
        :param rolls: Number of rolls to simulate
        :return:
        """
        pass

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


if __name__ == '__main_2_':
    dice_val = 6

    sim = Simulate(3, 12, 6)

    # a = sim.get_combination_list(sim.num_dice)
    #
    # for i, p in enumerate(a):
    #     print(i,(p/sum(a)))

    start_time = time.time()

    results = [0, 0, 0]
    p0, p1 = [10, 11, 9, 12, 8, 13, 7, 14, 6, 15, 11, 10], \
             [10, 11, 9, 12, 8, 13, 7, 14, 6, 9, 11, 10]

    # p0,p1 = [7,8,9,10,11,12,13,14], [7,8,9,10,11,12,13,10]

    print(sorted(p0), sorted(p1))
    p0, p1 = sim.convert_to_count_array(p0), sim.convert_to_count_array(p1)

    for _ in range(10000):
        a = sim.run_game(p0, p1)
        results[a] += 1
    print(results)
    print()
    print(p0)
    print(p1)
    print()

    sim.remove_equal_picks(p0, p1)
    results = [0, 0, 0]
    print(p0)
    print(p1)
    for _ in range(10000):
        a = sim.run_game(p0, p1)
        results[a] += 1
    print(results)

#    a = sim.find_ideal_picks()
#   print(a)
#  print(time.time() - start_time)


if __name__ == '__main__':
    start_time = time.time()

    sim = Simulate(num_dice=4, num_picks=5, dice_val=6, dice_rolls=100000)

    rt = sim.find_ideal_picks()

    print("\n\nIdeal pick:", rt)
    total_time = time.time() - start_time
    print("Total time:", total_time)