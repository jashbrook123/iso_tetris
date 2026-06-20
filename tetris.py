import numpy as np
import msvcrt
import random
import time
import pygame

tetrominoes = {
    "I": [
        [1, 1, 1, 1]
    ],
    "O": [
        [2, 2],
        [2, 2]
    ],
    "T": [
        [0, 3, 0],
        [3, 3, 3]
    ],
    "S": [
        [0, 4, 4],
        [4, 4, 0]
    ],
    "Z": [
        [5, 5, 0],
        [0, 5, 5]
    ],
    "J": [
        [6, 0, 0],
        [6, 6, 6]
    ],
    "L": [
        [0, 0, 7],
        [7, 7, 7]
    ]
}

def rotate_matrix(matrix):
    return [list(row) for row in zip(*matrix[::-1])]

def collision(board,piece,newx,newy,matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] != 0:
                boardx = newx + col
                boardy = newy + row

                # edge cases
                if boardx < 0: return True
                if boardx >= board.width: return True
                if boardy >= board.height: return True
                
                # check for other pieces
                if boardy >= 0 and (board.grid)[boardy][boardx] !=0: return True 
    return False

def merge_piece(board,piece):
    for row in range(len(piece.matrix)):
        for col in range(len(piece.matrix[row])):
            if piece.matrix[row][col] != 0:
                boardx = piece.x + col
                boardy = piece.y + row
                (board.grid)[boardy][boardx] = piece.matrix[row][col]

def clear_terminal():
    print("\033[H\033[J")

def render_board(board,piece):
    clear_terminal()
    for y in range(board.height):
        line = ""

        for x in range(board.width):
            cell = board.grid[y][x]

            for row in range(len(piece.matrix)):
                for col in range(len(piece.matrix[row])):    
                    if piece.matrix[row][col] != 0:
                        if piece.y + row == y and piece.x + col == x:
                            cell = piece.matrix[row][col]

            if cell != 0: line += "[]"
            else: line += ".."
        print(line)

def clear_lines(board):
    temp_grid = []
    cleared = 0
    for row in board.grid:
        if 0 not in row:
            cleared += 1
        else:temp_grid.append(row)

    for rows in range(cleared):
        temp_grid.insert(0,[0]*board.width)  
    board.grid = temp_grid

def get_input():
    if msvcrt.kbhit(): return msvcrt.getch()
    return None



class Board:
    def __init__(self):
        self.grid = np.zeros((20, 10), dtype=int)
        self.width = 10
        self.height = 20

class Piece:
    def __init__(self, shape):
        self.matrix = [row[:] for row in tetrominoes[shape]]
        self.x = 3
        self.y = 0

    def rotate(self,board):
        rotated = rotate_matrix(self.matrix)
        if not collision(board,self,self.x,self.y,rotated):
            self.matrix = rotated

class Z(Piece):
    def __init__(self):
        super().__init__()
        for i in range(2):
            image = pygame.image.load(f"assets/Z{i+1}.png")
            image = pygame.transform.scale_by(image,4)
            self.image_list.append(image)
        self.img = self.image_list[0]

class S(Piece):
    def __init__(self):
        super().__init__()
        for i in range(2):
            image = pygame.image.load(f"assets/S{i+1}.png")
            image = pygame.transform.scale_by(image,4)
            self.image_list.append(image)
        self.img = self.image_list[0]

class J(Piece):
    def __init__(self):
        super().__init__()
        for i in range(4):
            image = pygame.image.load(f"assets/J{i+1}.png")
            image = pygame.transform.scale_by(image,4)
            self.image_list.append(image)
        self.img = self.image_list[0]

class L(Piece):
    def __init__(self):
        super().__init__()
        for i in range(4):
            image = pygame.image.load(f"assets/L{i+1}.png")
            image = pygame.transform.scale_by(image,4)
            self.image_list.append(image)
        self.img = self.image_list[0]

class I(Piece):
    def __init__(self):
        super().__init__()
        for i in range(2):
            image = pygame.image.load(f"assets/I{i+1}.png")
            image = pygame.transform.scale_by(image,4)
            self.image_list.append(image)
        self.img = self.image_list[0]
        

class O(Piece):
    def __init__(self):
        super().__init__()
        image = pygame.image.load(f"assets/O.png")
        image = pygame.transform.scale_by(image,4)
        self.image_list.append(image)
        self.img = self.image_list[0]


class T(Piece):
    def __init__(self):
        super().__init__()
        for i in range(4):
            image = pygame.image.load(f"assets/T{i+1}.png")
            image = pygame.transform.scale_by(image,4)
            self.image_list.append(image)
        self.img = self.image_list[0]

def game_tick(last_drop,game_running,piece,board):

    if time.time() - last_drop > drop_speed:
        last_drop = time.time()

        if not collision(board, piece, piece.x, piece.y + 1, piece.matrix):
            piece.y += 1
        else: 
            merge_piece(board, piece)
            clear_lines(board)
            piece = Piece(random.choice(list(tetrominoes.keys())))
            if collision(board, piece, piece.x, piece.y, piece.matrix):
                game_running = False
    return last_drop,game_running,piece,board

def left(board,piece):
    if not collision(board, piece, piece.x - 1, piece.y, piece.matrix):
        piece.x -= 1
    return piece

def right(board,piece):
    if not collision(board, piece, piece.x + 1, piece.y, piece.matrix):
        piece.x += 1
    return piece

def soft_drop(board,piece):
    if not collision(board, piece, piece.x, piece.y + 1, piece.matrix):
        piece.y += 1
    return piece

def rotate_move(board,piece):
    piece.rotate(board)
    return piece


game_running = True
board = Board()
piece = Piece(random.choice(list(tetrominoes.keys())))
last_drop = time.time()
drop_speed = 0.5  # seconds per drop

while game_running:
    key = get_input()
    if key != None:
        if isinstance(key,bytes):
            key = key.decode().lower()
        
        if key == 'a':
            piece = left(board,piece)
        elif key == 'd':
            piece = right(board,piece)
        elif key == 's':
            piece = soft_drop(board,piece)
        elif key == 'w':
            piece = rotate_move(board,piece)
        elif key == 'q':
            game_running = False

    last_drop,game_running,piece,board = game_tick(last_drop,game_running,piece,board)
    render_board(board,piece)
    time.sleep(0.02)
