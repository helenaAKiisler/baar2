import time
import pygame
from settings import GAME_DURATION, WHITE, GREEN

import time
import pygame
from settings import GAME_DURATION, WHITE, GREEN

class GameTimer:
    def __init__(self):
        self.start_time = time.time()  # Mängu algusaeg
        self.paused_time = 0  # Pausi ajal möödunud aeg
        self.paused = False  # Paus alguses on välja lülitatud
        self.pause_start = None  # Pausi algusaeg
        self.elapsed_paused_time = 0  # Aeg, kui mäng on pausil
        self.last_time = pygame.time.get_ticks()  # Viimane aeg, et delta arvutada
        self.current_time = 0  # Üldine aeg, mis on möödunud
        self.time_at_pause = 0  # Salvestame progressiriba hetke väärtuse pausi alguses

    def toggle_pause(self):
        """Lülitab pausi sisse ja välja."""
        if self.paused:
            self.resume()  # Kui paus lõppeb, jätkame täitumist
        else:
            self.pause()  # Kui paus algab, peatame täitumise

    def pause(self):
        """Peatab ajamõõdiku täitumise."""
        self.paused = True
        self.pause_start = time.time()  # Salvestame pausi algusaja

    def resume(self):
        """Taaskäivitab ajamõõdiku täitumise pärast pausi."""
        if self.pause_start is not None:  # Veenduge, et paus on algatatud
            self.paused = False
            self.elapsed_paused_time += time.time() - self.pause_start  # Arvutame, kui kaua paus kestis
            self.start_time = time.time() - self.elapsed_paused_time  # Jätkame samalt kohalt
            self.pause_start = None  # Pärast taaskäivitamist nullime pause_starti

    def get_time_left(self):
        """Arvutab jäänud aja, võttes arvesse pausi kestust."""
        if self.paused:
            return self.time_at_pause  # Kui paus, siis progressiriba ei täitu
        return max(0, GAME_DURATION - (time.time() - self.start_time - self.elapsed_paused_time))

    def is_time_up(self):
        """Kontrollib, kas aeg on läbi."""
        return self.get_time_left() <= 0  # Kui jäänud aeg on null või negatiivne, siis on aeg läbi

    def get_delta_time(self):
        """Arvutab aja muutuse viimase ja praeguse hetke vahel sekundites."""
        if self.paused:
            return 0  # Kui paus on, ei liigu aeg edasi
        current_time = pygame.time.get_ticks()
        delta = (current_time - self.last_time) / 1000.0  # Sekundites
        self.last_time = current_time
        return delta

    def draw_progress_bar(self, screen):
        """Kuvab progressiriba ekraanile vastavalt jäänud ajale."""
        time_left = self.get_time_left()

        # Arvutame progressiriba täitumise protsendi
        progress_width = int((time_left / GAME_DURATION) * 200)  # Progressiriba laius

        # Kui paus on sisse lülitatud, siis ei liigu progressiriba
        if self.paused:
            # Pausi ajal täitumine seisab, progressiriba ei liigu edasi
            progress_width = int(self.time_at_pause)

        # Kuvame progressiriba
        pygame.draw.rect(screen, WHITE, (200, 10, 200, 20), 2)  # Riba raam
        pygame.draw.rect(screen, GREEN, (200, 10, progress_width, 20))  # Täituv progressiriba
