import random
import re

class Mine:
    def __init__(self, bombs, size):
        self.size = size
        self.bombs = bombs
        
        self.board = self.make_board()
        self.val()
        self.dug = set()

    def make_board(self):
        board = [[None for o in range(self.size)] for o in range(self.size)]

        bombs_c = 0

        while bombs_c < self.bombs:
            loc = random.randint(0, self.size**2-1)
            col = loc // self.size
            row = loc % self.size

            if board[col][row] == '*':
                continue
            
            board[col][row] = '*'
            bombs_c +=1
        return board

    def val(self):
        for col in range(self.size):
            for row in range(self.size):
                if self.board[col][row] == '*':
                    continue
                self.board[col][row] = self.near_bombs(col,row)
    
    def near_bombs(self, col, row):
        near_bombs_c = 0
        for c in range(max(0, col-1), min(self.size-1, col+1)+1):
            for r in range(max(0, row-1), min(self.size-1, row+1)+1):
                if c == col and r == row:
                    continue
                if self.board[c][r]=='*':
                    near_bombs_c += 1
        return near_bombs_c
    
    def dig(self, col, row):
        self.dug.add((col,row))

        if self.board[col][row] == '*':
            return False
        elif self.board[col][row] > 0:
            return True
        else:
            for c in range(max(0, col-1), min(self.size-1, col+1)+1):
                for r in range(max(0, row-1), min(self.size-1, row+1)+1):
                    if (c, r) in self.dug:
                        continue
                    self.dig(c, r)
        return True

    def __str__(self):
        user_board = [[None for o in range(self.size+1)] for o in range(self.size+1)]
        for col in range(self.size):
            for row in range(self.size):
                if (col, row) in self.dug:
                    user_board[col][row] = str(self.board[col][row])
                else:
                    user_board[col][row]= '_'
        p=0
        for col in range(self.size):
            user_board[col][self.size] = p
            p+=1
        p=0
        for row in range(self.size+1):
            if row == self.size:
                user_board[self.size][row] = 'X'
            else:
                user_board[self.size][row] = str(p)
            p+=1
        

        user_board = str(user_board)
        user_board = user_board.replace(']', '\n')
        user_board = user_board.replace('[', ' ')
        user_board = user_board.replace(',', '')
        user_board = user_board.replace("'", '')

        return user_board
        
def play(size=10, bombs=10):
    
    board = Mine(bombs, size)

    safe = True
    while len(board.dug) < board.size**2 - bombs:
        print(board)
        miner = input('Where will you dig? Format: column,row: ')
        row, col = int(miner[0]), int(miner[-1])
        if col < 0 or col >= board.size or row < 0 or row >= board.size:
            print('Invalid location!')
            continue

        safe = board.dig(col,row)
        if not safe:
            break
    
    if safe:
        print('Victory!')
    else:
        print('Game Over!')
        board.dug = [(c,r) for c in range(board.size) for r in range(board.size)]
        print(board)

play()