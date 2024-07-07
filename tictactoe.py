import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3))  # Инициализация игрового поля 3x3 нулями
        self.done = False  # Флаг, показывающий завершение игры
        self.winner = None  # Переменная для хранения победителя игры

    def reset(self):
        self.board = np.zeros((3, 3))  # Сброс игрового поля до начального состояния (все нули)
        self.done = False  # Сброс флага завершения игры
        self.winner = None  # Сброс переменной победителя
        return self.board  # Возвращает начальное состояние игрового поля

    def step(self, action, player):
        if self.board[action] == 0 and not self.done:  # Проверка на корректность хода
            self.board[action] = player  # Выполнение хода игрока на игровом поле
            if self.check_winner(player):  # Проверка на победу после хода
                self.done = True  # Установка флага завершения игры
                self.winner = player  # Запись победителя
                reward = 2  # Награда за победу
            elif np.all(self.board != 0):  # Проверка на ничью
                self.done = True  # Установка флага завершения игры
                self.winner = 0  # Объявление ничьей
                reward = 0  # Награда за ничью
            else:
                reward = 0  # Награда за продолжение игры
            return self.board, reward, self.done  # Возвращает текущее состояние поля, награду и флаг завершения
        else:
            return self.board, -2, self.done  # Возвращает текущее состояние поля, отрицательную награду и флаг завершения (неверный ход)

    def check_winner(self, player):
        for i in range(3):
            if np.all(self.board[i, :] == player) or np.all(self.board[:, i] == player):
                return True  # Проверка на победу по строкам и столбцам
        if self.board[0, 0] == player and self.board[1, 1] == player and self.board[2, 2] == player:
            return True  # Проверка на победу по главной диагонали
        if self.board[0, 2] == player and self.board[1, 1] == player and self.board[2, 0] == player:
            return True  # Проверка на победу по побочной диагонали
        return False  # Возвращение False, если победитель не найден

    def available_actions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]
        # Возвращает список доступных действий (ходов), где значение поля равно 0

    def render(self):
        for row in self.board:
            print(' '.join([str(int(cell)) for cell in row]))
        # Выводит текущее состояние игрового поля в консоль