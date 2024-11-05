#siia tulevad erinevad nupud vms
import pygame
from settings import VALGE

def draw_score(screen, font, score):
    score_text = font.render(f"Punktid: {score}", True, VALGE)
    screen.blit(score_text, (10, 10))

def draw_time(screen, font, time_left):
    time_text = font.render(f"Aega jäänud: {int(time_left)} s", True, VALGE)
    screen.blit(time_text, (10, 50))