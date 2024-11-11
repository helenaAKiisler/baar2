import sys

import pygame

from scene import Scene
from settings import DARK_GRAY, DARK_GREEN, LIGHT_GREEN
import ui
from game_level import GameLevel

class MainMenu(Scene):
    BACKGROUND_COLOR = pygame.Color(DARK_GREEN)

    def __init__(self, scene_switcher, game_title, screen):
        super().__init__(scene_switcher)
        self.scene_switcher = scene_switcher
        self.game_title = game_title
        self.screen = screen  # Salvestame screen objekti

        self.title = ui.FONT.render(game_title, True, ui.TEXT_COLOR)
        self.start_button = ui.Button("Start", on_pressed=lambda: self.scene_switcher("GameLevel", screen))
        self.quit_button = ui.Button("Quit", on_pressed=self.quit_scene)

    def render(self, screen: pygame.Surface):
        screen.fill(MainMenu.BACKGROUND_COLOR)
        screen.blit(self.title, ((screen.get_width() - self.title.get_width()) / 2, screen.get_height() * 0.2))

        self.quit_button.render(screen, (
            (screen.get_width() - self.quit_button.get_width()) / 2,
            screen.get_height() - self.quit_button.get_height() - 10))

        self.start_button.render(screen, (
            (screen.get_width() - self.start_button.get_width()) / 2,
            screen.get_height() - self.quit_button.get_height() - self.start_button.get_height() - 20))

    def handle_events(self, event):
        # Siin töötleme sündmused
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()