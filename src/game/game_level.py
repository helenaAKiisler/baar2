import pygame
import os
import random
from src.game import ui
from player import Player
from enemy import Enemy
from object import Glass, Table
from progress_bar import GameTimer
from scene import Scene
from settings import WIDTH, HEIGHT, GAME_DURATION
from bar import Bar


class GameLevel(Scene):
    BACKGROUND_COLOR = pygame.Color(101, 67, 33)

    def __init__(self, scene_switcher, level=1):
        super().__init__(scene_switcher)

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
        character_image_path = os.path.join(base_path, "assets", "designs", "character", "teenindus.mees2.png")
        player_image = pygame.image.load(character_image_path)

        # Mängija loome koos algpositsiooni ja pildiga
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
        """Seadistab leveli raskusastme ja elementide arvu vastavalt levelile."""
        table_count = min(5 + level, 10)  # Taseme kasvades suurendame lauaarvu
        glass_count = min(5 + 2 * level, 15)  # Taseme kasvades suurendame klaaside arvu
        enemy_count = min(1 + (level // 2), 5)  # Taseme kasvades suurendame vaenlaste arvu

        # Lisame lauad koos juhusliku positsiooniga
        for _ in range(table_count):
            x = random.randint(50, WIDTH - 100)
            y = random.randint(50, HEIGHT - 100)
            table = Table(x, y)
            self.tables.add(table)
            self.sprites.add(table)
            self.collision_layer.add(table)

        # Lisame klaasid
        for _ in range(glass_count):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            color, points = random.choice([((255, 0, 0), 1), ((0, 255, 0), 2), ((0, 0, 255), 3)])
            glass = Glass(x, y, color, points)
            self.glasses.add(glass)
            self.sprites.add(glass)

            # Lisame vaenlased koos juhusliku positsiooniga
            for _ in range(enemy_count):
                x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            enemy = Enemy(x, y)  # Lisame x ja y positsioonid
            self.enemies.add(enemy)
            self.sprites.add(enemy)

    def start(self):
        """Alustab levelit."""
        self.is_running = True
        self.game_timer = GameTimer()
        self.score = 0

    def update(self):
        """Uuendab leveli seisundit."""
        if self.game_timer.is_time_up():
            self.end_game()
            return

        delta = pygame.time.Clock().tick(30) / 1000.0
        self.player.update(delta)
        self.enemies.update(delta)

        self.check_collisions()
        self.check_win_condition()

    def check_collisions(self):
        """Kontrollib mängija ja klaaside või vaenlaste vahelisi kokkupõrkeid."""
        if self.carried_glasses < self.max_glasses:
            glasses_collected = pygame.sprite.spritecollide(self.player, self.glasses, True)
            self.carried_glasses += len(glasses_collected)

        if self.carried_glasses > 0 and self.player.rect.colliderect(self.bar.rect):
            self.score += self.carried_glasses * 2
            self.carried_glasses = 0

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