import pygame
import random

def iso_to_screen(x, y):
    newx = (8*x - 23)+ 23
    newy = (4*x + 8*y -23)+23
    return (newx,newy)
def get_building_surf(height,width):
    sprite_sheet = pygame.image.load("assets/main_building_sprite_sheet.png").convert_alpha()
    building = pygame.Surface(((height+1)*8,(width+5.5)*8))
    for col in range(width-1,-1,-1): # y
        for row in range(height): # x
            if col == 0: 
                if row == 0: 
                    surf = get_top_left(sprite_sheet)
                elif row == height-1:
                    surf = get_top_right(sprite_sheet)
                else:
                    surf = get_top(sprite_sheet)
            elif col == width - 1:
                if row == 0: 
                    surf = get_bottom_left(sprite_sheet)
                elif row == height-1:
                    surf = get_bottom_right(sprite_sheet)
                else:
                    surf = get_bottom(sprite_sheet)
            else:
                if row == 0: 
                    surf = get_left(sprite_sheet)
                elif row == height-1:
                    surf = get_right(sprite_sheet)
                else:
                    surf = get_centre(sprite_sheet)
            building.blit(surf,iso_to_screen(row,col))
    return building

# seperating sprite sheet
def get_top_left(sprite_sheet):
    surf = sprite_sheet.subsurface(0,0,16,16)
    return surf

def get_bottom_left(sprite_sheet):
    surf = sprite_sheet.subsurface(0,17,16,16)
    return surf

def get_top_right(sprite_sheet):
    surf = sprite_sheet.subsurface(51,0,16,16)
    return surf

def get_bottom_right(sprite_sheet):
    surf = sprite_sheet.subsurface(51,17,16,16)
    return surf

def get_left(sprite_sheet):
    surf = sprite_sheet.subsurface(17,17,16,16)
    return surf

def get_right(sprite_sheet):
    surf = sprite_sheet.subsurface(17,0,16,16)
    return surf

def get_bottom(sprite_sheet):
    surf = sprite_sheet.subsurface(34,17,16,16)
    return surf

def get_top(sprite_sheet):
    surf = sprite_sheet.subsurface(34,0,16,16)
    return surf

def get_centre(sprite_sheet):
    rv = random.randint(1,35)
    if rv == 1:
        surf = sprite_sheet.subsurface(68,17,16,16) # sparkles
    else:
        surf = sprite_sheet.subsurface(68,0,16,16) # normal
    return surf
    
""" testing

big_screen = pygame.display.set_mode((650,500))
clock = pygame.time.Clock()
running = True
sprite_sheet = pygame.image.load("assets/main_building_sprite_sheet.png").convert_alpha()
building = get_building_surf(10,8)
building = pygame.transform.scale_by(building,4)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
    big_screen.fill((0,0,0))
    big_screen.blit(building,(0,0))
    screen_ss = pygame.transform.scale_by(sprite_sheet,4)
    big_screen.blit(screen_ss,(300,0))
    pygame.display.flip()
"""