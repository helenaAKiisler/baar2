import time
import pygame
from settings import GAME_DURATION, WHITE, GREEN

class GameTimer:
    def __init__(self):
        # Algväärtustused mängu aja ja pausiseisundi jaoks
        self.start_time = time.time()
        self.paused_time = 0  # Pausi ajal kogunenud aeg
        self.paused = False
        self.pause_start = None  # Pausi algusaeg

    def toggle_pause(self):
        """Lülitab mängu pausile ja pausilt tagasi."""
        if self.paused:
            # Kui paus lõppeb, arvuta pausile kulunud aeg
            self.paused_time += time.time() - self.pause_start
            self.pause_start = None
        else:
            # Pausi alustamine
            self.pause_start = time.time()
        self.paused = not self.paused

    def is_time_up(self):
        """Kontrollib, kas mängu aeg on läbi."""
        return self.get_time_left() <= 0

    def get_time_left(self):
        """Arvutab järelejäänud aja, võttes arvesse pausi kestust."""
        if self.paused:
            # Kui mäng on pausil, ei arvesta täiendavat kulunud aega
            current_time = self.pause_start - self.start_time - self.paused_time
        else:
            # Kui mäng ei ole pausil, arvuta kulunud aeg
            current_time = time.time() - self.start_time - self.paused_time
        return max(0, GAME_DURATION - current_time)

    def draw_progress_bar(self, screen):
        """Kuvab progressiriba ekraanile vastavalt järelejäänud ajale."""
        time_left = self.get_time_left()
        progress_width = int((time_left / GAME_DURATION) * 200)  # Progressiriba laius
        pygame.draw.rect(screen, WHITE, (200, 10, 200, 20), 2)  # Riba raam
        pygame.draw.rect(screen, (GREEN), (200, 10, progress_width, 20))  # Täituv progressiriba