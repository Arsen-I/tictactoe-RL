import random
import numpy as np
from tictactoe import TicTacToe  # Импорт класса TicTacToe из файла tictactoe.py
import pickle

class QLearningAgent:

    def __init__(self, alpha=0.3, gamma=0.9, epsilon=0.2):
        self.q_table = {}  # Инициализация таблицы Q-значений (Q-таблицы)
        self.alpha = alpha  # Параметр обучения (learning rate)
        self.gamma = gamma  # Дисконтный фактор
        self.epsilon = epsilon  # Эпсилон для эпсилон-жадной стратегии
        self.history = []

    def get_q_value(self, state, action):
        state_tuple = tuple(tuple(row) for row in state)  # Преобразование состояния игрового поля в кортеж
        return self.q_table.get((state_tuple, action), -0.1)  # Получение Q-значения из таблицы, либо 0.0, если значения нет

    def update_q_value(self, state, action, reward, next_state):
        state_tuple = tuple(tuple(row) for row in state)  # Преобразование текущего состояния в кортеж
        next_state_tuple = tuple(tuple(row) for row in next_state)  # Преобразование следующего состояния в кортеж
        best_next_action = self.best_action(next_state_tuple)  # Выбор лучшего действия для следующего состояния
        td_target = reward + self.gamma * self.get_q_value(next_state_tuple, best_next_action)  # Целевое значение TD
        print(f"td_target = {td_target}")
        td_error = td_target - self.get_q_value(state_tuple, action)  # Ошибка TD
        print(f"td_error = {td_error}")
        new_q_value = self.get_q_value(state_tuple, action) + self.alpha * td_error  # Новое значение Q-значения
        print(f"self.get_q_value(state_tuple, action) = {self.get_q_value(state_tuple, action)}")
        print(f"state_tuple = {state_tuple}")
        print(f"action = {action}")
        print(f"new_q_value = {new_q_value}")
        self.q_table[(state_tuple, action)] = new_q_value  # Обновление Q-таблицы
        print(f' q_table[(state_tuple, action)]  = {self.q_table[(state_tuple, action)]}')

        # Добавление текущего шага в историю
        self.history.append((state, action, reward, next_state))

        # Дополнительная проверка на выигрыш агента
        if reward > 0:
            # Добавляем небольшой reward ко всем сохраненным шагам
            for h in self.history:
                h_state, h_action, _, _ = h
                h_state_tuple = tuple(tuple(row) for row in h_state)
                if h_action == action:  # Находим предыдущий ход, который привел к текущему выигрышу
                    self.q_table[(h_state_tuple, h_action)] += 0.001  # Пример добавления небольшого reward

    def available_actions(self, state):
        return [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0]  # Возвращает доступные действия для текущего состояния

    def best_action(self, state):
        state_tuple = tuple(tuple(row) for row in state)  # Преобразование состояния в кортеж
        available_actions = self.available_actions(state_tuple)  # Получение доступных действий
        # print(f"available_actions = {available_actions}")
        if not available_actions:
            return None
        q_values = [self.get_q_value(state_tuple, action) for action in available_actions]  # Получение Q-значений для доступных действий
        print(f"q_values = {q_values}")
        max_q_value = max(q_values)  # Нахождение максимального Q-значения
        print(f"max_q_value = {max_q_value}")
        best_actions = [action for action, q in zip(available_actions, q_values) if q == max_q_value]  # Выбор лучших действий
        return random.choice(best_actions)  # Случайный выбор из лучших действий

    def choose_action(self, state):
        state_tuple = tuple(tuple(row) for row in state)  # Преобразование текущего состояния в кортеж
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.available_actions(state_tuple))  # Случайный выбор действия при эпсилон-жадной стратегии
        else:
            act = self.best_action(state_tuple)
            return act  # Выбор лучшего действия по Q-значениям

    def show_q_table(self, state, action):
        key = (board_to_tuple(state), action)  # Разделение ключа (состояние, действие)
        q_value = self.q_table.get(key, "No Q-value found")  # Получение Q-значения
        print(f"State:\n{state}\nAction: {action}\nQ-value: {q_value}\n")  # Вывод состояния, действия и Q-значения

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

def board_to_tuple(board):
    return tuple(tuple(row) for row in board)  # Преобразование игрового поля в кортеж кортежей

def train_agent(episodes=10000):
    env = TicTacToe()  # Создание экземпляра игровой среды TicTacToe
    agent = QLearningAgent()  # Создание экземпляра Q-агента

    for episode in range(episodes):
        state = env.reset()  # Сброс игрового поля до начального состояния
        state = board_to_tuple(state)  # Преобразование игрового поля в кортеж кортежей
        done = False  # Флаг завершения эпизода

        while not done:
            action = agent.choose_action(state)  # Выбор действия агента
            next_state, reward, done = env.step(action, 1)  # Выполнение действия и получение следующего состояния, награды и флага завершения

            print(f"next_state = {next_state}")

            # Обновление Q-значения для хода агента
            agent.update_q_value(state, action, reward, next_state)

            if done:
                break

                # Оппонент делает ход
            opponent_action = agent.choose_action(next_state)
            next_state, opponent_reward, done = env.step(opponent_action, -1)
            next_state = board_to_tuple(next_state)

            # Если оппонент выиграл, агент получает отрицательную награду
            if done:
                reward = -1
                agent.update_q_value(next_state, opponent_action, opponent_reward, state)
                break
            else:
                # Обновление Q-значения для хода оппонента
                agent.update_q_value(next_state, opponent_action, opponent_reward, state)

            state = next_state  # Переход к следующему состоянию

        if (episode + 1) % 1000 == 0:
            print(f"Episode {episode + 1}/{episodes} completed")  # Вывод номера текущего эпизода
            print(f"Q-table size: {len(agent.q_table)}")  # Вывод размера Q-таблицы

            test_state = board_to_tuple([[1.0, -1.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])  # Пример игрового поля для тестирования

            for action in agent.available_actions(test_state):
                print(f"Q-values for state {test_state}:")  # Вывод Q-значений для тестового состояния
                agent.show_q_table(test_state, action)




    return agent

# Замените этот блок кода на вашу основную функцию для обучения и использования агента
if __name__ == "__main__":
    trained_agent = train_agent(episodes=5000)  # Обучение агента на 10000 эпизодах
    trained_agent.show_q_table()  # Вывод Q-таблицы после обучения

