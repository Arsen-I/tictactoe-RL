from q_learning_agent import QLearningAgent, board_to_tuple
from tictactoe import TicTacToe
import random
def robot_game(first_agent, second_agent):
    env = TicTacToe()
    state = env.reset()
    state_tuple = board_to_tuple(state)

    for i in range(100):

        done = False

        epsilon = 0.5

        while not done:
            env.render()
            print()

            action = first_agent.choose_action(state_tuple)


            # action = first_agent.choose_action(state_tuple)
            next_state, reward, done = env.step(action, 1)
            next_state_tuple = board_to_tuple(next_state)
            first_agent.update_q_value(state_tuple, action, reward, next_state_tuple)  # Обновление Q-таблицы
            state = next_state

            if done:
                break

            state_tuple = board_to_tuple(state)

            action = second_agent.choose_action(state_tuple)


            next_state, reward, done = env.step(action, -1)
            next_state_tuple = board_to_tuple(next_state)
            second_agent.update_q_value(state_tuple, action, reward, next_state_tuple)  # Обновление Q-таблицы
            state = next_state

        env.render()

        if env.winner == 1:
            print("firs agent is win!")
        elif env.winner == -1:
            print("second agent is win!")
        else:
            print("Ничья!")



if __name__ == "__main__":

    first_agent = QLearningAgent.load("agent_human_second.pkl")
    second_agent = QLearningAgent.load("agent_human_first.pkl")

    robot_game(first_agent, second_agent)