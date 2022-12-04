import random
import pickle
import math


class RandomAgent:
    def __init__(self):
        pass

    def get_action(self, state):
        return random.choice(state.possible_actions())


class UserAgent:
    def __init__(self):
        pass

    def get_action(self, state):
        print(state.possible_actions())
        die_num = int(input("Face of the die?"))
        die_count = int(input("How many?"))
        while (die_num, die_count) not in state.possible_actions():
            die_num = int(input("Face of the die?"))
            die_count = int(input("How many?"))

        return die_num, die_count


class ProbabilityAgent:
    def __init__(self):
        pass

    def get_action(self, state):
        face, d_count = state.wager_num, state.wager_count
        die_count = state.get_cur_player_die_count()
        num_of_die = len(die_count)
        opp_need = d_count - die_count[face]
        # binomial distribution
        if opp_need < 0:
            opp_need = 0
        prob = 0
        for i in range(opp_need, num_of_die + 1):
            prob += math.comb(num_of_die, i) * (1 / num_of_die) ** i * (num_of_die - 1 / num_of_die) ** (num_of_die - i)
        # arbitrary threshold
        if prob < 0.5:
            return -1, -1

        # try not the bluff first
        not_bluff_moves = []
        for i in range(face, len(die_count)):
            for j in range(d_count, die_count[i]):
                not_bluff_moves.append((i, j + 1))
        if not_bluff_moves:
            return random.choice(not_bluff_moves)
        return random.choice(state.possible_actions())


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=1, epsilon=0.1):
        self.q = dict()
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.train = True

    def compute_action(self, state):
        actions = state.possible_actions()
        max_q = self.get_max_q_value(state)
        best_actions = []
        for action in actions:
            if self.get_q_value(state, action) == max_q:
                best_actions.append(action)
        return random.choice(best_actions)

    def get_q_value(self, state, action):
        dice_count = state.get_cur_player_die_count()

        face, d_count = state.wager_num, state.wager_count

        simple_state = d_count - dice_count[face]

        # simple_state = state.get_cur_player_die_count()

        q = 0
        if (simple_state, action) in self.q:
            q += self.q[(simple_state, action)]

        elif action == (-1, -1):
            #print("..")
            face, d_count = state.wager_num, state.wager_count
            die_count = state.get_cur_player_die_count()
            num_of_die = len(die_count)
            opp_need = d_count - die_count[face]
            # binomial distribution
            if opp_need < 0:
                opp_need = 0
            prob = 0
            for i in range(opp_need, num_of_die + 1):
                prob += math.comb(num_of_die, i) * (1 / num_of_die) ** i * (num_of_die - 1 / num_of_die) ** (
                            num_of_die - i)
            q = prob * 10
        else:
            # encourage exploring
            #print("..")
            q = 200

        return q

    def get_max_q_value(self, state):
        actions = state.possible_actions()
        max_q = float('-inf')
        for action in actions:
            q = self.get_q_value(state, action)
            if q > max_q:
                max_q = q
        return max_q

    def update(self, state, action, new_state):


        dice_count = state.get_cur_player_die_count()

        face, d_count = state.wager_num, state.wager_count

        simple_state = d_count - dice_count[face]

        # simple_state = state.get_cur_player_die_count()
        if (simple_state, action) in self.q:
            self.q[(simple_state, action)] = (1 - self.alpha) * self.q[(simple_state, action)] + self.alpha * (
                    state.get_reward(action) + self.get_max_q_value(new_state) * self.gamma)
        else:
            self.q[(simple_state, action)] = self.alpha * (
                    state.get_reward(action) + self.get_max_q_value(new_state) * self.gamma)

    def get_action(self, state):
        # simply return the best option when not training
        if not self.train:
            return self.compute_action(state)
        # update the q value weights
        if random.random() < self.epsilon:
            action = random.choice(state.possible_actions())
        else:
            action = self.compute_action(state)
        new_state = state.get_next(action)
        self.update(state, action, new_state)
        return action

    def save_q_table(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.q, f)

    def load_q_table(self, filename):
        with open(filename, "rb") as f:
            self.q = pickle.load(f)
