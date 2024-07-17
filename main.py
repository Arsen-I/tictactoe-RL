from tictactoe import TicTacToe
from q_learning_agent import train_agent_first_move, board_to_tuple, train_agent_second_move, QLearningAgent, train_agent_against_agent, train_agent_against_agent_updated, train_agent_against_agent_info
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
                   "6 - посмотреть результат игры двух агентов\n"
                   
                   "Ваше число:  "))

if number == 0:

    # Обучение агента
    agent_first = train_agent_first_move(800000)
    agent_first.save("agent_first.pkl")

    agent_second = train_agent_second_move(800000)
    agent_second.save("agent_second.pkl")

    # Игра против случайного противника
    play_with_random(agent_first)

    # Игра против агента, где агент делает первый ход
    play_against_agent_first(agent_first)

    # Игра против агнета, где агент делает второй ход
    play_against_agent_second(agent_second)


elif number == 1:

    agent_first, agent_second = train_agent_against_agent(500000)
    # agent_first.save("agent_first.pkl")
    agent_second.save("agent_second.pkl")

    # Игра против агента, где агент делает первый ход
    # play_against_agent_first(agent_first)

    # Игра против агнета, где агент делает второй ход
    play_against_agent_second(agent_second)



elif number == 2:
    question = int(input("1 - хотите дообучить агента, который играет за крестики\n"
                         "2 - хотите дообучить агента, который играет за нолики\n"
                         "Ваше число:  "))

    if question==1:

        u_o_n = int(input("1 - дообучить только обученного\n"
                          "2 - дообучить updated\n"
                          "Число: "))

        if u_o_n == 1:
            trained_agent = QLearningAgent.load("agent_first.pkl")
        else:
            trained_agent = QLearningAgent.load("agent_first_updated.pkl")

        agent_first_new, summ = agent_against_random(trained_agent,10000)

        print(summ)

        question = int(input("1 - сохранить нового агента в updated\n"
                             "2 - не сохранять\n"
                             "Вводите: "))
        if question== 1:
            agent_first_new.save("agent_first_updated.pkl")
        else:
            print("Хорошо")

    else:
        u_o_n = int(input("1 - дообучить только обученного\n"
                          "2 - дообучить updated\n"
                          "Число: "))

        if u_o_n == 1:
            trained_agent = QLearningAgent.load("agent_second.pkl")
        else:
            trained_agent = QLearningAgent.load("agent_second_updated.pkl")

        agent_second_new, summ = random_against_agent(trained_agent, 50000)
        print(summ)

        question = int(input("1 - сохранить нового агента в updated\n"
                             "2 - не сохранять"))
        if question == 1:
            agent_second_new.save("agent_second_updated.pkl")
        else:
            print("Хорошо")



elif number == 3:



    i = int(input("0 - дообучить только что обученных агентов\n"
                  "1 - дообучить агентов с updated\n"
                  "Вводи: "))
    if i == 0:
        trained_agent_second_step = QLearningAgent.load("agent_second.pkl")
        trained_agent_first_step = QLearningAgent.load("agent_first.pkl")
    else:
        trained_agent_second_step = QLearningAgent.load("agent_second_updated.pkl")
        trained_agent_first_step = QLearningAgent.load("agent_first_updated.pkl")

    agent_first_new, agent_second_new, new_summ = train_agent_against_agent_updated(trained_agent_first_step, trained_agent_second_step, 5000)


    print(new_summ)

    q = int(input("1 - обновить таблицу агентов\n"
                  "2 - без сохранения\n"
                  "Введите цифру "))
    if q == 1:
        agent_first_new.save("agent_first_updated.pkl")
        agent_second_new.save("agent_second_updated.pkl")
    else:
        print("Хорошо!")


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
        trained_agent = QLearningAgent.load("agent_second_best.pkl")
        agent = play_against_agent(trained_agent)
        # agent.save("agent_second_best.pkl")

    else:
        trained_agent = QLearningAgent.load("agent_first_best.pkl")
        agent = play_against_agent_second_move(trained_agent)
        # agent.save("agent_first_best.pkl")


elif number == 6:
    trained_agent_first = QLearningAgent.load("agent_first_best.pkl")
    trained_agent_second = QLearningAgent.load("agent_second_best.pkl")

    summ = train_agent_against_agent_info(trained_agent_first,trained_agent_second, 1000)
    print(summ)











