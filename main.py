from tictactoe import TicTacToe
from q_learning_agent import train_agent_first_move, board_to_tuple, train_agent_second_move

def play_with_agent(agent):
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

def play_against_agent_second_move(agent):
    print('play_against_agent_second_move')
    env = TicTacToe()
    state = env.reset()
    state_tuple = board_to_tuple(state)
    done = False

    print("Агент играет крестиками (-1), вы играете ноликами (1).")

    # Первый ход агента
    action = agent.choose_action(state_tuple)
    state, _, done = env.step(action, -1)
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


def play_against_agent_first_move(agent):
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

# Обучение агента
agent_human_first = train_agent_first_move(5000)
agent_human_first.save("agent_human_first.pkl")


agent_human_second = train_agent_second_move(5000)
agent_human_second.save("agent_human_second.pkl")

# Игра против случайного противника
play_with_agent(agent_human_second)

# Игра против агента, где агент делает первый ход
play_against_agent_first_move(agent_human_first)

#Игра против агнета, где агент делает второй ход
play_against_agent_second_move(agent_human_second)


