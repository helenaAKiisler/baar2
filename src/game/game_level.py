import sys

import pygame
import os
import random
from src.game import ui
from player import Player
from object import Glass, Table, Enemy
from progress_bar import GameTimer
from scene import Scene
from settings import WIDTH, HEIGHT, GAME_DURATION
from bar import Bar


class GameLevel(Scene):
    BACKGROUND_COLOR = pygame.Color(101, 67, 33)

    def __init__(self, scene_switcher, level=1):
        super().__init__(scene_switcher)
        self.is_running = True
        self.level = level
        self.quit_button = ui.Button("Quit", on_pressed=self.quit_scene)

        # Spraitide kihid
        self.collision_layer = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.glasses = pygame.sprite.Group()
        self.tables = pygame.sprite.Group()

        # Mängija pildi laadimine
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        character_image_path = os.path.join(base_path, "assets", "designs", "character", "mees", "teenindus.mees2.png")
        player_image = pygame.image.load(character_image_path)

        # Mängija loomine
        self.player = Player(WIDTH // 2, HEIGHT - 80, player_image)
        self.sprites.add(self.player)
        self.collision_layer.add(self.player)

        # Baar
        self.bar = Bar(WIDTH)
        self.sprites.add(self.bar)
        self.collision_layer.add(self.bar)

        # Taseme seadistamine
        self.setup_level(self.level)

        # Mängu muutujad
        self.game_timer = GameTimer()
        self.score = 0
        self.carried_glasses = 0
        self.max_glasses = 3

    def setup_level(self, level):
        """Seadistab leveli raskusastme ja elementide arvu."""
        table_count = min(5 + level, 10)  # Taseme kasvades suurendame lauaarvu
        glass_count = min(5 + 2 * level, 15)  # Taseme kasvades suurendame klaaside arvu
        enemy_count = min(1 + (level // 2), 5)  # Taseme kasvades suurendame vaenlaste arvu

        # Juhuslik paigutus ja kattuvuse vältimine laudade jaoks
        positions = []
        for _ in range(table_count):
            while True:
                x = random.randint(50, WIDTH - 100)
                y = random.randint(50, HEIGHT - 100)
                new_rect = pygame.Rect(x, y, 50, 50)  # 50x50 on laua suurus
                if not any(new_rect.colliderect(existing) for existing in positions):
                    table = Table(x, y)
                    self.tables.add(table)
                    self.sprites.add(table)
                    self.collision_layer.add(table)
                    positions.append(new_rect)
                    break

        # Klaaside paigutus
        for _ in range(glass_count):
            while True:
                x = random.randint(50, WIDTH - 50)
                y = random.randint(50, HEIGHT - 50)
                new_rect = pygame.Rect(x, y, 20, 20)  # Klaasi suurus
                if not any(new_rect.colliderect(existing) for existing in positions):
                    color, points = random.choice([((255, 0, 0), 1), ((0, 255, 0), 2), ((0, 0, 255), 3)])
                    glass = Glass(x, y, color, points)
                    self.glasses.add(glass)
                    self.sprites.add(glass)
                    positions.append(new_rect)
                    break

        # Vaenlaste paigutus
        for _ in range(enemy_count):
            while True:
                x = random.randint(50, WIDTH - 50)
                y = random.randint(50, HEIGHT - 50)
                new_rect = pygame.Rect(x, y, 30, 30)  # Vaenlase suurus
                if not any(new_rect.colliderect(existing) for existing in positions):
                    enemy = Enemy(x, y)
                    self.enemies.add(enemy)
                    self.sprites.add(enemy)
                    positions.append(new_rect)
                    break

    def check_collisions(self):
        """Kontrollib mängija ja klaaside või vaenlaste vahelisi kokkupõrkeid."""
        if self.carried_glasses < self.max_glasses:
            glasses_collected = pygame.sprite.spritecollide(self.player, self.glasses, True)
            for glass in glasses_collected:
                self.score += glass.points  # Lisab punktid skoorile klaasi väärtuse põhjal
            self.carried_glasses += len(glasses_collected)

        # Kui mängija viib klaasid baari juurde
        if self.carried_glasses > 0 and self.player.rect.colliderect(self.bar.rect):
            self.score += self.carried_glasses * 2
            self.carried_glasses = 0

        # Vaenlase kokkupõrke puhul kaotab mängija kaasaskantavad klaasid
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.carried_glasses = 0

    def check_win_condition(self):
        """Kontrollib, kas leveli võidutingimused on täidetud."""
        # Suurendame punktinõuet vastavalt leveli numbrile
        required_score = 10 + (self.level - 1) * 5
        if self.score >= required_score:
            print("Läbisid leveli!")
            self.end_game()

    def render(self, screen):
        """Kuvab leveli ekraanile."""
        screen.fill(self.BACKGROUND_COLOR)
        self.sprites.draw(screen)

        # Kui mäng on lõppenud, kuvatakse ekraanil lõpp-skoor
        if not self.is_running:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))

            end_text = pygame.font.Font(None, 48).render(f"Level {self.level} lõppenud!", True, (255, 255, 255))
            score_text = pygame.font.Font(None, 36).render(f"Skoor: {self.score}", True, (255, 255, 255))

            screen.blit(overlay, (0, 0))
            screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))

        # Mängu oleku kuvarid
        self.quit_button.render(screen, (50, 550))
        ui.draw_score(screen, pygame.font.Font(None, 36), self.score)
        self.game_timer.draw_progress_bar(screen)

    def end_game(self):
        """Lõpetab leveli ja suunab tagasi peamenüüsse või järgmisele levelile."""
        self.is_running = False
        if self.scene_switcher:
            if self.level < 5:
                self.scene_switcher("NextLevel")  # Näide järgmisele tasemele liikumisest
            else:
                self.scene_switcher("MainMenu")  # Pärast viimast levelit tagasi menüüsse

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def update(self):
        """Uuendab leveli seisundit."""
        if self.game_timer.is_time_up():
            self.end_game()
            return

        delta = self.game_timer.get_delta_time()

        # Käsitleme mängija liikumist
        keys = pygame.key.get_pressed()
        self.player.handle_movement(keys, self.tables, delta)

        # Uuendame vaenlasi ja kontrollime kokkupõrkeid
        self.enemies.update()

        # Kontrollime kokkupõrkeid ja võidutingimusi
        self.check_collisions()
        self.check_win_condition()