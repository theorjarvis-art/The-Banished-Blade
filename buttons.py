import pygame

class Button: #handles buttons 
    def __init__(self, x, y, image_path, hover_scale = 1.08):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        w, h = self.image.get_size()
        self.hover_image = pygame.transform.scale(self.image, (int(w * hover_scale), int(h * hover_scale)))

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, event): # checks if the button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if self.rect.collidepoint(event.pos):
                return True
            return False

    def draw(self, screen):    
        if self.is_hovered():
            hover_rect = self.hover_image.get_rect(center=self.rect.center) # keeps englarged image centered
            screen.blit(self.hover_image, hover_rect)
        else:
            screen.blit(self.image, self.rect)