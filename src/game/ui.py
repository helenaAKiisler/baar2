# Fonti initseerimine ja nuppude klass, mis sätestab ära erinevad nupud mängus.

import pygame
from settings import OFF_WHITE, LIGHT_GREEN, DARK_GREEN, GREEN
from typing import Callable
pygame.font.init()  # Initsialiseerime Pygame'i fondisüsteemi enne FONT muutujat

TEXT_COLOR = pygame.Color(152, 191, 161)
BUTTON_TEXT_COLOR = pygame.Color(16, 72, 36)
BUTTON_COLOR = pygame.Color(91, 139, 102)
BUTTON_HOVER_COLOR = pygame.Color(152, 191, 161)
BUTTON_PADDING = 15

FONT = pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 25)

def initialize_font():
    global FONT
    FONT = pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 25)

class Button(pygame.Surface):
    FONT = pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 25)
    def __init__(self, text, on_pressed: Callable):
        self.text = text
        self.on_pressed = on_pressed
        self.rect = pygame.Rect(0, 0, 150, 30)  # Nupu laiuse ja kõrguse määramine
        self.color = (91, 139, 102)  # Nupu värv
        self.text_surface = FONT.render(self.text, True, (16, 72, 36))
        self.is_down = False
        button_size = self.text_surface.get_rect().inflate(20, 20).size
        super().__init__(button_size)

    def render(self, screen: pygame.Surface, position):
        button_color = BUTTON_HOVER_COLOR if self.is_down else BUTTON_COLOR
        detection_rect = pygame.draw.rect(screen, button_color, pygame.Rect(position, self.get_size()))
        screen.blit(self.text_surface, (position[0] + 10, position[1] + 10))

        # Vajutamise tuvastamine
        if self.is_down and not pygame.mouse.get_pressed(3)[0]:
            self.on_pressed()

        self.is_down = pygame.mouse.get_pressed(3)[0] and detection_rect.collidepoint(pygame.mouse.get_pos())

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
    score_text = font.render(f"Points: {score}", True, OFF_WHITE)
    screen.blit(score_text, (10, 0))

