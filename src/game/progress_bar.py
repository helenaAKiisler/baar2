import time
import pygame
from settings import GAME_DURATION, WHITE, GREEN

class GameTimer:
    def __init__(self):
        self.start_time = time.time()  # Mängu algusaeg
        self.paused_time = 0  # Pausi ajal möödunud aeg
        self.paused = False
        self.pause_start = None  # Pausi algusaeg
        self.last_time = pygame.time.get_ticks()

    def toggle_pause(self):
        """Lülitab mängu pausile ja pausilt tagasi."""
        if self.paused:
            # Pausi lõpp, arvutame aega
            self.paused_time += time.time() - self.pause_start
            self.pause_start = None
        else:
            # Pausi algus
            self.pause_start = time.time()
        self.paused = not self.paused

    def is_time_up(self):
        """Kontrollib, kas mängu aeg on läbi."""
        return self.get_time_left() <= 0

    def get_time_left(self):
        """Arvutab järelejäänud aja, võttes arvesse pausi."""
        if self.paused:
            # Kui paus on, aeg ei liigu edasi
            current_time = self.pause_start - self.start_time - self.paused_time
        else:
            # Kui mäng ei ole pausil, arvuta kulunud aeg
            current_time = time.time() - self.start_time - self.paused_time
        return max(0, GAME_DURATION - current_time)

    def get_delta_time(self):
        """Arvutab aja muutuse viimase ja praeguse hetke vahel sekundites."""
        if self.paused:
            return 0  # Kui paus on, ei liigu aeg edasi
        current_time = pygame.time.get_ticks()
        delta = (current_time - self.last_time) / 1000.0  # Sekundites
        self.last_time = current_time
        return delta

    def draw_progress_bar(self, screen):
        """Kuvab progressiriba ekraanile vastavalt järelejäänud ajale."""
        if screen is None:
            print("Error: screen is None!")
            return  # Kui screen on None, siis lõpetame funktsiooni täitmise

        if self.paused:
            # Kui paus on, täidame progressiriba täis
            pygame.draw.rect(screen, WHITE, (200, 10, 200, 20), 2)  # Riba raam
            pygame.draw.rect(screen, GREEN, (200, 10, 200, 20))  # Täis progressiriba
        else:
            # Kui mäng ei ole pausil, täidame progressiriba vastavalt jäänud ajale
            time_left = self.get_time_left()
            progress_width = int((time_left / GAME_DURATION) * 200)  # Progressiriba laius
            pygame.draw.rect(screen, WHITE, (200, 10, 200, 20), 2)  # Riba raam
            pygame.draw.rect(screen, GREEN, (200, 10, progress_width, 20))  # Täituv progressiriba

