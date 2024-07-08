from q_learning_agent import QLearningAgent, board_to_tuple
from tictactoe import TicTacToe

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
        state, _, done = env.step(action, 1)
        state_tuple = board_to_tuple(state)

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

        state, _, done = env.step(human_action, -1)
        state_tuple = board_to_tuple(state)

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

        # Ход
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


# Загрузка обученного агента и игра против него
if __name__ == "__main__":
    number = int(input("Введите 0 если хотите ходить КРЕСТИКОМ, либо 1 если хотите ходить НОЛИКОМ: "))

    if number == 0:
        trained_agent = QLearningAgent.load("agent_human_first.pkl")
        play_against_agent(trained_agent)
    else:
        trained_agent = QLearningAgent.load("agent_human_second.pkl")
        play_against_agent_second_move(trained_agent)