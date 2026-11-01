import pygame
import pytmx
from global_variables import *


class TiledMap:
    def __init__(self, filename):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight

    def render(self, surface):
        tw = self.tmxdata.tilewidth
        th = self.tmxdata.tileheight
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * tw, y * th))

    def make_map(self):
        surface = pygame.Surface((self.width, self.height)).convert()
        self.render(surface)
        return surface


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        game.walls.add(self)


class Camera:
    def __init__(self, map_width, map_height):
        self.camera = pygame.Rect(0, 0, map_width, map_height)
        self.width = map_width
        self.height = map_height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2

        if self.width <= SCREEN_WIDTH:
            x = (SCREEN_WIDTH - self.width) // 2
        else:
            x = min(0, x)                          
            x = max(-(self.width - SCREEN_WIDTH), x)   

        if self.height <= SCREEN_HEIGHT:
            y = (SCREEN_HEIGHT - self.height) // 2
        else:
            y = min(0, y)                          
            y = max(-(self.height - SCREEN_HEIGHT), y) 

        self.camera = pygame.Rect(x, y, self.width, self.height)