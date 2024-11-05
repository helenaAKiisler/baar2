import time
import pygame
from settings import GAME_DURATION, VALGE, ROHELINE

class GameTimer:
    def __init__(self):
        self.start_time = time.time()
        self.paused_time = 0
        self.paused = False
        self.pause_start_time = 0

    def toggle_pause(self):
        if self.paused:
            # Kui mäng jätkub pausilt, uuendame `paused_time`, et pausil oldud aeg maha arvutada
            self.paused_time += time.time() - self.pause_start_time
            self.paused = False
        else:
            # Pausile minnes salvestame pausialguse aja
            self.pause_start_time = time.time()
            self.paused = True

    def get_time_left(self):
        if self.paused:
            # Kui mäng on pausil, tagastame järelejäänud aja viimase teadaoleva hetke põhjal
            return max(0, GAME_DURATION - (self.pause_start_time - self.start_time - self.paused_time))
        else:
            # Kui mäng ei ole pausil, arvestame kogu pausidel oldud aega maha
            current_time = time.time() - self.start_time - self.paused_time
            return max(0, GAME_DURATION - current_time)

    def draw_progress_bar(self, screen):
        time_left = self.get_time_left()
        progress_width = int((time_left / GAME_DURATION) * 200)
        pygame.draw.rect(screen, VALGE, (200, 10, 200, 20), 2)
        pygame.draw.rect(screen, ROHELINE, (200, 10, progress_width, 20))

    def is_time_up(self):
        return self.get_time_left() <= 0