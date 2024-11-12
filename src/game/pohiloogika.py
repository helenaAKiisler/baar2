import pygame
import sys
from settings import DARK_BROWN
from progress_bar import GameTimer
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        self.is_paused = False
        self.game_timer = GameTimer()  # game_timer tuleb määrata õigesti

    def start_game(self):
        """Algatab mängu ajastamise ja muud mängu algseaded."""
        self.game_timer = GameTimer()  # Alustame mängu ajamõõdikut
        self.is_paused = False

    def toggle_pause(self):
        """Lülitab mängu pausile või pausilt välja."""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.game_timer.toggle_pause()  # Peatame ajamõõdiku täitumise
        else:
            self.game_timer.toggle_pause()  # Jätkame ajamõõdiku täitumist

    def quit_game(self):
        """Lõpetab mängu ja sulgeb akna."""
        pygame.quit()
        sys.exit()

