import pygame
from settings import GLASS_SIZE, TABLE_SIZE

class Glass:
    def __init__(self, x, y, color, points):
        self.rect = pygame.Rect(x, y, GLASS_SIZE, GLASS_SIZE)
        self.color = color
        self.points = points

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_pickup(self, player, score):
        if self.rect.colliderect(player.rect):
            score += self.points
            return True, score  # Tagastame True, et klaas saaks eemaldada
        return False, score


class Table:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TABLE_SIZE, TABLE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, HALL, self.rect)