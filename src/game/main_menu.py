import pygame

from scene import Scene
from settings import DARK_GRAY, DARK_GREEN, LIGHT_GREEN

class MainMenu(Scene):
    BACKGROUND_COLOR = pygame.Color(DARK_GREEN)

    def __init__(self, scene_switcher, game_title):
        super().__init__(scene_switcher)

        self.title
