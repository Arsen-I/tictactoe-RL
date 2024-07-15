from q_learning_agent import QLearningAgent, board_to_tuple
from tictactoe import TicTacToe
import random

def play_against_agent_second_move(agent):
    env = TicTacToe()
    state = env.reset()
    done = False

    print("Агент играет крестиками (1), вы играете ноликами (-1).")

    while not done:
        env.render()
        print()

        # Ход агента
        state_tuple = board_to_tuple(state)
        action = agent.choose_action(state_tuple)
        next_state, reward, done = env.step(action, 1)
        next_state_tuple = board_to_tuple(next_state)
        agent.update_q_value(state_tuple, action, reward, next_state_tuple)  # Обновление Q-таблицы
        state = next_state

        if done:
            break

        env.render()
        print()

        # Ход человека
        human_action = None
        while human_action not in env.available_actions():
            try:
                row = int(input("Введите номер строки (0, 1 или 2): "))
                col = int(input("Введите номер столбца (0, 1 или 2): "))
                human_action = (row, col)
            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")
            if human_action not in env.available_actions():
                print("Это место уже занято или ход неверный. Попробуйте снова.")

        next_state, _, done = env.step(human_action, -1)
        next_state_tuple = board_to_tuple(next_state)
        reward = -1 if done else 0
        agent.update_q_value(state_tuple, action, reward, next_state_tuple)  # Обновление Q-таблицы
        state = next_state

    env.render()

    if env.winner == 1:
        print("Агент выиграл!")
    elif env.winner == -1:
        print("Вы выиграли!")
    else:
        print("Ничья!")

def play_against_agent(agent):
    env = TicTacToe()
    state = env.reset()
    state_tuple = board_to_tuple(state)
    done = False

    print("Вы играете крестиками (1), агент играет ноликами (-1).")

    while not done:
        env.render()
        print()

        # Ход человека
        human_action = None
        while human_action not in env.available_actions():
            try:
                row = int(input("Введите номер строки (0, 1 или 2): "))
                col = int(input("Введите номер столбца (0, 1 или 2): "))
                human_action = (row, col)
            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")
            if human_action not in env.available_actions():
                print("Это место уже занято или ход неверный. Попробуйте снова.")

        next_state, _, done = env.step(human_action, 1)
        next_state_tuple = board_to_tuple(next_state)
        reward = 1 if done else 0
        agent.update_q_value(state_tuple, action, reward, next_state_tuple)  # Обновление Q-таблицы
        state = next_state

        if done:
            break

        # Ход агента
        state_tuple = board_to_tuple(state)
        action = agent.choose_action(state_tuple)
        next_state, reward, done = env.step(action, -1)
        next_state_tuple = board_to_tuple(next_state)
        agent.update_q_value(state_tuple, action, reward, next_state_tuple)  # Обновление Q-таблицы
        state = next_state

    env.render()

    if env.winner == 1:
        print("Вы выиграли!")
    elif env.winner == -1:
        print("Агент выиграл!")
    else:
        print("Ничья!")

def agent_against_agent(agent_first_step, agent_second_step):

    env = TicTacToe()
    state = env.reset()
    state_tuple = board_to_tuple(state)
    previous_state = state_tuple

    done = False

    print("Агент против Агента")

    while not done:
        env.render()
        print()

        # Ход агента за крестики
        state_tuple = board_to_tuple(state)
        action = agent_first_step.choose_action(state_tuple)
        next_state, reward, done = env.step(action, 1)
        next_state_tuple = board_to_tuple(next_state)
        agent_first_step.update_q_value(state_tuple, action, reward, next_state_tuple)  # Обновление Q-таблицы


        if done:
            if env.check_winner(1):
                print("тут победил крестик")
                reward = -1
                agent_second_step.update_q_value(previous_state, previous_action, reward, state)
            break

        previous_action = action
        previous_state = state
        state = next_state

        # Ход агента за нолики
        state_tuple = board_to_tuple(state)
        action = agent_second_step.choose_action(state_tuple)
        next_state, reward, done = env.step(action, -1)
        next_state_tuple = board_to_tuple(next_state)
        agent_second_step.update_q_value(state_tuple, action, reward, next_state_tuple)  # Обновление Q-таблицы

        if done:
            if env.check_winner(-1):
                print("тут победил нолик")
                reward = -1
                agent_first_step.update_q_value(previous_state, previous_action, reward, state)

            break
        previous_action = action
        previous_state = state_tuple
        state = next_state_tuple


    env.render()

    if env.winner == 1:
        print("Выиграл Х")
        sum['X'] += 1
    elif env.winner == -1:
        print("Выиграл 0")
        sum['O'] += 1
    else:
        print("Ничья!")
        sum['-'] += 1

