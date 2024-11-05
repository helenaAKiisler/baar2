#siia tulevad erinevad nupud vms
import pygame
from settings import WHITE, LIGHT_GREEN, DARK_GREEN, GREEN
from typing import Callable

TEXT_COLOR = pygame.Color(LIGHT_GREEN)

BUTTON_TEXT_COLOR = pygame.Color(DARK_GREEN)
BUTTON_COLOR = pygame.Color(LIGHT_GREEN)
BUTTON_HOVER_COLOR = pygame.Color(GREEN)
BUTTON_PADDING = 15

FONT: pygame.font.Font

def initialize_font():
    global FONT
    FONT = pygame.font.Font("assets/font/Inknut-Antiqua")

def draw_score(screen, font, score):
    score_text = font.render(f"Punktid: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_time(screen, font, time_left):
    time_text = font.render(f"Aega jäänud: {int(time_left)} s", True, WHITE)
    screen.blit(time_text, (10, 50))