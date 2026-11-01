import pygame

# ---------- File Imports ---------- #
from game_state import GameState
from buttons import Button
from sprite import SpriteSheet
from global_variables import *
# ---------------------------------- #

# ----------- Pygame Initialization ----------- #
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
pygame.display.set_caption("The Banished Blade")
# --------------------------------------------- #


# ---------- Image and Button Imports ---------- #
background_image = pygame.image.load("assets/background.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (1280, 720))
title = pygame.image.load("assets/banished_blade_title.png").convert_alpha()
options = pygame.image.load("assets/options_title.png").convert_alpha()

start_button = Button(488, 400, "assets/start_button.png")
options_button = Button(488, 500, "assets/options_button.png")
exit_button = Button(488, 600, "assets/exit_button.png")
back_button = Button(488, 600, "assets/back_button.png")
#----------------------------------------------- #

game_state = GameState(
    background_image, 
    title, 
    options, 
    start_button, 
    options_button, 
    exit_button, 
    back_button
)



# ------------- Game Loop ------------- #
while game_state.running:
    game_state.dt = clock.tick(60) / 1000
    #event handeler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False
        game_state.handle_game_state(event)

    game_state.update()
    game_state.draw(screen)
    pygame.display.flip()

pygame.quit()
