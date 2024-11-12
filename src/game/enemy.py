import pygame
import random
from settings import WIDTH, HEIGHT, BLACK

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Vaenlase suurus
        self.image.fill((255, 0, 0))  # Vaenlane on punane
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """Vaenlase liikumine (liigub random suunas või mängija poole)."""
        self.rect.x += random.randint(-2, 2)  # Liikumine horisontaalses suunas
        self.rect.y += random.randint(-2, 2)  # Liikumine vertikaalses suunas