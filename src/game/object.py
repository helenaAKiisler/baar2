import pygame
from settings import GLASS_SIZE, TABLE_SIZE, GRAY, RED
import random

class Glass(pygame.sprite.Sprite):
    def __init__(self, x, y, color, points):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((20, 20))  # Määrame klaasi suuruse
        self.image.fill(color)  # Määrame klaasi värvi vastavalt etteantud värvile
        self.rect = self.image.get_rect(topleft=(x, y))  # Seadistame asukoha
        self.points = points  # Määrame klaasi punktiväärtuse

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_pickup(self, player, score):
        # laiendan klaasi üleskorjamis/kokkupõrke ala
        pickup_area = self.rect.inflate(50, 50)

        if pickup_area.colliderect(player.rect):
            score += self.points
            return True, score  # Tagastame True, et klaas saaks eemaldada
        return False, score

class Table(pygame.sprite.Sprite):  # Lisame pärimise pygame.sprite.Sprite klassist
    def __init__(self, x, y):
        super().__init__()  # Kutsume Sprite konstruktori
        self.image = pygame.Surface((50, 50))  # Määrame laua suuruse
        self.image.fill((150, 75, 0))  # Valime lauale pruuni värvi
        self.rect = self.image.get_rect(topleft=(x, y))  # Seadistame asukoha

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)

class Enemy(pygame.sprite.Sprite):
    BASE_SPEED = 50
    def __init__(self, x, y, image):
        super().__init__()
#        self.image = pygame.Surface((30, 30))  # Vaenlase suurus
#        self.image.fill(RED)  # Vaenlane on punane
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """Vaenlase liikumine (liigub random suunas või mängija poole)."""
        self.rect.x += random.randint(-2, 2)  # Liikumine horisontaalses suunas
        self.rect.y += random.randint(-2, 2)  # Liikumine vertikaalses suunas

    def draw(self, surface):
        surface.blit(self.image, self.rect)