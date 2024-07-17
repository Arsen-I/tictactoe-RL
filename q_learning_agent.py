import random
from tictactoe import TicTacToe
import pickle

class QLearningAgent:

    def __init__(self, alpha=0.01, gamma=0.9, epsilon=0.6, epsilon_decay=0.95):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.history = []

    def get_q_value(self, state, action):
        state_tuple = tuple(tuple(row) for row in state)
        return self.q_table.get((state_tuple, action), -0.001)

    def update_q_value(self, state, action, reward, next_state):
        state_tuple = tuple(tuple(row) for row in state)
        next_state_tuple = tuple(tuple(row) for row in next_state)
        best_next_action = self.best_action(next_state_tuple)
        td_target = reward + self.gamma * self.get_q_value(next_state_tuple, best_next_action)
        td_error = td_target - self.get_q_value(state_tuple, action)
        new_q_value = self.get_q_value(state_tuple, action) + self.alpha * td_error
        self.q_table[(state_tuple, action)] = new_q_value

    def available_actions(self, state):
        return [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0]

    def best_action(self, state):
        state_tuple = tuple(tuple(row) for row in state)
        available_actions = self.available_actions(state_tuple)
        if not available_actions:
            return None
        q_values = [self.get_q_value(state_tuple, action) for action in available_actions]
        max_q_value = max(q_values)
        best_actions = [action for action, q in zip(available_actions, q_values) if q == max_q_value]
        return random.choice(best_actions)

    def choose_action(self, state):
        state_tuple = tuple(tuple(row) for row in state)
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.available_actions(state_tuple))
        else:
            act = self.best_action(state_tuple)
            return act

    def show_q_table(self, state, action):
        key = (board_to_tuple(state), action)
        q_value = self.q_table.get(key, "No Q-value found")
        print(f"State:\n{state}\nAction: {action}\nQ-value: {q_value}\n")

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
def board_to_tuple(board):
    return tuple(tuple(row) for row in board)


