import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.done = False
        self.winner = None
        self.win_count = {1: 0, -1: 0, 0: 0}

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
                # print(f"player = {player}")
                self.win_count[player] += 1
                reward = +2
            elif np.all(self.board != 0):
                self.done = True
                self.winner = 0
                self.win_count[0] += 1
                reward = +1.5
            else:
                reward = +0.01
            return self.board.copy(), reward, self.done
        else:
            return self.board.copy(), -2, self.done

    def potential_opponent_win(self, opponent):
        print(f"opponent = {opponent}")
        for action in self.available_actions():
            temp_board = self.board.copy()
            temp_board[action] = opponent
            if self.check_winner(opponent, temp_board):
                return True
        return False

    def check_winner(self, player, board=None):
        # print(f"player in check winner = {player}")
        if board is None:
            board = self.board

        for i in range(3):
            if np.all(board[i, :] == player) or np.all(board[:, i] == player):
                return True
        if board[0, 0] == player and board[1, 1] == player and board[2, 2] == player:
            return True
        if board[0, 2] == player and board[1, 1] == player and board[2, 0] == player:
            return True
        return False

    def available_actions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def render(self):
        for row in self.board:
            print(' '.join([str(int(cell)) for cell in row]))

    def get_win_counts(self):
        return self.win_count.copy()