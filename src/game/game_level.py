import pygame

from src.game import ui
from player import Player
from scene import Scene

class GameLevel(Scene):
    BACKGROUND_COLOR = pygame.Color(101, 67, 33)
    #Siia tuleks lisada siis algne mängu leveli layout

    def __init__(self, scene_switcher):
        super().__init__(scene_switcher)

        self.quit_button = ui.Button("Quit", on_pressed=self.quit_scene)

        self.collision_layer = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.player = Player(self.collision_layer)

        self.previous_frame_time = 0
        self.running = True
        self.clock = pygame.time.Clock()

    def update(self):
        # self.clock.tick(30)
        frame_time = pygame.time.get_ticks()
        delta = (frame_time - self.previous_frame_time) / 1000.0
        self.previous_frame_time = frame_time

        if delta > 0.1:
            delta = 0

