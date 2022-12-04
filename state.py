import keyboard
from player import Player
import copy


# Press the green button in the gutter to run the script.
class State:
    def __init__(self, num_player, num_die):
        self.players = [Player(num_die) for _ in range(num_player)]
        self.die_count = [0 for i in range(6)]
        for player in self.players:
            for i in range(6):
                self.die_count[i] += player.die_count[i]
        self.wager_num = 0
        self.wager_count = 0
        self.total_dice = num_player * num_die
        self.called = False
        self.cur_player = 0
        self.last_action = None

    def possible_actions(self):
        # (wager_num, wager_count)
        # (-1, -1) is call liar
        actions = [(-1, -1)]
        for i in range(self.wager_num, 6):
            for j in range(self.wager_count + 1, self.total_dice):
                actions.append((i, j))
        return actions

    def next(self, action):
        if action not in self.possible_actions():
            raise Exception("Invalid move")
        if action == (-1, -1):
            self.called = True
        else:
            self.wager_num, self.wager_count = action
        self.cur_player += 1
        if self.cur_player >= len(self.players):
            self.cur_player = 0
        self.last_action = action

    def get_next(self, action):
        new_state = copy.deepcopy(self)
        new_state.next(action)
        return new_state

    def over(self):
        return self.called

    def last_player_won(self):
        return self.die_count[self.wager_num] < self.wager_count

    def get_reward(self, action):
        if action == (-1, -1):
            # win
            if self.die_count[self.wager_num] < self.wager_count:
                return 100
            # lose
            else:
                return -100
        return 0

    def get_cur_player_die_count(self):
        return self.players[self.cur_player].die_count

    def __repr__(self):
        return f'Die face {self.wager_num}, count {self.wager_count}'
