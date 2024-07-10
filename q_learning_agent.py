import random
from tictactoe import TicTacToe
import pickle

class QLearningAgent:

    def __init__(self, alpha=0.2, gamma=0.9, epsilon=0.5, epsilon_decay=0.999999):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.history = []

    def get_q_value(self, state, action):
        state_tuple = tuple(tuple(row) for row in state)
        return self.q_table.get((state_tuple, action), -0.0001)

    def update_q_value(self, state, action, reward, next_state):
        state_tuple = tuple(tuple(row) for row in state)
        next_state_tuple = tuple(tuple(row) for row in next_state)
        best_next_action = self.best_action(next_state_tuple)
        td_target = reward + self.gamma * self.get_q_value(next_state_tuple, best_next_action)
        td_error = td_target - self.get_q_value(state_tuple, action)
        new_q_value = self.get_q_value(state_tuple, action) + self.alpha * td_error
        self.q_table[(state_tuple, action)] = new_q_value
        # print(f"state and action = {state_tuple}, {action}")
        # print(f"q_table[({state_tuple}, {action})] = {new_q_value}")

        # self.history.append((state, action, reward, next_state))
        #
        # if reward >= 1:
        #
        #     for h in self.history:
        #         h_state, h_action, _, _ = h
        #         h_state_tuple = tuple(tuple(row) for row in h_state)
        #         if h_action == action:
        #             self.q_table[(h_state_tuple, h_action)] += 0.01
        #
        # if reward <= -1:
        #
        #     for h in self.history:
        #         h_state, h_action, _, _ = h
        #         h_state_tuple = tuple(tuple(row) for row in h_state)
        #         if h_action == action:
        #             self.q_table[(h_state_tuple, h_action)] -= 0.01

    def available_actions(self, state):
        return [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0]

    def best_action(self, state):
        state_tuple = tuple(tuple(row) for row in state)
        available_actions = self.available_actions(state_tuple)
        # print(f"available_actions = {available_actions}")
        if not available_actions:
            return None
        q_values = [self.get_q_value(state_tuple, action) for action in available_actions]
        max_q_value = max(q_values)
        # print(f"q_values = {q_values}")
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


def train_agent_first_move(episodes):
    env = TicTacToe()
    agent = QLearningAgent()

    # existing_agent = QLearningAgent.load("agent_human_second.pkl")

    for episode in range(episodes):
        state = env.reset()
        state = board_to_tuple(state)
        previous_state = state
        done = False

        while not done:
            available_actions = env.available_actions()
            # q_values = {action: existing_agent.q_table.get((state, action), None) for action in available_actions}

            # if any(q is not None for q in q_values.values()):
            #     opponent_action = max(q_values, key=lambda action: (
            #         q_values[action] if q_values[action] is not None else -float('inf')))
            #     # print(f"Using Q-table for opponent_action_1: {opponent_action}")
            # else:
            #     opponent_action = random.choice(available_actions)
            #     # print("Using random action for opponent_action_1")

            opponent_action = random.choice(available_actions)

            next_state, opponent_reward, done = env.step(opponent_action, 1)
            next_state = board_to_tuple(next_state)

            if done:
                reward = -2
                agent.update_q_value(previous_state, action, reward, state)
                break
            previous_state = board_to_tuple(state)
            action = agent.choose_action(next_state)
            state, reward, done = env.step(action, -1)
            state = board_to_tuple(state)

            agent.update_q_value(next_state, action, reward, state)

            if done:
                break

        agent.epsilon *= agent.epsilon_decay

        if (episode + 1) % 10000 == 0:
            print(f"Episode {episode + 1}/{episodes} completed")
            print(f"Q-table size: {len(agent.q_table)}")

            test_state = board_to_tuple([[1.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
            # agent.save("trained_agent_second_move.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)

    print("Выигрыши и ничьи, агент -1:", env.get_win_counts())

    return agent


def train_agent_second_move(episodes):
    env = TicTacToe()
    agent = QLearningAgent()

    # existing_agent = QLearningAgent.load("agent_human_first.pkl")
    # print(f"Loaded Q-table size: {len(existing_agent.q_table)}")

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
            state = board_to_tuple(next_state)
            if done:
                break

            available_actions = env.available_actions()
            # q_values = {action: existing_agent.q_table.get((state, action), None) for action in available_actions}

            # print(f"Current state: {state}")
            # print(f"Available actions: {available_actions}")
            # print(f"Q-values: {q_values}")

            # if any(q is not None for q in q_values.values()):
            #     opponent_action = max(q_values, key=lambda action: (
            #         q_values[action] if q_values[action] is not None else -float('inf')))
            #     # print(f"Using Q-table for opponent_action_2: {opponent_action}")
            # else:
            #     opponent_action = random.choice(available_actions)
            #     # print("Using random action for opponent_action_2")

            opponent_action = random.choice(available_actions)

            next_state, opponent_reward, done = env.step(opponent_action, -1)
            next_state = board_to_tuple(next_state)

            if done:
                reward = -2
                agent.update_q_value(previous_state, action, reward, state)
                break
            # else:
            #     agent.update_q_value(next_state, opponent_action, opponent_reward, state)
            previous_state = state
            state = next_state

        agent.epsilon *= agent.epsilon_decay

        if (episode + 1) % 10000 == 0:
            print(f"Episode {episode + 1}/{episodes} completed")
            print(f"Q-table size: {len(agent.q_table)}")

            test_state = board_to_tuple([[1.0, -1.0, 0.0], [1.0, -1.0, 0.0], [0.0, 0.0, 0.0]])
            # agent.save("trained_agent.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)

    print("Выигрыши и ничьи, агент +1:", env.get_win_counts())




    return agent


if __name__ == "__main__":
    trained_agent_first_move = train_agent_first_move(episodes=4000)

    trained_agent_second_move = train_agent_second_move(episodes=4000)

