# Määrab ära progressiriba ja selle muutumise mängu alustamisel pausile minekul ja lõpetamisel.
import time
import pygame
from settings import duration, OFF_WHITE, GREEN

class GameTimer:
    def __init__(self, duration=60):
        self.start_time = time.time()  # Mängu algusaeg
        self.duration = duration
        self.paused = False  # Paus alguses on välja lülitatud
        self.pause_start = None  # Pausi algusaeg
        self.elapsed_paused_time = 0  # Aeg, kui mäng on pausil
        self.last_time = pygame.time.get_ticks()  # Viimane aeg, et delta arvutada
        self.time_at_pause = self.duration  # Salvestame progressiriba hetke väärtuse pausi alguses

    # Lülitab pausi sisse ja välja.
    def toggle_pause(self):
        if self.paused:
            self.resume()  # Kui paus lõppeb, jätkame täitumist
        else:
            self.pause()  # Kui paus algab, peatame täitumise

    # Peatab ajamõõdiku täitumise.
    def pause(self):
        if not self.paused:
            self.paused = True
            self.pause_start = time.time()  # Salvestame pausi algusaja
            self.time_at_pause = self.get_time_left()  # Salvestame järelejäänud aja

    # Taaskäivitab ajamõõdiku täitumise pärast pausi.
    def resume(self):
        """Taaskäivitab ajamõõdiku täitumise pärast pausi."""
        if self.paused:
            self.paused = False
            self.elapsed_paused_time += time.time() - self.pause_start
            self.last_time = pygame.time.get_ticks() + 1  # Väldi null delta aega
            self.pause_start = None

    # Arvutab jäänud aja, võttes arvesse pausi kestust.
    def get_time_left(self):
        if self.paused:
            return self.time_at_pause  # Kui pausil, tagastame salvestatud aja
        return max(0, self.duration - (time.time() - self.start_time - self.elapsed_paused_time))

    # Kontrollib, kas aeg on läbi.
    def is_time_up(self):
        return self.get_time_left() <= 0  # Kui jäänud aeg on null või negatiivne, siis on aeg läbi

    # Arvutab aja muutuse viimase ja praeguse hetke vahel sekundites.
    def get_delta_time(self):
        if self.paused:
            return 0  # Kui paus on, ei liigu aeg edasi
        current_time = pygame.time.get_ticks()
        delta = (current_time - self.last_time) / 1000  # Sekundites
        self.last_time = current_time
        return delta

    # Kuvab progressiriba ekraanile vastavalt jäänud ajale.
    def draw_progress_bar(self, screen):
        time_left = self.get_time_left()
        progress_width = int((time_left / self.duration) * 200)

        # Kuvame progressiriba
        pygame.draw.rect(screen, OFF_WHITE, (200, 15, 200, 20), 2)  # Riba raam
        pygame.draw.rect(screen, GREEN, (200, 15, progress_width, 20))  # Täituv progressiriba
