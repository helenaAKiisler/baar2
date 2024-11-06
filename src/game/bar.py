import pygame

from settings import DARK_BROWN, WIDTH

class Bar(pygame.sprite.Sprite):
    def __init__(self, WIDTH):
        super().__init__()
        self.image = pygame.Surface((100, 40))
        self.image.fill((139, 69, 19))
        self.rect = self.image.get_rect(midtop=(WIDTH // 2, 10))