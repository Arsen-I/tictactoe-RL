from tictactoe import TicTacToe
from q_learning_agent import train_agent_first_move, board_to_tuple, train_agent_second_move, QLearningAgent, train_agent_against_agent
from game import agent_against_agent, play_against_agent, play_against_agent_second_move, agent_against_random, random_against_agent
import os

def play_with_random(agent):
    env = TicTacToe()
    state = env.reset()
    state_tuple = board_to_tuple(state)
    done = False

    while not done:
        env.render()
        print()

        action = agent.choose_action(state_tuple)
        state, _, done = env.step(action, 1)

        state_tuple = board_to_tuple(state)

        if done:
            break

        opponent_action = agent.choose_action(state_tuple)
        state, _, done = env.step(opponent_action, -1)
        state_tuple = board_to_tuple(state)

    env.render()

    if env.winner == 1:
        print("Agent wins!")
    elif env.winner == -1:
        print("Opponent wins!")
    else:
        print("It's a draw!")

def play_against_agent_first(agent):
    print('play_against_agent_second_move')
    env = TicTacToe()
    state = env.reset()
    state_tuple = board_to_tuple(state)
    done = False

    print("Агент играет крестиками (1), вы играете ноликами (-1).")

    # Первый ход агента
    action = agent.choose_action(state_tuple)
    state, _, done = env.step(action, 1)
    state_tuple = board_to_tuple(state)

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

        state, _, done = env.step(human_action, -1)
        state_tuple = board_to_tuple(state)

        if done:
            break

        # Ход агента
        action = agent.choose_action(state_tuple)
        state, _, done = env.step(action, 1)
        state_tuple = board_to_tuple(state)

    env.render()

    if env.winner == -1:
        print("Вы выиграли!")
    elif env.winner == 1:
        print("Агент выиграл!")
    else:
        print("Ничья!")




def play_against_agent_second(agent):
    print('play_against_agent_first_move')
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

        state, _, done = env.step(human_action, 1)
        state_tuple = board_to_tuple(state)

        if done:
            break

        # Ход агента
        action = agent.choose_action(state_tuple)
        state, _, done = env.step(action, -1)
        state_tuple = board_to_tuple(state)

    env.render()

    if env.winner == 1:
        print("Вы выиграли!")
    elif env.winner == -1:
        print("Агент выиграл!")
    else:
        print("Ничья!")





number = int(input("0 - начать обучение для агентов с рандомом\n"
                   "1 - обучить агента на игре между собой\n"
                   "2 - дообучить агента на выбор с оппонентом, который выбирает шаг рандомно\n"
                   "3 - дообучить агентов между собой после 0го или 1го шагов\n"
                   "4 - дообучить агентов между собой после 2го шага\n"
                   "5 - сыграть с агентом\n"
                   "Ваше число:  "))

if number == 0:

    # Обучение агента
    agent_first = train_agent_first_move(50000)
    agent_first.save("agent_first.pkl")

    agent_second = train_agent_second_move(50000)
    agent_second.save("agent_second.pkl")

    # Игра против случайного противника
    play_with_random(agent_first)

    # Игра против агента, где агент делает первый ход
    play_against_agent_first(agent_first)

    # Игра против агнета, где агент делает второй ход
    play_against_agent_second(agent_second)


elif number == 1:

    agent_first, agent_second = train_agent_against_agent(500000)
    agent_first.save("agent_first.pkl")
    agent_second.save("agent_second.pkl")

    # Игра против агента, где агент делает первый ход
    play_against_agent_first(agent_first)

    # Игра против агнета, где агент делает второй ход
    play_against_agent_second(agent_second)



elif number == 2:
    question = int(input("1 - хотите дообучить агента, который играет за крестики\n"
                         "2 - хотите дообучить агента, который играет за крестики\n"
                         "Ваше число:  "))

    if question==1:
        if os.path.exists("agent_first_updated.pkl"):
            trained_agent = QLearningAgent.load("agent_first_updated.pkl")
        else:
            trained_agent = QLearningAgent.load("agent_first.pkl")

        agent_against_random(trained_agent)

    else:
        if os.path.exists("agent_second_updated.pkl"):
            trained_agent = QLearningAgent.load("agent_second_updated.pkl")
        else:
            trained_agent = QLearningAgent.load("agent_second.pkl")

        random_against_agent(trained_agent)



elif number == 3:

    summ = {'X': 0, '0': 0, '-': 0}

    for i in range(100):
        if i == 0:
            trained_agent_second_step = QLearningAgent.load("agent_second.pkl")
            trained_agent_first_step = QLearningAgent.load("agent_first.pkl")
        else:
            trained_agent_second_step = QLearningAgent.load("agent_second_updated.pkl")
            trained_agent_first_step = QLearningAgent.load("agent_first_updated.pkl")

        result = int(agent_against_agent(trained_agent_first_step, trained_agent_second_step))

        print(f"{i} раз!")

        if result == 1:
            summ['X'] += 1
        elif result == -1:
            summ['0'] += 1
        elif result == 0:
            summ['-'] += 1


    print(f"summ = {summ}")


elif number == 4:

    for i in range(100):
        trained_agent_second_step = QLearningAgent.load("agent_second_updated.pkl")
        trained_agent_first_step = QLearningAgent.load("agent_first_updated.pkl")

        agent_against_agent(trained_agent_first_step, trained_agent_second_step)

        print(f"{i} раз!")

        trained_agent_second_step.save("agent_second_updated.pkl")
        trained_agent_first_step.save("agent_first_updated.pkl")


elif number == 5:
    new_number = int(input("1 - играть за крестики\n"
                           "2 - играть за нолики\n"
                           "Ваш выбор:  "))
    if new_number == 1:
        if os.path.exists("agent_second_updated.pkl"):
            trained_agent = QLearningAgent.load("agent_second_updated.pkl")
        else:
            trained_agent = QLearningAgent.load("agent_second.pkl")

        play_against_agent(trained_agent)
        trained_agent.save("agent_second_updated.pkl")

    else:
        if os.path.exists("agent_first_updated.pkl"):
            trained_agent = QLearningAgent.load("agent_first_updated.pkl")
        else:
            trained_agent = QLearningAgent.load("agent_first.pkl")

        play_against_agent_second_move(trained_agent)
        trained_agent.save("agent_first_updated.pkl")












