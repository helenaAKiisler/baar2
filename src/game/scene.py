# Stseenide vahetamise klass. Võimaldab vahetada ja eristada Main Menu ja Game levelit erinevate stseenidena.
from abc import ABC

import pygame

class Scene(ABC):

    def __init__(self, scene_switcher):
        self.scene_switcher = scene_switcher  # Edastage scene_switcher, kui on vajalik
        self.is_running = True

    def handle_events(self):
        pass

    def quit_scene(self):
        self.is_running = False

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        pass
