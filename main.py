import copy

from state import State
from agent import *
import math
import matplotlib.pyplot as plt
import glob


class Game:
    def __init__(self, state, agents, display=True):
        self.state = state
        self.agents = agents
        self.turn = 0  # which agent's turn to play
        self.display = display

    def show(self):
        if self.state.over():
            print('----------------------')
            print(f'player {(self.turn - 1) % len(self.state.players)} called liar')
            print(f'Current state: {self.state}')
            print(f'Die: {self.state.die_count}')
            if not self.state.last_player_won():
                print(f'Player {(self.turn - 1) % len(self.state.players)} Lost')
            else:
                print(f'Player {(self.turn - 2) % len(self.state.players)} Lost')
            print('----------------------')
        else:
            print('----------------------')
            print(f'Player {(self.turn - 1) % len(self.state.players)} played {self.state.last_action}')
            print(f'Player {self.turn} to play')
            print(f'Current state: {self.state}')
            print('----------------------')

    # also return the player no of loser
    def loop(self):
        if self.display:
            print('----------------------')
            print(f'Player {self.turn} to play')
            print(f'Current state: {self.state}')
            print('----------------------')
        while not self.state.over():
            self.next()
            if self.display: self.show()
        if self.state.last_player_won():
            return (self.turn - 2) % len(self.state.players)
        else:
            return (self.turn - 1) % len(self.state.players)

    def next(self):
        self.state.next(self.agents[self.turn].get_action(self.state))
        self.turn = (self.turn + 1) % len(self.state.players)


# training for 2 player game
def train2(agent, adversary):
    agent_list = [agent, adversary]
    for i in range(1, 10000001):
        if math.log10(i).is_integer() or i % 1000000 == 0:
            print(i)
            agent.save_q_table(f"q_tables/{i}.pickle")
        agent.train2 = True
        random.shuffle(agent_list)
        game = Game(State(2, num_of_die), agent_list, False)
        game.loop()


def test(agent, adversary=ProbabilityAgent()):
    win = 0
    agent.train2 = False
    r = adversary
    for i in range(1000):
        game = Game(State(2, num_of_die), [r, agent], False)
        win += 1 if (game.loop() != 1) else 0
    return win / 1000.0


def graph(dir):
    agent = QLearningAgent()
    file_list = glob.glob(f"{dir}/*")
    training_num = []
    result = []
    for fname in file_list:
        training_num.append(fname.split(".")[0].split('\\')[1])
        agent.load_q_table(fname)
        result.append(test(agent, ProbabilityAgent()))
    plt.plot(training_num, result, marker='o', label="win % of Q learning agent")
    plt.legend(loc="upper left")
    ax = plt.gca()
    ax.set_ylim([0, 1])
    plt.xlabel("training iterations")
    plt.ylabel("winning % against prob agent")
    for i, t in enumerate(result):
        ax.annotate(t, (training_num[i], result[i]))
    plt.savefig("Test_against_prob.png")
    plt.clf()

    agent = QLearningAgent()
    file_list = glob.glob(f"{dir}/*")
    training_num = []
    result = []
    for fname in file_list:
        training_num.append(fname.split(".")[0].split('\\')[1])
        agent.load_q_table(fname)
        result.append(test(agent, RandomAgent()))
    plt.plot(training_num, result, marker='o', label="win % of Q learning agent")
    plt.legend(loc="upper left")
    ax = plt.gca()
    ax.set_ylim([0, 1])
    plt.xlabel("training iterations")
    plt.ylabel("winning % against random agent")
    for i, t in enumerate(result):
        ax.annotate(t, (training_num[i], result[i]))
    plt.savefig("Test_against_random.png")

    #plt.show()


num_of_die = 6

if __name__ == "__main__":

    agent = QLearningAgent()
    train2(agent, QLearningAgent())
    graph("q_tables")