def train_agent_second_move(episodes):
    env = TicTacToe()
    agent = QLearningAgent()

    for episode in range(episodes):
        state = env.reset()
        state = board_to_tuple(state)
        previous_state = None
        action = None
        done = False

        while not done:
            available_actions = env.available_actions()
            opponent_action = random.choice(available_actions)
            next_state, opponent_reward, done = env.step(opponent_action, 1)
            next_state = board_to_tuple(next_state)

            if done:
                if env.check_winner(1):
                    reward = -1
                    agent.update_q_value(previous_state, action, reward, state)

                break

            previous_state = board_to_tuple(next_state)

            action = agent.choose_action(next_state)
            state, reward, done = env.step(action, -1)
            state = board_to_tuple(state)

            agent.update_q_value(next_state, action, reward, state)

            if done:
                break


        if (episode + 1) % 10000 == 0:
            print(f"Episode {episode + 1}/{episodes} completed")
            print(f"Q-table size: {len(agent.q_table)}")

            test_state = board_to_tuple([[1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
            # agent.save("trained_agent_second_move.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)

            test_state = board_to_tuple([[1.0, 0.0, -1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
            # agent.save("trained_agent_second_move.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)
            #
            test_state = board_to_tuple([[1.0, 0.0, 1.0], [-1.0, -1.0, 0.0], [1.0, 0.0, 0.0]])
            # agent.save("trained_agent_second_move.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)


            print(f"agent.epsilon = {agent.epsilon}")
            agent.epsilon *= agent.epsilon_decay



    return agent


def train_agent_first_move(episodes):
    env = TicTacToe()
    agent = QLearningAgent()

    for episode in range(episodes):
        state = env.reset()
        state = board_to_tuple(state)
        done = False

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action, 1)
            next_state = board_to_tuple(next_state)
            agent.update_q_value(state, action, reward, next_state)
            previous_state = state
            state = board_to_tuple(next_state)

            if done:
                break

            available_actions = env.available_actions()
            opponent_action = random.choice(available_actions)
            next_state, opponent_reward, done = env.step(opponent_action, -1)
            next_state = board_to_tuple(next_state)

            if done:
                if env.check_winner(-1):
                    reward = -1
                    agent.update_q_value(previous_state, action, reward, state)
                break

            state = next_state


        if (episode + 1) % 10000 == 0:
            print(f"Episode {episode + 1}/{episodes} completed")
            print(f"Q-table size: {len(agent.q_table)}")

            # test_state = board_to_tuple([[1.0, -1.0, 0.0], [1.0, -1.0, 0.0], [0.0, 0.0, 0.0]])
            # # agent.save("trained_agent.pkl")
            # for action in agent.available_actions(test_state):
            #     print(f"Q-values for state {test_state}:")
            #     agent.show_q_table(test_state, action)
            #
            # test_state = board_to_tuple([[0.0, 0.0, 1.0], [0.0, -1.0, 0.0], [1.0, 0.0, -1.0]])
            # # agent.save("trained_agent.pkl")
            # for action in agent.available_actions(test_state):
            #     print(f"Q-values for state {test_state}:")
            #     agent.show_q_table(test_state, action)
            #
            # test_state = board_to_tuple([[-1.0, 1.0, 1.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
            # # agent.save("trained_agent.pkl")
            # for action in agent.available_actions(test_state):
            #     print(f"Q-values for state {test_state}:")
            #     agent.show_q_table(test_state, action)

            print(f"agent.epsilon = {agent.epsilon}")

            agent.epsilon *= agent.epsilon_decay



    return agent


def train_agent_against_agent(episodes):
    env = TicTacToe()

    agent = QLearningAgent()
    agent1 = QLearningAgent()

    for episode in range(episodes):
        state = env.reset()
        state = board_to_tuple(state)
        previous_state = state
        done = False

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action, 1)
            next_state = board_to_tuple(next_state)
            agent.update_q_value(state, action, reward, next_state)

            if done:
                reward = -1
                agent1.update_q_value(previous_state, action, reward, state)
                break

            previous_state = state
            state = board_to_tuple(next_state)


            action = agent.choose_action(state)
            next_state, reward, done = env.step(action, -1)
            next_state = board_to_tuple(next_state)
            agent1.update_q_value(state, action, reward, next_state)


            if done:
                reward = -1
                agent.update_q_value(previous_state, action, reward, state)
                break

            previous_state = state
            state = next_state


        if (episode + 1) % 50000 == 0:
            print(f"Episode {episode + 1}/{episodes} completed")
            print(f"Q-table size: {len(agent.q_table)}")
            print(f"Q-table size: {len(agent1.q_table)}")

            print("Для крестика")
            test_state = board_to_tuple([[1.0, -1.0, 0.0], [1.0, -1.0, 0.0], [0.0, 0.0, 0.0]])
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)

            print("Для нолика")
            test_state = board_to_tuple([[1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
            for action in agent1.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent1.show_q_table(test_state, action)


            print(f"agent.epsilon = {agent.epsilon}")

            agent.epsilon *= agent.epsilon_decay
            agent1.epsilon *= agent1.epsilon_decay



    return agent,agent1


def train_agent_against_agent_updated(agent, agent1, episodes):
    env = TicTacToe()

    summ = {'X': 0, 'O': 0, '-': 0}

    for episode in range(episodes):
        state = env.reset()
        state = board_to_tuple(state)
        previous_state = state
        done = False

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action, 1)
            next_state = board_to_tuple(next_state)
            agent.update_q_value(state, action, reward, next_state)

            if done:
                reward = -1
                agent1.update_q_value(previous_state, action, reward, state)
                break

            previous_state = state
            state = board_to_tuple(next_state)


            action = agent1.choose_action(state)
            next_state, reward, done = env.step(action, -1)
            next_state = board_to_tuple(next_state)
            agent1.update_q_value(state, action, reward, next_state)

            if done:
                reward = -1
                agent.update_q_value(previous_state, action, reward, state)
                break

            previous_state = state
            state = next_state


        if (episode + 1) % 50000 == 0:
            # print(f"Episode {episode + 1}/{episodes} completed")
            # print(f"Q-table size: {len(agent.q_table)}")
            # print(f"Q-table size: {len(agent1.q_table)}")
            #
            # print("Для крестика")
            # test_state = board_to_tuple([[1.0, -1.0, 0.0], [1.0, -1.0, 0.0], [0.0, 0.0, 0.0]])
            # for action in agent.available_actions(test_state):
            #     print(f"Q-values for state {test_state}:")
            #     agent.show_q_table(test_state, action)
            #
            # print("Для нолика")
            # test_state = board_to_tuple([[1.0, 0.0, 1.0], [-1.0, 0.0, 1.0], [-1.0, 0.0, 0.0]])
            # for action in agent1.available_actions(test_state):
            #     print(f"Q-values for state {test_state}:")
            #     agent1.show_q_table(test_state, action)


            print(f"agent.epsilon = {agent.epsilon}")

            agent.epsilon *= agent.epsilon_decay
            agent1.epsilon *= agent1.epsilon_decay

        env.render()

        if env.winner == 1:
            summ['X'] += 1
            print("Выиграл Х")
        elif env.winner == -1:
            summ['O'] += 1
            print("Выиграл 0")

        else:
            summ['-'] += 1
            print("Ничья!")




    return agent,agent1, summ

def train_agent_against_agent_info(agent, agent1, episodes):
    env = TicTacToe()

    summ = {'X': 0, 'O': 0, '-': 0}

    for episode in range(episodes):
        state = env.reset()
        state = board_to_tuple(state)
        done = False

        while not done:
            action = agent.best_action(state)
            next_state, reward, done = env.step(action, 1)
            next_state = board_to_tuple(next_state)


            if done:
                break

            state = board_to_tuple(next_state)


            action = agent1.best_action(state)
            next_state, reward, done = env.step(action, -1)
            next_state = board_to_tuple(next_state)

            if done:
                break
            state = next_state


        if env.winner == 1:
            summ['X'] += 1
        elif env.winner == -1:
            summ['O'] += 1
        else:
            summ['-'] += 1


    return summ


