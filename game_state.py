import pygame
import pytmx
from sprite import *
from map import TiledMap, Camera, Obstacle


class GameState:
    def __init__(self, background_image, title_image, options_title, start_button, options_button, exit_button, back_button):
        self.state = "title"
        self.running = True

        self.background_image = background_image
        self.title_image = title_image
        self.options_title = options_title

        self.start_button = start_button
        self.options_button = options_button
        self.exit_button = exit_button
        self.back_button = back_button

        self.dt = 0
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        # --- tile map ---
        self.map = TiledMap("maps/map1.tmx") 
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        
        for obj in self.map.tmxdata.objects:
            if obj.name == "wall":
                Obstacle(self, obj.x, obj.y, obj.width, obj.height)

        self.player = Player(self, 5, 2000)
        self.camera = Camera(self.map.width, self.map.height)

    def handle_game_state(self, event):
        if self.state == "title":
            if self.start_button.is_clicked(event):
                self.state = "game"
            if self.options_button.is_clicked(event):
                self.state = "options"
            if self.exit_button.is_clicked(event):
                self.running = False

        elif self.state == "game":
            if self.back_button.is_clicked(event):
                self.state = "title"

        elif self.state == "options":
            if self.back_button.is_clicked(event):
                self.state = "title"

    def update(self):
        if self.state == "game":
            self.all_sprites.update()
            self.camera.update(self.player)

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))

        if self.state == "title":
            screen.blit(self.title_image, self.title_image.get_rect(midtop=(640, 100)))
            self.start_button.draw(screen)
            self.options_button.draw(screen)
            self.exit_button.draw(screen)

        elif self.state == "game":
            screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
            for sprite in self.all_sprites:
                screen.blit(sprite.image, self.camera.apply(sprite))
            

        elif self.state == "options":
            screen.blit(self.options_title, self.options_title.get_rect(midtop=(640, 50)))
            self.back_button.draw(screen)