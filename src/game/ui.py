# Fonti initseerimine ja nuppude klass, mis sätestab ära erinevad nupud mängus.

import pygame
from settings import button_path, OFF_WHITE
from os import listdir
from os.path import isfile, join
from typing import Callable



class Button(pygame.Surface):
    def __init__(self, button, on_pressed: Callable):
        self.on_pressed = on_pressed
        self.is_down = False
        self.button = button
        self.button_image = pygame.image.load(join(button_path, (button + ".png")))
        self.button_hover_img = pygame.image.load(join(button_path, (button + "_pressed.png")))
        self.rect = self.button_image.get_rect()
        button_size = self.rect.size
        super().__init__(button_size)

    def render(self, screen: pygame.Surface, position):
        is_mouse_pressed = pygame.mouse.get_pressed(3)[0]
        button_img = self.button_hover_img if self.is_down else self.button_image
        detection_rect = pygame.draw.rect(screen, OFF_WHITE, pygame.Rect((position[0]+5, position[1]+5), (self.get_width()-10, self.get_height()-10)))
        screen.blit(button_img, (position[0], position[1]))

        # Vajutamise tuvastamine
        if self.is_down and not is_mouse_pressed:
            self.on_pressed()

        self.is_down = is_mouse_pressed and detection_rect.collidepoint(pygame.mouse.get_pos())

    def check_click(self, pos):
        """Kontrollib, kas nupp on klikitud."""
        if self.rect.collidepoint(pos):
            self.on_pressed()

    def handle_events(self, event):
        """Kontrollib, kas nupp on vajutatud."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):  # Kui hiir on nupu peal ja nupp on vajutatud
                if self.on_pressed:
                    self.on_pressed()  # Kutsub välja nuppudele määratud tegevuse

def draw_score(screen, font, score):
    score_text = font.render(f"Points: {score}", True, OFF_WHITE)
    screen.blit(score_text, (10, 0))

