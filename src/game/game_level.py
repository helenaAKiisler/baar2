import sys

import pygame
import os
import random
from src.game import ui
from player import Player
from object import Glass, Table, Enemy
from progress_bar import GameTimer
from scene import Scene
from settings import WIDTH, HEIGHT, DARK_BROWN, GAME_DURATION
from bar import Bar


class GameLevel(Scene):
    BACKGROUND_COLOR = DARK_BROWN
    def __init__(self, scene_switcher, screen, level=1):
        super().__init__(scene_switcher)
        self.screen = screen
        self.level = level
        self.is_running = True
        self.quit_button = ui.Button("Quit", on_pressed=self.quit_game)
        self.continue_button = ui.Button("Continue", on_pressed=self.resume_game)
        self.score = 0
        self.carried_glasses = 0
        self.max_glasses = 3


        # Lisame kollisioonide kihid ja muud spraitide grupid
        self.collision_layer = pygame.sprite.Group()  # SIIN MÄÄRAME KOLLISIOONI KIHID
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.glasses = pygame.sprite.Group()
        self.tables = pygame.sprite.Group()

        # Spraitide kihid
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.tables = pygame.sprite.Group()

        # Mängija pildi määramine
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        character_image_path = os.path.join(base_path, "assets", "designs", "character", "mees", "teenindus.mees2.png")
        player_image = pygame.image.load(character_image_path)

        enemy_image_path = os.path.join(base_path, "assets", "designs", "character", "naine", "idle.png")
        enemy_image = pygame.image.load(enemy_image_path)


        # Mängija loomine
        self.player = Player(WIDTH // 2, HEIGHT - 80, player_image)
        self.sprites.add(self.player)

        self.enemy = Enemy(200, 80, enemy_image)

        # Baar
        self.bar = Bar(200)  # Baar väiksem kui ekraani laius
        self.sprites.add(self.bar)

        # Pausi seaded
        self.paused = False
        self.game_timer = GameTimer()
        self.continue_button = ui.Button("Continue", on_pressed=self.resume_game)

        # Startides ei ole nupp nähtav
        self.continue_button.visible = False

        self.setup_level(level)


    def setup_level(self, level):
        """Seadistab taseme raskusastme ja muud elemendid."""
        table_count = min(5 + level, 10)  # Taseme raskusaste
        glass_count = min(5 + 2 * level, 15)
        enemy_count = min(1 + (level // 2), 5)

        # Paigutame lauad ja klaasid, tagame et lauad ei ole üksteise peal ega üksteise kõrval
        positions = []
        for _ in range(table_count):
            while True:
                x = random.randint(50, WIDTH - 100)
                y = random.randint(50, HEIGHT - 200)
                new_rect = pygame.Rect(x, y, 50, 50)  # 50x50 on laua suurus
                if not any(new_rect.colliderect(existing) for existing in positions):
                    table = Table(x, y)
                    self.tables.add(table)
                    self.sprites.add(table)
                    self.collision_layer.add(table)
                    positions.append(new_rect)
                break

        # Klaaside paigutus
        glass_types = [{"color": "black", "points": 1}, {"color": "red", "points": 2}, {"color": "green", "points": 3}]
        for table in self.tables:
            for i in range(3):  # Veenduge, et iga laud saab kuni 3 klaasi
                x_offset = 10 + (i * 30) if i < 2 else 25
                y_offset = 10 if i < 2 else 40
                glass_x = table.rect.x + x_offset
                glass_y = table.rect.y + y_offset
                color, points = random.choice([((255, 0, 0), 1), ((0, 255, 0), 2), ((0, 0, 255), 3)])
                glass = Glass(glass_x, glass_y, color, points)
                self.glasses.add(glass)
                self.sprites.add(glass)
                positions.append(glass.rect)

        for _ in range(1):
            self.enemies.add(self.enemy)
            self.sprites.add(self.enemy)


    def handle_events(self, event):
        """Mängu sündmuste käsitlemine."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Kui vajutatakse P, siis lülitame pausi sisse või välja
                self.toggle_pause()
        if event.type == pygame.MOUSEBUTTONDOWN:  # Kui vajutatakse hiirega nupp
            if self.quit_button.rect.collidepoint(event.pos):  # Kui vajutatakse Quit nuppu
                self.quit_game()
            if self.continue_button.rect.collidepoint(event.pos):  # Kui vajutatakse Continue nuppu
                self.continue_game()

    def toggle_pause(self):
        """Lülitab pausi sisse ja välja."""
        if self.paused:
            self.resume_game()
        else:
            self.pause_game()

    def pause_game(self):
        """Pausib mängu ja kuvab 'Continue' nupu."""
        self.paused = True
        self.continue_button.visible = True  # Kuvab 'Continue' nupu

        # Loome läbipaistva musta kihi ekraanile, et teha ekraan udune
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)  # Set transparency of the overlay (150 makes it semi-transparent)
        overlay.fill((0, 0, 0))  # Fill with black color for the blur effect
        self.screen.blit(overlay, (0, 0))  # Render the overlay to the screen

    def show_continue_button(self):
        self.continue_button.visible = True

    def hide_continue_button(self):
        self.continue_button.visible = False

    def resume_game(self):
        """Taaskäivitab mängu pärast pausi."""
        self.paused = False
        self.continue_button.visible = False  # Peidab 'Continue' nupu

    def update(self):
        """Uuendab leveli seisundit."""
        if self.game_timer.is_time_up():
            self.quit_scene()
            return

        delta = self.game_timer.get_delta_time()  # Arvutame aja muutuse

        # Käsitleme mängija liikumist
        keys = pygame.key.get_pressed()
        self.player.handle_movement(keys, self.tables, delta)  # Edastame kõik vajalikud argumendid

        # Uuendame vaenlasi ja kontrollime kokkupõrkeid
        self.enemies.update()

        # Kontrollime kokkupõrkeid ja võidutingimusi
        self.check_collisions()
        self.check_win_condition()

        # Pausi ajal progressiriba ei täitu edasi
        self.game_timer.draw_progress_bar(self.screen)

    def continue_game(self):
        """Jätkab mängu pärast pausi."""
        self.paused = False
        self.continue_button.is_visible = False  # Peidab 'Continue' nupu
        self.game_timer.resume()  # Taaskäivitab mängu ajamõõdiku

    def render(self, screen):
        """Renderdab mängu ekraanile."""
        screen.fill(self.BACKGROUND_COLOR)  # Taust on pruun
        self.sprites.draw(screen)

        # Kui mäng on pausil, kuvatakse must ekraan ja 'Continue' nupp
        if self.paused:
            # Must taust ja overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)  # Läbipaistev must kiht
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Kuvame "Continue" nupu ekraani keskele
            continue_button_position = (WIDTH // 2 - self.continue_button.rect.width // 2, HEIGHT // 2 - self.continue_button.rect.height // 2)
            self.continue_button.render(screen, continue_button_position)
        else:
            # Joonista mängu tavaline ekraan
            self.sprites.draw(screen)
            self.game_timer.draw_progress_bar(screen)
            ui.draw_score(screen, pygame.font.Font(None, 36), self.score)

        ui.draw_score(screen, pygame.font.Font(None, 36), self.score)  # Kuvab skoori

        # Quit nupp paigutatud paremasse nurgasse
        quit_button_position = (WIDTH - 250, HEIGHT - 70)
        self.quit_button.render(screen, quit_button_position)

    def quit_game(self):
        """Mängu lõpetamine"""
        pygame.quit()
        sys.exit()

    def check_collisions(self):
        """Kontrollib mängija ja klaaside või vaenlaste vahelisi kokkupõrkeid."""
        if self.carried_glasses < self.max_glasses:
            glasses_collected = pygame.sprite.spritecollide(self.player, self.glasses, True)
            for glass in glasses_collected:
                self.score += glass.points  # Lisab punktid skoorile klaasi väärtuse põhjal
            self.carried_glasses += len(glasses_collected)

        # Kui mängija viib klaasid baari juurde
        if self.carried_glasses > 0 and self.player.rect.colliderect(self.bar.rect):
            self.score += self.carried_glasses
            self.carried_glasses = 0

        # Vaenlase kokkupõrke puhul kaotab mängija kaasaskantavad klaasid
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.carried_glasses = 0

    def check_win_condition(self):
        """Kontrollib, kas mängija on võitnud taseme."""
        pass