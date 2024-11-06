import pygame
import random
from settings import WIDTH, HEIGHT, BLACK

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=100, y=100):  # Vaikimisi määrame x ja y väärtused
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        """Liigutab vaenlast allapoole. Kui jõuab ekraani alla, asetatakse tagasi üles."""
        self.rect.y += 10
        if self.rect.top > HEIGHT:
            self.reset_position()

    def reset_position(self):
        """Paigutab vaenlase uuesti üles ekraani algusesse juhusliku horisontaalse positsiooniga."""
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def draw(self, surface):
        """Joonistab vaenlase ekraanile."""
        surface.blit(self.image, self.rect)