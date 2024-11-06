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

class Button(pygame.Surface):
    def __init__(self, button_text: str, on_pressed: Callable):
        global FONT
        if FONT is None:
            initialize_font()
        self.text = button_text
        self.on_pressed = on_pressed
        self.font_surface = FONT.render(button_text, True, BUTTON_TEXT_COLOR)
        self.is_down = False

        button_size = self.font_surface.get_rect().inflate(BUTTON_PADDING, BUTTON_PADDING).size
        super().__init__(button_size)

    def render(self, screen: pygame.Surface, position):
        is_mouse_pressed = pygame.mouse.get_pressed(3)[0]
        button_color = BUTTON_HOVER_COLOR if self.is_down else BUTTON_COLOR

        detection_rect = pygame.draw.rect(screen, button_color, pygame.Rect(position, self.get_size()))
        screen.blit(self.font_surface, (position[0] + BUTTON_PADDING / 2, position[1] + BUTTON_PADDING / 2))

        if self.is_down and not is_mouse_pressed:
            self.on_pressed()

        self.is_down = is_mouse_pressed and detection_rect.collidepoint(pygame.mouse.get_pos())

def draw_score(screen, font, score):
    score_text = font.render(f"Punktid: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_time(screen, font, time_left):
    time_text = font.render(f"Aega jäänud: {int(time_left)} s", True, WHITE)
    screen.blit(time_text, (10, 50))