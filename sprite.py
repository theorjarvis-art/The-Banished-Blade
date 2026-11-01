import pygame
from global_variables import *

class SpriteSheet:
    def __init__(self, sheet, width, height):
        self.sheet = sheet
        self.width = width
        self.height = height

    def get_sprite(self, col, row):
        """Cut one frame out of the sheet by column and row."""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0),
                   (col * self.width, row * self.height, self.width, self.height))
        return image

    def get_row(self, row, count):
        return [self.get_sprite(col, row) for col in range(count)]


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # --- animation setup ---
        sheet_image = pygame.image.load(PLAYER_SHEET).convert_alpha()
        sheet = SpriteSheet(sheet_image, FRAME_W, FRAME_H)
        size = (int(FRAME_W * PLAYER_SCALE), int(FRAME_H * PLAYER_SCALE))
        self.animations = {
            "down": [pygame.transform.scale(f, size) for f in sheet.get_row(ROW_DOWN, FRAMES_PER_ROW)],
            "left": [pygame.transform.scale(f, size) for f in sheet.get_row(ROW_LEFT, FRAMES_PER_ROW)],
            "right": [pygame.transform.scale(f, size) for f in sheet.get_row(ROW_RIGHT, FRAMES_PER_ROW)],
            "up": [pygame.transform.scale(f, size) for f in sheet.get_row(ROW_UP, FRAMES_PER_ROW)],
        }
        self.facing = "down"
        self.frame = 0
        self.anim_timer = 0
        self.moving = False

        self.image = self.animations[self.facing][0]
        self.rect = self.image.get_rect()

        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.topleft = (self.x, self.y)

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def animate(self):
        self.moving = self.vx != 0 or self.vy != 0

     
        if self.vx < 0:
            self.facing = "left"
        elif self.vx > 0:
            self.facing = "right"
        elif self.vy < 0:
            self.facing = "up"
        elif self.vy > 0:
            self.facing = "down"

        frames = self.animations[self.facing]

        if self.moving:
            self.anim_timer += self.game.dt
            if self.anim_timer >= ANIM_TIME:
                self.anim_timer = 0
                self.frame = (self.frame + 1) % len(frames)
        else:
            
            self.frame = 0
            self.anim_timer = 0

        self.image = frames[self.frame]

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.animate()   # uses the velocity before collisions zero it out
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

        # keep the player inside the map
        self.x = max(0, min(self.x, self.game.map.width - self.rect.width))
        self.y = max(0, min(self.y, self.game.map.height - self.rect.height))
        self.rect.topleft = (self.x, self.y)