def agent_against_random(agent_first_step):

    env = TicTacToe()
    state = env.reset()
    done = False

    print("Обучение агента играть за крестики")

    while not done:
        env.render()
        print()

        # Ход агента за крестики
        state_tuple = board_to_tuple(state)
        action = agent_first_step.choose_action(state_tuple)
        next_state, reward, done = env.step(action, 1)
        next_state_tuple = board_to_tuple(next_state)
        agent_first_step.update_q_value(state_tuple, action, reward, next_state_tuple)  # Обновление Q-таблицы

        previous_state = state_tuple
        state = next_state_tuple

        if done:
            break

        available_actions = env.available_actions()
        opponent_action = random.choice(available_actions)

        next_state, opponent_reward, done = env.step(opponent_action, -1)
        next_state = board_to_tuple(next_state)

        if done:
            if env.check_winner(-1):
                print("тут победил рандом нолик")
                reward = -1
                agent_first_step.update_q_value(previous_state, action, reward, state)
            break

        state = next_state

    env.render()

    if env.winner == 1:
        print("Выиграл Х")
        sum['X'] += 1
    elif env.winner == -1:
        print("Выиграл 0")
        sum['O'] += 1
    else:
        print("Ничья!")
        sum['-'] += 1


def random_against_agent(agent_second_step):
    env = TicTacToe()
    state = env.reset()
    previous_state = state
    done = False

    print("Обучение агента играть за нолики")

    while not done:
        available_actions = env.available_actions()
        opponent_action = random.choice(available_actions)

        next_state, opponent_reward, done = env.step(opponent_action, 1)
        next_state = board_to_tuple(next_state)

        if done:
            if env.check_winner(1):
                print("тут победил рандом крестик")
                reward = -1
                agent_second_step.update_q_value(previous_state, action, reward, state)
            break

        action = agent_second_step.choose_action(next_state)
        state, reward, done = env.step(action, -1)
        state = board_to_tuple(state)

        agent_second_step.update_q_value(next_state, action, reward, state)

        if done:
            break

        previous_state = next_state

    env.render()

    if env.winner == 1:
        print("Выиграл Х")
        sum['X'] += 1
    elif env.winner == -1:
        print("Выиграл 0")
        sum['O'] += 1
    else:
        print("Ничья!")
        sum['-'] += 1



if __name__ == "__main__":
    number = int(input("Введите 0 если хотите ходить КРЕСТИКОМ, либо 1 если хотите ходить НОЛИКОМ, либо 2 - агент против агента для обучения. "
                       "Ну а если хотите дообучить на с рандомом то 3 для агента с крестиком, 4 для агента с ноликом:  "))

    if number == 0:
        trained_agent = QLearningAgent.load("agent_human_first_updated.pkl")
        play_against_agent(trained_agent)
        trained_agent.save("agent_human_first_updated.pkl")  # Сохранение обновленного агента


    elif number == 1:
        trained_agent = QLearningAgent.load("agent_human_second_updated.pkl")
        play_against_agent_second_move(trained_agent)
        trained_agent.save("agent_human_second_updated.pkl")  # Сохранение обновленного агента


    elif number == 2:

        trained_agent_first_step = QLearningAgent.load("agent_human_first_updated.pkl")
        trained_agent_second_step = QLearningAgent.load("agent_human_first_updated.pkl")
        sum = {'X':0, 'O':0, '-':0 }

        for i in range(1000):

            agent_against_agent(trained_agent_first_step,trained_agent_first_step)

            trained_agent_first_step.save("agent_human_second_updated.pkl")
            trained_agent_second_step.save("agent_human_first_updated.pkl")
            print(f"{i} раз!")
            print(sum)

        print(sum)


    elif number == 3:
        trained_agent_first_step = QLearningAgent.load("agent_human_second.pkl")
        sum = {'X':0, 'O':0, '-':0 }



        for i in range(2000):

            agent_against_random(trained_agent_first_step)

            trained_agent_first_step.save("agent_human_second_updated.pkl")
            print(f"{i} раз!")
            print(sum)

        print(sum)


    elif number == 4:
        trained_agent_second_step = QLearningAgent.load("agent_human_first.pkl")


        sum = {'X':0, 'O':0, '-':0 }

        for i in range(2000):

            random_against_agent(trained_agent_second_step)

            trained_agent_second_step.save("agent_human_first_updated.pkl")
            print(f"{i} раз!")
            print(sum)

        print(sum)
