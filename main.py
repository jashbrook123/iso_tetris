import numpy as np
import msvcrt
import random
import time
import pygame
import game_class as gc

def iso_to_screen(x, y):
    newx = 2*(100 + 8*x - 15)
    newy = 2*(4*x + 8*y -15)
    return (newx,newy)

def render_board(screen,board):
    for y in range(19,-1,-1):
        for x in range(9,-1,-1):
            if board.grid[y][x] != 0:
                shape_num = board.grid[y][x]
                image = pygame.transform.scale_by(pygame.image.load(f"assets/{shape_num}.png"),2)
                coords = iso_to_screen(x,y)
                screen.blit(image,coords)

def get_iso_matrix():
    BLOCK_W = 16
    BLOCK_H = 16

    return np.array([
        [BLOCK_W * 0.5, -BLOCK_W * 0.5],
        [BLOCK_H * 0.25, BLOCK_H * 0.25]
    ])






pygame.init()
screen = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()
running = True
dt = 0

game_running = True
board = gc.Board()
piece_type = random.choice(list(gc.tetrominoes.keys()))
piece = getattr(gc, "Piece")(piece_type)
last_drop = time.time()
drop_speed = 0.5 
background = pygame.transform.scale_by(pygame.image.load("assets/background.png"),2)
landed_pieces = []

while running:
    screen.fill((0,255,0))
    screen.blit(background,(100,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_w: piece = gc.rotate_move(board,piece)
            elif event.key == pygame.K_a: piece = gc.left(board,piece)
            elif event.key == pygame.K_d: piece = gc.right(board,piece)
            elif event.key == pygame.K_s: piece = gc.soft_drop(board,piece)


    last_drop,game_running,piece,board,landed_pieces = gc.game_tick(last_drop,drop_speed,game_running,piece,board,landed_pieces)

    gc.render_board(board,piece)
    render_board(screen,board)



    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()