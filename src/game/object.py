import pygame
from settings import GLASS_SIZE, TABLE_SIZE, GRAY

class Glass:
    def __init__(self, x, y, color, points):
        self.rect = pygame.Rect(x, y, GLASS_SIZE, GLASS_SIZE)
        self.color = color
        self.points = points

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
        self.rect = pygame.Rect(x, y, TABLE_SIZE, TABLE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)