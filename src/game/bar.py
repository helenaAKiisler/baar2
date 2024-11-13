import pygame

from settings import DARK_BROWN, WIDTH

class Bar(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image = pygame.Surface((width, 50))  # Baar on laiem, kõrgus 50px
        self.image.fill((99, 102, 106))  # Baaril pruun värv
        self.rect = self.image.get_rect()

        # Paigutame baari ekraani ülaosas keskele
        self.rect.x = (WIDTH - width) // 2  # Baar on keskendatud horisontaalselt
        self.rect.y = 50  # Baar asub ekraani ülaservas, kuid natuke allpool