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

    def handle_events(self):
        """Käsitleb kasutaja sisendit ja sündmusi."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Kui vajutatakse 'A', käivitatakse mäng
                    self.start_game()
                elif event.key == pygame.K_p:  # Kui vajutatakse 'P', lülitatakse paus sisse või välja
                    self.toggle_pause()
                elif event.key == pygame.K_q:  # 'Q' lõpetamiseks
                    self.quit_game()
                elif event.key == pygame.K_c and self.is_paused:  # 'C' jätkamiseks, kui mäng on pausil
                    self.toggle_pause()
