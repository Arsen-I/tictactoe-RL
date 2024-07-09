import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.done = False
        self.winner = None

    def reset(self):
        self.board = np.zeros((3, 3))
        self.done = False
        self.winner = None
        return self.board.copy()

    def step(self, action, player):
        if self.board[action] == 0 and not self.done:
            self.board[action] = player
            if self.check_winner(player):
                self.done = True
                self.winner = player
                reward = 1
            elif np.all(self.board != 0):
                self.done = True
                self.winner = 0
                reward = 0.05
            else:
                reward = 0.5
            return self.board.copy(), reward, self.done
        else:
            return self.board.copy(), -1, self.done

    def check_winner(self, player):
        for i in range(3):
            if np.all(self.board[i, :] == player) or np.all(self.board[:, i] == player):
                return True
        if self.board[0, 0] == player and self.board[1, 1] == player and self.board[2, 2] == player:
            return True
        if self.board[0, 2] == player and self.board[1, 1] == player and self.board[2, 0] == player:
            return True
        return False

    def available_actions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def render(self):
        for row in self.board:
            print(' '.join([str(int(cell)) for cell in row]))