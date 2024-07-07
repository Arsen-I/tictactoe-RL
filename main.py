from tictactoe import TicTacToe  # Импорт класса TicTacToe из модуля tictactoe
from q_learning_agent import QLearningAgent, train_agent, board_to_tuple  # Импорт QLearningAgent, функции train_agent и board_to_tuple из модуля q_learning_agent
import random  # Импорт модуля random для генерации случайных чисел

def play_with_agent(agent):
    env = TicTacToe()  # Создание экземпляра игровой среды TicTacToe
    state = env.reset()  # Сброс игрового поля до начального состояния
    state_tuple = board_to_tuple(state)  # Преобразование игрового поля в кортеж кортежей
    done = False  # Флаг завершения игры

    while not done:
        env.render()  # Отображение текущего состояния игрового поля
        print()  # Пустая строка для отступа

        action = agent.choose_action(state_tuple)  # Выбор действия агентом
        state, _, done = env.step(action, 1)  # Выполнение действия и получение следующего состояния, награды и флага завершения

        state_tuple = board_to_tuple(state)  # Преобразование игрового поля в кортеж кортежей

        if done:
            break  # Если игра завершена, выход из цикла

        opponent_action = agent.choose_action(state_tuple)  # Случайный выбор действия случайного противника
        state, _, done = env.step(opponent_action, -1)  # Выполнение действия противника и получение следующего состояния, награды и флага завершения
        state_tuple = board_to_tuple(state)  # Преобразование игрового поля в кортеж кортежей

    env.render()  # Отображение конечного состояния игрового поля

    if env.winner == 1:
        print("Agent wins!")  # Если победил агент
    elif env.winner == -1:
        print("Opponent wins!")  # Если победил противник
    else:
        print("It's a draw!")  # Если ничья

def play_against_agent(agent):
    env = TicTacToe()  # Создание экземпляра игровой среды TicTacToe
    state = env.reset()  # Сброс игрового поля до начального состояния
    state_tuple = board_to_tuple(state)  # Преобразование игрового поля в кортеж кортежей
    done = False  # Флаг завершения игры

    print("Вы играете крестиками (1), агент играет ноликами (-1).")

    while not done:
        env.render()  # Отображение текущего состояния игрового поля
        print()  # Пустая строка для отступа

        # Ход человека
        human_action = None
        while human_action not in env.available_actions():
            try:
                row = int(input("Введите номер строки (0, 1 или 2): "))  # Ввод строки игроком
                col = int(input("Введите номер столбца (0, 1 или 2): "))  # Ввод столбца игроком
                human_action = (row, col)  # Формирование действия из введенных координат
            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")  # Вывод сообщения об ошибке
            if human_action not in env.available_actions():
                print("Это место уже занято или ход неверный. Попробуйте снова.")  # Вывод сообщения об ошибке, если ход невозможен

        state, _, done = env.step(human_action, -1)  # Выполнение действия игрока и получение следующего состояния, награды и флага завершения
        state_tuple = board_to_tuple(state)  # Преобразование игрового поля в кортеж кортежей

        if done:
            break  # Если игра завершена, выход из цикла

        # Ход агента
        action = agent.choose_action(state_tuple)  # Выбор действия агентом
        state, _, done = env.step(action, 1)  # Выполнение действия агента и получение следующего состояния, награды и флага завершения
        state_tuple = board_to_tuple(state)  # Преобразование игрового поля в кортеж кортежей

    env.render()  # Отображение конечного состояния игрового поля

    if env.winner == 1:
        print("Вы выиграли!")  # Если победил игрок
    elif env.winner == -1:
        print("Агент выиграл!")  # Если победил агент
    else:
        print("Ничья!")  # Если ничья

# Обучение агента
agent = train_agent()

agent.save("trained_agent.pkl")

# Игра против случайного противника
play_with_agent(agent)

# Игра против агента
play_against_agent(agent)


