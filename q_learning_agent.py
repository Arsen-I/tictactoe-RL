import random
from tictactoe import TicTacToe
import pickle

class QLearningAgent:

    def __init__(self, alpha=0.2, gamma=0.9, epsilon=0.5, epsilon_decay=1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.history = []

    def get_q_value(self, state, action):
        state_tuple = tuple(tuple(row) for row in state)
        return self.q_table.get((state_tuple, action), 0)

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
            print("Random!")
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

    for episode in range(episodes):
        state = env.reset()
        state = board_to_tuple(state)
        previous_state = state
        done = False

        while not done:
            available_actions = env.available_actions()
            opponent_action = random.choice(available_actions)
            next_state, opponent_reward, done = env.step(opponent_action, 1)
            next_state = board_to_tuple(next_state)

            if done:
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


        if (episode + 1) % 50000 == 0:
            print(f"Episode {episode + 1}/{episodes} completed")
            print(f"Q-table size: {len(agent.q_table)}")

            test_state = board_to_tuple([[1.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
            # agent.save("trained_agent_second_move.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)

            test_state = board_to_tuple([[1.0, 0.0, -1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]])
            # agent.save("trained_agent_second_move.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)

            test_state = board_to_tuple([[1.0, 0.0, 1.0], [-1.0, 0.0, 1.0], [-1.0, 0.0, 0.0]])
            # agent.save("trained_agent_second_move.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)


            print(f"agent.epsilon = {agent.epsilon}")
            agent.epsilon *= agent.epsilon_decay



    return agent


def train_agent_second_move(episodes):
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
                reward = -1
                agent.update_q_value(previous_state, action, reward, state)
                break

            state = next_state


        if (episode + 1) % 50000 == 0:
            print(f"Episode {episode + 1}/{episodes} completed")
            print(f"Q-table size: {len(agent.q_table)}")

            test_state = board_to_tuple([[1.0, -1.0, 0.0], [1.0, -1.0, 0.0], [0.0, 0.0, 0.0]])
            # agent.save("trained_agent.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)

            test_state = board_to_tuple([[0.0, 0.0, 1.0], [0.0, -1.0, 0.0], [1.0, 0.0, -1.0]])
            # agent.save("trained_agent.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)

            test_state = board_to_tuple([[-1.0, 1.0, 1.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
            # agent.save("trained_agent.pkl")
            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")
                agent.show_q_table(test_state, action)

            print(f"agent.epsilon = {agent.epsilon}")

            agent.epsilon *= agent.epsilon_decay



    return agent


if __name__ == "__main__":
    trained_agent_first_move = train_agent_first_move(episodes=4000)

    trained_agent_second_move = train_agent_second_move(episodes=4000)

