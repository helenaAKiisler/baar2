# Kirjeldab ära game leveli ja tutorial leveli loomise klassid
import pygame
import os
import random
from pygame import K_SPACE
from src.game import ui
from player import Player
from object import Glass, Table, Enemy, Bar
from progress_bar import GameTimer
from scene import Scene
from settings import table_image, enemy_image, bar_image, player_image, background_image, base_path, predefined_table_positions, predefined_enemy_positions, glass_types
from settings import WIDTH, HEIGHT, BLACK


class GameLevel(Scene):
    """Loob mängu leveli"""
    def __init__(self, scene_switcher, screen, level=1):
        super().__init__(scene_switcher)
        self.screen = screen
        self.level = level
        self.is_running = True
        self.score = 0
        self.carried_glasses = 0
        self.max_glasses = 3
        self.waiting_to_place_glasses = False
        self.collected_glasses = []
        self.win_points = 15
        self.placed_glasses = []

        # Määrame baasi tee (base_path) kõigis meetodites kasutamiseks
        self.base_path = base_path

        # Lisame kollisioonide kihid ja muud spraitide grupid
        self.collision_layer = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.glasses = pygame.sprite.Group()
        self.tables = pygame.sprite.Group()

        self.background_image = pygame.transform.scale(background_image,(WIDTH // 8, HEIGHT // 8))  # Muudame suuruse ekraanile sobivaks

        # Baar objekti loomine
        self.bar_image = bar_image
        self.bar = Bar(256,50, 288, 96, self.bar_image)
        self.sprites.add(self.bar)

        # Mängija loomine
        self.player = Player(400, 520, player_image, self.bar)
        self.sprites.add(self.player)


        # Pausi seaded
        self.is_paused = False
        self.game_timer = GameTimer()

        self.time_up = False

        #Nupud
        self.restart_button = ui.Button("Try_Again", on_pressed=self.restart_level)
        self.quit_button = ui.Button("Quit", on_pressed=self.quit_game)
        self.continue_button = ui.Button("Continue", on_pressed=self.resume_game)
        self.pause_button = ui.Button("Pause", on_pressed=self.pause_game)

        # Startides ei ole nupp nähtav
        self.continue_button.visible = False

        self.setup_level(level)

    def setup_level(self, level):
        """Seadistab taseme raskusastme ja muud elemendid."""
        table_count = min(5 + level, 10)
        enemy_count = min(1 + (level // 2), 5)
        for i in range(table_count):
            x, y = predefined_table_positions[i]
            table = Table(x, y, 64, 64, table_image)
            self.tables.add(table)
            self.sprites.add(self.tables)
            self.collision_layer.add(self.tables)

        # Paigutame klaasid laua keskpunkti ümber
        for table in self.tables:

            # Määrame laua keskpunkti
            table_centerx = table.rect.centerx
            table_centery = table.rect.centery

            # Paigutame klaasid täpselt laua keskpunkti ümber, et need ei ulatuks laua piiridest välja
            for i in range(2):
                if i == 0:
                    # Esimene klaas paigutatakse laua vasakule küljele
                    x_offset = table_centerx - 25
                    y_offset = table_centery - 20
                    glass_data = random.choice(glass_types)  # Valime klaasi tüübi
                    glass = Glass(x_offset, y_offset, 18, 24, glass_data["image"], glass_data["points"])
                    self.glasses.add(glass)
                    self.sprites.add(glass)
                else:
                    # Teine klaas paigutatakse laua paremale küljele
                    x_offset = table_centerx + 5
                    y_offset = table_centery - 20
                    glass_data = random.choice(glass_types)  # Valime klaasi tüübi
                    glass = Glass(x_offset, y_offset, 18, 24, glass_data["image"], glass_data["points"])
                    self.glasses.add(glass)
                    self.sprites.add(glass)

        # Lisame vaenlased, tagame, et nad ei tekiks laudadele
        for a in range(enemy_count):
            enemy_x, enemy_y = predefined_enemy_positions[a]
            enemy = Enemy(enemy_x, enemy_y, enemy_image, self.tables)
            self.enemies.add(enemy)
            self.sprites.add(enemy)

    def handle_events(self, event):
        """Mängu sündmuste käsitlemine."""
        if self.time_up:
            if self.score >= self.win_points:
                self.check_win_condition()
            else:
                self.restart_button.handle_events(event)
                self.quit_button.handle_events(event)
            return

        if self.is_paused:
            self.continue_button.handle_events(event)
            self.quit_button.handle_events(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.scene_switcher("MainMenu", self.screen)
            elif event.key == pygame.K_x:  # Klaasi korjamine
                self.pick_up_glass()
            elif event.key == pygame.K_p:
                self.pause_game()
            elif self.waiting_to_place_glasses and event.key == K_SPACE:
                self.place_glasses_in_bar()
                place_glass_sound = pygame.mixer.Sound("../../assets/sfx/place_glass.mp3")
                place_glass_sound.play()
                place_glass_sound.set_volume(0.5)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pause_button.rect.collidepoint(event.pos):
                self.pause_game()
            if self.waiting_to_place_glasses and event.button == 1:
                self.place_glasses_in_bar()
                place_glass_sound = pygame.mixer.Sound("../../assets/sfx/place_glass.mp3")
                place_glass_sound.play()
                place_glass_sound.set_volume(0.5)

    def pause_game(self):
        if self.is_paused == False:
            self.is_paused = True
            self.continue_button.visible = True  # Kuvab 'Continue' nupu
            self.game_timer.pause()

    def resume_game(self):
        if self.is_paused == True:
            self.is_paused = False
            self.continue_button.visible = False  # Peidab 'Continue' nupu
            self.game_timer.resume()  # Taaskäivitab mängu ajamõõdiku


    def render(self, screen):
        # Kuvame taustapildi mitmekordistamise, et katta kogu ekraan
        for x in range(0, WIDTH, self.background_image.get_width()):
            for y in range(0, HEIGHT, self.background_image.get_height()):
                screen.blit(self.background_image, (x, y))

        # Tumeda ala lisamine punktide ja progress bar'i taustaks
        dark_area_height = 50
        pygame.draw.rect(screen, (26, 35, 29), (0, 0, WIDTH, dark_area_height))

        self.sprites.draw(screen)
        ui.draw_score(screen, pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 20), self.score)
        self.game_timer.draw_progress_bar(screen)

        # Kuvame leveli numbri progressiriba kõrvale mustale alale
        font = pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 20)
        level_text = font.render(f"Level: {self.level}", True, (180, 212, 187))
        screen.blit(level_text, (410, 0))  # Positsioon: progressiriba kõrvale paremale

        # Kui mäng on pausil, kuvatakse must ekraan ja 'Continue' nupp
        if self.is_paused:
            # Must taust ja overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(170)  # Läbipaistev must kiht
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Kuvame "Continue" nupu ekraani keskele
            continue_button_position = (WIDTH // 2 - self.continue_button.rect.width // 2 , HEIGHT // 2 - self.continue_button.rect.height // 2)
            self.continue_button.render(screen, continue_button_position)
            quit_button_position = (WIDTH // 2 - self.quit_button.rect.width // 2, HEIGHT // 2 - self.quit_button.rect.height // 2 + 90)
            self.quit_button.render(screen, quit_button_position)

        elif self.time_up:
            if self.score >= self.win_points:
                self.check_win_condition()
            else:
                # "Aeg läbi" ekraan
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(170)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))

                font = pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 42)
                text = font.render("Time is up! You lost", True, (180, 212, 187))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 -40))

                # Nuppude kuvamine
                self.restart_button.render(screen, (WIDTH // 2 - self.restart_button.rect.width // 2, HEIGHT // 2- self.restart_button.rect.height // 2))
                self.quit_button.render(screen, (WIDTH // 2 - self.quit_button.rect.width // 2, HEIGHT // 2 - self.quit_button.rect.height // 2 + 90))
                pygame.mixer.music.pause()
                lose_sound = pygame.mixer.Sound("../../assets/sfx/lose.mp3")
                lose_sound.play(0)
                lose_sound.set_volume(0.5)
                pygame.mixer.music.queue("../../assets/sfx/menu.mp3")
        else:
            # Kuvame Pause nuppu ainult siis, kui aeg pole otsas
            pause_button_position = (WIDTH - 130, 5)
            self.pause_button.render(screen, pause_button_position)

    def restart_level(self):
        """Vahetab stseeni tagasi GameLevel'iks"""
        self.scene_switcher("GameLevel", self.screen)

    def quit_game(self):
        self.scene_switcher("MainMenu", self.screen)

    def pick_up_glass(self):
        """Korjab klaasi, kui mängija on lähedal ja kannab alla 3 klaasi."""
        if self.carried_glasses < 3:
            expanded_rect = self.player.rect.inflate(50, 50)  # Suurendame mängija rect-i, et hõlbustada korjamist
            for glass in self.glasses:
                if expanded_rect.colliderect(glass.rect):
                    print(f"Kokkupõrge tuvastatud klaasiga asukohas: {glass.rect}")
                    self.carried_glasses += 1
                    self.collected_glasses.append(glass)
                    self.glasses.remove(glass)  # Eemaldame klaasi klaaside grupist
                    self.sprites.remove(glass)  # Eemaldame klaasi sprite'ide grupist
                    print(f"Klaas korjatud! Kannab {self.carried_glasses} klaasi.")
                    pickup_sound = pygame.mixer.Sound("../../assets/sfx/pick_up.mp3")
                    pickup_sound.play()
                    pickup_sound.set_volume(0.5)
                    break
            else:
                print("Ühtegi klaasi ei leitud mängija lähedalt.")
        else:
            print("Mängija kannab juba maksimaalselt 3 klaasi.")

    def place_glasses_in_bar(self):
        """Paigutab mängija korjatud klaasid baari musta ala peale ja lisab punktid."""
        bar_x = self.bar.rect.left
        bar_top = self.bar.rect.top

        x_offsets = [18, 18, 18, 18]

        for i, glass in enumerate(self.collected_glasses):
            if len(self.placed_glasses) == 0:
                glass.rect.x = bar_x + x_offsets[i]
                glass.rect.y = bar_top + 40  # Paigutame klaasid musta ala peale
                self.sprites.add(glass)  # Lisame klaasi uuesti sprite'ide gruppi
                self.placed_glasses.append(glass.rect.x)
            elif len(self.placed_glasses) > 0:
                glass.rect.x = self.placed_glasses[-1] + x_offsets[i]
                glass.rect.y = bar_top + 40  # Paigutame klaasid musta ala peale
                self.sprites.add(glass)  # Lisame klaasi uuesti sprite'ide gruppi
                self.placed_glasses.append(glass.rect.x)

        # Lisame punktid
        for glass in self.collected_glasses:
            self.score += glass.points
            print(f"Punktid lisatud: {glass.points}")

        # Tühjendame mängija korjatud klaaside loendi
        self.carried_glasses = 0
        self.collected_glasses.clear()
        self.waiting_to_place_glasses = False
        print(f"Kõik klaasid viidud baari! Skoor: {self.score}")

    def check_collisions(self):
        """Kontrollib mängija ja vaenlaste vahelisi kokkupõrkeid."""

        # Vaenlase kokkupõrke kontroll
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            # Kui mängija põrkab kokku vaenlasega, kaotab ta kõik klaasid, aga mitte punktid
            collision_sound = pygame.mixer.Sound("../../assets/sfx/enemy.mp3")
            collision_sound.play()
            collision_sound.set_volume(0.5)
            self.carried_glasses = 0
            self.collected_glasses.clear()
            print("Põrkasid vaenlasega! Klaasid kadusid.")

    def update(self):
        """Uuendab leveli seisundit."""
        if self.is_paused:
            return
        if self.game_timer.is_time_up():
            self.time_up = True  # Märgime, et aeg on läbi
            return
        if not self.is_paused and not self.time_up:
            delta = self.game_timer.get_delta_time()  # Arvutame aja muutuse
            keys = pygame.key.get_pressed()
            self.player.handle_movement(keys, self.tables, delta)
            self.enemies.update()
            self.check_collisions()

        # Käsitleme mängija liikumist
        keys = pygame.key.get_pressed()  # Kontrollime, milliseid nuppe on vajutatud
        self.player.handle_movement(keys, self.tables, delta)  # Kutsume liikumise funktsiooni
        self.player.update()

        # Uuendame vaenlasi ja kontrollime kokkupõrkeid
        self.enemies.update()

        # Kontrollime kokkupõrkeid ja võidutingimusi
        self.check_collisions()
        self.check_win_condition()

        # Pausi ajal progressiriba ei täitu edasi
        self.game_timer.draw_progress_bar(self.screen)

        # Kontrollime, kas mängija on baari juures ja kannab 3 klaasi
        if self.carried_glasses > 0 and self.player.rect.colliderect(self.bar.rect):
            self.waiting_to_place_glasses = True

    def check_win_condition(self):
        if self.time_up and self.score >= self.win_points:
            next_level = self.level + 1
            if next_level <= 4:
                self.scene_switcher("GameLevel", self.screen, level=next_level)
            else:
                self.scene_switcher("WinMenu", self.screen)


class TutorialLevel(GameLevel):
    """Loob tutorial leveli."""
    def __init__(self, scene_switcher, screen, ):
        super().__init__(scene_switcher, screen)
        self.score = 0
        self.carried_glasses = 0
        self.max_glasses = 3
        self.waiting_to_place_glasses = False
        self.collected_glasses = []
        self.win_points = 15
        self.placed_glasses = []
        self.background_image = background_image
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        self.player_image = player_image
        self.table_image = table_image
        self.enemy_image = enemy_image
        self.bar_image = bar_image
        self.glass_image = pygame.image.load(os.path.join(base_path, "glass", "uusmartini.png"))

        self.collision_layer = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.glasses = pygame.sprite.Group()
        self.tables = pygame.sprite.Group()

        # Mängu objektid
        self.bar = Bar(256,50, 288, 96, self.bar_image)
        self.player = Player(WIDTH // 2, 400, self.player_image, self.bar)

        # Klaasi paigutamine täpselt laua keskele


        # Kas mängija kannab klaasi
        self.is_carrying_glass = False

        # Skip nupp
        self.skip_button = ui.Button("Skip", on_pressed=self.skip_tutorial)

        self.tutorial_texts = [
            ("Use arrow keys or WASD to move.", (20, HEIGHT - 180)),
            ("Press X to pick up glasses.", (20, HEIGHT - 150)),
            ("Press SPACE to place glasses on the bar.", (20, HEIGHT - 120)),
            ("Collect minimum 15 points.", (20, HEIGHT - 90)),
            ("Avoid enemies!", (20, HEIGHT - 60)),
        ]

        # Sprite grupp
        self.sprites.add(self.bar)
        self.sprites.add(self.player)
        self.setup_level(0)

    def setup_level(self, level=0):
        """Seadistab taseme raskusastme ja muud elemendid."""
        table_count = 2
        enemy_count = 1
        for i in range(table_count):
            x, y = predefined_table_positions[i]
            table = Table(x, y, 64, 64, table_image)
            self.tables.add(table)
            self.collision_layer.add(self.tables)
            self.sprites.add(self.tables)

        # Paigutame klaasid laua keskpunkti ümber
        for table in self.tables:

            # Määrame laua keskpunkti
            table_centerx = table.rect.centerx
            table_centery = table.rect.centery

            # Paigutame klaasid täpselt laua keskpunkti ümber, et need ei ulatuks laua piiridest välja
            for i in range(2):
                # Iga klaasi paigutamine erinevatesse kohtadesse laua ümber
                if i == 0:
                    # Esimene klaas paigutatakse laua vasakule küljele
                    x_offset = table_centerx - 25
                    y_offset = table_centery - 20
                    glass_data = random.choice(glass_types)  # Valime klaasi tüübi
                    glass = Glass(x_offset, y_offset, 18, 24, glass_data["image"], glass_data["points"])
                    self.glasses.add(glass)
                    self.sprites.add(glass)
                else:
                    # Teine klaas paigutatakse laua paremale küljele
                    x_offset = table_centerx + 5
                    y_offset = table_centery - 20
                    glass_data = random.choice(glass_types)  # Valime klaasi tüübi
                    glass = Glass(x_offset, y_offset, 18, 24, glass_data["image"], glass_data["points"])
                    self.glasses.add(glass)
                    self.sprites.add(glass)

        # Lisame vaenlase j akontrollime, et nad ei tekiks laudadele.
        for a in range(enemy_count):
            enemy_x, enemy_y = predefined_enemy_positions[a]
            enemy = Enemy(enemy_x, enemy_y, enemy_image, self.tables)
            self.enemies.add(enemy)
            self.sprites.add(enemy)

    def skip_tutorial(self):
        self.scene_switcher("GameLevel", self.screen, level=1)

    def render(self, screen):
        for x in range(0, WIDTH, self.background_image.get_width()):
            for y in range(0, HEIGHT, self.background_image.get_height()):
                screen.blit(self.background_image, (x, y))

        # Must ala progressiriba ja punktide jaoks
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))

        # Kuvame punktid ja "Tutorial Level" teksti progressiriba kõrvale
        font = pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 20)
        points_text = font.render(f"Points: {self.score}", True, (180, 212, 187))
        tutorial_text = font.render("Tutorial Level", True, (180, 212, 187))
        screen.blit(points_text, (10, 10))
        screen.blit(tutorial_text, (WIDTH // 2 + 80, 10))

        # Kuvame kõik sprite'id
        self.sprites.draw(screen)

        # Kuvame progressiriba
        self.game_timer.draw_progress_bar(screen)

        # Selgitavate tekstide kuvamine
        for text, position in self.tutorial_texts:
            text_surface = font.render(text, True, (26, 35, 29))
            screen.blit(text_surface, position)

        # Skip nupp paremas ülanurgas
        self.skip_button.render(screen, (WIDTH - 130, 5))