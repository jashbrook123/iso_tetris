import numpy as np
import random
import time
import pygame
import game_class as gc
import mb_gen as mb

def iso_to_screen(x, y):
    newx = 2*(8*x - 23) +50
    newy = 2*(4*x + 8*y -23) + 75
    return (newx,newy)

def render_board(screen,board,piece):
    new_board = gc.merge_piece(board,piece)
    for y in range(19,-1,-1):
        for x in range(0,10):
            if new_board[y][x] != 0:
                shape_num = new_board[y][x]
                image = pygame.transform.scale_by(pygame.image.load(f"assets/{shape_num}.png"),2)
                coords = iso_to_screen(x,y)
                screen.blit(image,coords)

def render_falling_piece(screen, piece):
    for row in range(len(piece.matrix)-1,-1,-1):
        for col in range(len(piece.matrix[row])):
            if piece.matrix[row][col] != 0:
                shape_num = piece.matrix[row][col]
                image = pygame.transform.scale_by(pygame.image.load(f"assets/{shape_num}.png"),2)
                boardx = piece.x + col
                boardy = piece.y + row
                coords = iso_to_screen(boardx,boardy)

                screen.blit(image,coords)

pygame.init()

screen = pygame.Surface((200, 450))
big_screen = pygame.display.set_mode((400, 900))
clock = pygame.time.Clock()
running = True
dt = 0
db_time = 250  # ms
past_click = 250

game_running = True
board = gc.Board()
piece_type = random.choice(list(gc.tetrominoes.keys()))
piece = getattr(gc, "Piece")(piece_type)
last_drop = time.time()
drop_speed = 0.5 
background = mb.get_building_surf(10,20)
background = pygame.transform.scale_by(background,2)
landed_pieces = []

while running:
    screen.fill((0,0,0))
    screen.blit(background,(18,27))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_w: piece = gc.rotate_move(board,piece)
            elif event.key == pygame.K_a: piece = gc.left(board,piece)
            elif event.key == pygame.K_d: piece = gc.right(board,piece)
            elif event.key == pygame.K_s: 
                now = pygame.time.get_ticks()
                if now - past_click <= db_time: piece = gc.slam(board,piece)
                else: piece = gc.soft_drop(board,piece)
                past_click = now

    last_drop,game_running,piece,board,landed_pieces = gc.game_tick(last_drop,drop_speed,game_running,piece,board,landed_pieces)

    render_board(screen,board,piece)

    big_screen.blit(pygame.transform.scale_by(screen,2),(0,0))
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()