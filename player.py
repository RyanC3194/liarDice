import random


class Player:
    def __init__(self, num_dice):
        die = [random.randint(1, 6) for _ in range(num_dice)]
        self.die_count = tuple([die.count(i) for i in range(1, 7)])
