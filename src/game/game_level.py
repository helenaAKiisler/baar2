import pygame

from src.game import ui
from player import Player
from enemy import Enemy
from object import Glass, Table
from progress_bar import GameTimer
from scene import Scene
from settings import GAME_DURATION
from bar import Bar
#from src.game.main import table, glass, enemy
from src.game.settings import WIDTH, HEIGHT


class GameLevel(Scene):
    BACKGROUND_COLOR = pygame.Color(101, 67, 33)
    #Siia tuleks lisada siis algne mängu leveli layout

    def __init__(self, scene_switcher):
        super().__init__(scene_switcher)

        self.quit_button = ui.Button("Quit", on_pressed=self.quit_scene)

        self.collision_layer = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.player = Player(self.collision_layer)
        self.enemies = pygame.sprite.Group()
        self.glasses = pygame.sprite.Group()
        self.tables = pygame.sprite.Group()

        self.bar = Bar(WIDTH)

        self.setup_level(WIDTH, HEIGHT)

        self.game_timer = GameTimer()
        self.score = 0
        self.carried_glasses = 0
        self.max_glasses = 3

    def setup_level(self):
        #algne mängu layout, mitu klaasi on, mitu lauda ja mitu klienti/vaenlast
        self.sprites.add(self.bar)
        self.collision_layer.add(self.bar)
        for _ in range(5):
            table = Table()
            self.tables.add(table)
            self.sprites.add(table)
            self.collision_layer.add(table)

        for _ in range(5):
            glass = Glass()
            self.glasses.add(glass)
            self.sprites.add(glass)

        for _ in range(1):
            enemy = Enemy()
            self.enemies.add(enemy)
            self.sprites.add(enemy)

    def start(self):
        self.is_running = True
        self.game_timer = GameTimer()
        self.score = 0

    def update(self):
        if self.game_timer.is_time_up():
            self.end_game()
            return

        delta = pygame.time.Clock().tick(30) / 1000.0
        self.player.update(delta)
        self.enemies.update(delta)

        self.check_collisions()
        self.check_win_condition()

        if self.game_timer.is_time_up():
            self.end_game()

    def check_collisions(self):
        if self.carried_glasses < self.max_glasses:
            glasses_collected = pygame.sprite.spritecollide(self.player, self.glasses, True)
            self.carried_glasses += len(glasses_collected)

        if self.carried_glasses > 0 and self.player.rect.colliderect(self.bar.rect):
            self.score += self.carried_glasses * 2
            self.carried_glasses = 0

        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.carried_glasses = 0

    def check_win_condition(self):
        if self.score >= 10: #praegu panin miinimum punkti summaks 10
            print("Läbisid leveli!")
            self.end_game()

    def render(self, screen):
        screen.fill(self.BACKGROUND_COLOR)
        self.sprites.draw(screen)

        self.quit_button.render(screen, (50, 550))
        ui.draw_score(screen, pygame.font.Font(None, 36), self.score)
        self.game_timer.draw_progress_bar(screen)

    def end_game(self):
        self.running = False
        if self.scene_switcher:
            self.scene_switcher("MainMenu")



