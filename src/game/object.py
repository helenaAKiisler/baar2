import pygame
from settings import GLASS_SIZE, TABLE_SIZE, GRAY

class Glass(pygame.sprite.Sprite):
    def __init__(self, x, y, color, points):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Määrame klaasi suuruse
        self.image.fill(color)  # Määrame klaasi värvi vastavalt etteantud värvile
        self.rect = self.image.get_rect(topleft=(x, y))  # Seadistame asukoha
        self.points = points  # Määrame klaasi punktiväärtuse

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_pickup(self, player, score):
        #laiendan klaasi üleskorjamis/kokkupõrke ala esmalt
        pickup_area = self.rect.inflate(40, 40)

        if pickup_area.colliderect(player.rect):
            score += self.points
            return True, score  # Tagastame True, et klaas saaks eemaldada
        return False, score


class Table:
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Määrame laua suuruse
        self.image.fill((150, 75, 0))  # Valime lauale pruuni värvi
        self.rect = self.image.get_rect(topleft=(x, y))  # Seadistame asukoha

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)

class Enemy(pygame.sprite.Sprite):
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((30, 30))  # Määrame vaenlase suuruse
            self.image.fill((0, 0, 255))  # Valime vaenlasele sinise värvi
            self.rect = self.image.get_rect(topleft=(x, y))  # Seadistame asukoha