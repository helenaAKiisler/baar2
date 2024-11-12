#siia tulevad erinevad nupud vms

import pygame
from settings import WHITE, LIGHT_GREEN, DARK_GREEN, GREEN
from typing import Callable
pygame.font.init()  # Initsialiseerime Pygame'i fondisüsteemi enne FONT muutujat

TEXT_COLOR = pygame.Color(LIGHT_GREEN)
BUTTON_TEXT_COLOR = pygame.Color(DARK_GREEN)
BUTTON_COLOR = pygame.Color(LIGHT_GREEN)
BUTTON_HOVER_COLOR = pygame.Color(GREEN)
BUTTON_PADDING = 15

FONT = pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 25)


def initialize_font():
    global FONT
    FONT = pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 25)


class Button:
    def __init__(self, text, on_pressed):
        self.text = text
        self.on_pressed = on_pressed
        self.rect = pygame.Rect(0, 0, 200, 50)  # Nupu suurus
        self.color = (16, 72, 36)  #Tumeroheline
        self.text_surface = pygame.font.Font(None, 36).render(self.text, True, (255, 255, 255))

    def render(self, screen, position):
        self.rect.topleft = position  # Määrame nupu asukoha
        pygame.draw.rect(screen, self.color, self.rect)

        # Teksti renderdamine keskmesse
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def check_click(self, pos):
        """Kontrollib, kas nupp on klikitud."""
        if self.rect.collidepoint(pos):
            self.on_pressed()

    def handle_events(self, event):
        """Kontrollib, kas nupp on vajutatud."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):  # Kui hiir on nupu peal ja nupp on vajutatud
                if self.on_pressed:
                    self.on_pressed()  # Kutsub välja nuppudele määratud tegevuse

def draw_score(screen, font, score):
    score_text = font.render(f"Punktid: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

