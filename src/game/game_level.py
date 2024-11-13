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
from src.game.main import enemy_image


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

        # Määrame baasi tee (base_path) kõigis meetodites kasutamiseks
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Lisame kollisioonide kihid ja muud spraitide grupid
        self.collision_layer = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.glasses = pygame.sprite.Group()
        self.tables = pygame.sprite.Group()

        # Baar
        self.bar = Bar(200)  # Baar väiksem kui ekraani laius
        self.sprites.add(self.bar)

        # Mängija pildi määramine
        character_image_path = os.path.join(self.base_path, "assets", "designs", "character", "mees", "teenindus.mees2.png")
        player_image = pygame.image.load(character_image_path)

        # Mängija loomine
        self.player = Player(WIDTH // 2, HEIGHT - 80, player_image, self.bar)
        self.sprites.add(self.player)

        # Laadige vaenlase pilt enne objekti loomist
        enemy_image_path = os.path.join(self.base_path, "assets", "designs", "character", "naine", "idle.png")
        enemy_image = pygame.image.load(enemy_image_path)  # Laadige pilt

        # Loome vaenlase, edastades pildi
        self.enemy = Enemy(random.randint(50, WIDTH - 100), random.randint(50, HEIGHT - 100), enemy_image, self.tables)

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

        # Defineeri kindlad kohad lauadeks (koordinaadid)
        predefined_table_positions = [
            (100, 100), (200, 200), (300, 300), (400, 100), (500, 200),
            (100, 400), (200, 500), (300, 400), (400, 500), (500, 400)
        ]

        # Paigutame lauad kindlatesse kohtadesse, kontrollides, et nad ei oleks liiga lähedal baari
        positions = []
        for i in range(table_count):
            while True:
                x, y = predefined_table_positions[i]
                new_rect = pygame.Rect(x, y, 50, 50)  # 50x50 on laua suurus

                # Kontrollime, et laud ei ole liiga lähedal baari
                if new_rect.colliderect(self.bar.rect) or new_rect.centerx > self.bar.rect.right + 50:
                    continue  # Kui laud on liiga lähedal baari, proovime uut kohta

                # Kui laud ei kattu teistega ja ei ole liiga lähedal baari, paigutame laua
                if not any(new_rect.colliderect(existing) for existing in positions):
                    table = Table(x, y)
                    self.tables.add(table)
                    self.sprites.add(table)
                    self.collision_layer.add(table)
                    positions.append(new_rect)
                    break  # Kui laud ei kattu teistega ja ei ole liiga lähedal baari, paigutame laua

        # Klaaside paigutus
        glass_types = [
            {"image": pygame.image.load(os.path.join(self.base_path, "assets", "designs", "glass", "shot.png")),"points": 1},
            {"image": pygame.image.load(os.path.join(self.base_path, "assets", "designs", "glass", "klaas4.png")),"points": 2},
            {"image": pygame.image.load(os.path.join(self.base_path, "assets", "designs", "glass", "martini.png")),"points": 3}
        ]

        # Klaasi suuruse muutmine
        for glass in glass_types:
            # Muutame klaasi pildi suuruseks (nt 40x40)
            glass["image"] = pygame.transform.scale(glass["image"], (20, 20))

        for table in self.tables:
            for i in range(3):  # Veenduge, et iga laud saab kuni 3 klaasi
                x_offset = 10 + (i * 30) if i < 2 else 25
                y_offset = 10 if i < 2 else 40
                glass_x = table.rect.x + x_offset
                glass_y = table.rect.y + y_offset

                # Veenduge, et klaasid ei kattuks omavahel
                glass_rect = pygame.Rect(glass_x, glass_y, 40, 40)  # Klaasi uus suurus
                if not any(glass_rect.colliderect(existing.rect) for existing in self.glasses):
                    glass_data = random.choice(glass_types)  # Valime klaasi tüübi
                    glass = Glass(glass_x, glass_y, glass_data["image"], glass_data["points"])
                    self.glasses.add(glass)
                    self.sprites.add(glass)
                    positions.append(glass.rect)

        # Lisame vaenlased, tagame, et nad ei saa tekkida lauadele
        for _ in range(enemy_count):
            while True:
                enemy_x = random.randint(50, WIDTH - 100)
                enemy_y = random.randint(50, HEIGHT - 100)
                enemy_rect = pygame.Rect(enemy_x, enemy_y, 50, 50)  # Vaenlase suurus

                # Kontrollime, kas vaenlase koht ei kattu lauaga
                if not any(enemy_rect.colliderect(table.rect) for table in self.tables):
                    break  # Kui vaenlane ei kattu lauaga, siis paigutame ta

            # Kui koht on leitud, loome vaenlase ja lisame selle
            self.enemy = Enemy(enemy_x, enemy_y, enemy_image, self.tables)
            self.enemies.add(self.enemy)
            self.sprites.add(self.enemy)


    def handle_events(self, event):
        """Mängu sündmuste käsitlemine."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Kui vajutatakse P, siis lülitame pausi sisse või välja
                self.toggle_pause()
            elif event.key == pygame.K_q:  # Kui vajutatakse Q nuppu, siis viige tagasi MainMenu
                self.scene_switcher("MainMenu", self.screen)

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
        keys = pygame.key.get_pressed()  # Kontrollime, milliseid nuppe on vajutatud
        self.player.handle_movement(keys, self.tables, delta)  # Kutsume liikumise funktsiooni

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
            continue_button_position = (
            WIDTH // 2 - self.continue_button.rect.width // 2, HEIGHT // 2 - self.continue_button.rect.height // 2)
            self.continue_button.render(screen, continue_button_position)
        else:
            # Joonista mängu tavaline ekraan
            self.sprites.draw(screen)
            self.game_timer.draw_progress_bar(screen)
            ui.draw_score(screen, pygame.font.Font(None, 36), self.score)  # Kuvab skoori

        # Quit nupp paigutatud paremasse nurgasse
        quit_button_position = (WIDTH - 250, HEIGHT - 70)
        self.quit_button.render(screen, quit_button_position)

    def quit_game(self):
        """Mängu lõpetamine või MainMenu-le naasmine"""
        from main_menu import MainMenu  # Liiguta impordi siin, et vältida tsüklilist importimist
        self.scene_switcher("MainMenu", self.screen)

    def check_collisions(self):
        """Kontrollib mängija ja klaaside või vaenlaste vahelisi kokkupõrkeid."""

        # Klaaside kogumise kontroll (punktid ei suurene kohe)
        if self.carried_glasses < self.max_glasses:
            glasses_collected = pygame.sprite.spritecollide(self.player, self.glasses, True)
            for glass in glasses_collected:
                self.carried_glasses += 1  # Lisame klaasi, aga punktid ei suurene veel

        # Kui mängija viib klaasid baari juurde ja vajutab hiireklahvi, saab ta punkte klaasi väärtuse järgi
        if self.carried_glasses > 0 and self.player.rect.colliderect(self.bar.rect):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bar.rect.collidepoint(event.pos):  # Kui klikk on baari peal
                        points_earned = 0  # Algväärtustame teenitud punktide kogusumma

                        # Läbime kõik klaasid, mida mängija on korjanud
                        glasses_to_remove = []  # Loend klaasid, mis eemaldatakse
                        for glass in self.glasses:
                            if glass.rect.colliderect(self.player.rect):  # Kui klaas on mängijal kaasas
                                points_earned += glass.points  # Lisame klaasi määratud punktid
                                glasses_to_remove.append(glass)  # Lisame klaasi eemaldamiseks

                                # Paigutame klaasi baari peale
                                glass.rect.center = self.bar.rect.center  # Paigutame klaasi baari keskele
                                self.sprites.add(glass)  # Lisame klaasi baari peale

                        # Kui teenitud punkte on
                        if points_earned > 0:
                            self.score += points_earned  # Lisame teenitud punktid mängija skoorile
                            self.carried_glasses = 0  # Tühjendame kaasaskantavad klaasid
                            print(f"Punktid teenitud: {points_earned}")  # Kontrollimiseks

                            # Eemaldame klaasid mängija käest, sest need on baari viidud
                            for glass in glasses_to_remove:
                                self.glasses.remove(glass)
                                self.sprites.remove(glass)
                                self.collision_layer.remove(glass)

        # Vaenlase kokkupõrke kontroll
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            # Kui mängija põrkab kokku vaenlasega, kaotab ta kõik klaasid, aga mitte punktid
            self.carried_glasses = 0  # Kaotab kõik klaasid, kuid punktid jäävad alles

    def check_win_condition(self):
        """Kontrollib, kas mängija on võitnud taseme."""
        pass