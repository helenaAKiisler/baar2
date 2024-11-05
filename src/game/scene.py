from abc import ABC

import pygame

class Scene(ABC):

    def __init__(self, scene_switcher):
        self.is_running = True
        self.scene_switcher = scene_switcher

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_scene()

    def quit_scene(self):
        self.is_running = False

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        pass