# Määrab ära mängu klassi
import pygame
import sys
from progress_bar import GameTimer
from settings import BASE_GAME_DURATION
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        self.is_paused = False
        self.game_timer = GameTimer(BASE_GAME_DURATION)

    def start_game(self):
        """Algatab mängu ajastamise ja muud mängu algseaded."""
        self.game_timer = GameTimer(BASE_GAME_DURATION)  # Alustame mängu ajamõõdikut
        self.is_paused = False

    def toggle_pause(self):
        """Lülitab mängu pausile või pausilt välja."""
        self.is_paused = not self.is_paused
        self.game_timer.toggle_pause()

    def quit_game(self):
        """Lõpetab mängu ja sulgeb akna."""
        pygame.quit()
        sys.exit()




