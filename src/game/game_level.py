import pygame
import os
import random
from src.game import ui
from player import Player
from object import Glass, Table, Enemy, Bar
from progress_bar import GameTimer
from scene import Scene
from main import table_image, bar_image, enemy_image
from settings import WIDTH, HEIGHT


class GameLevel(Scene):

    def __init__(self, scene_switcher, screen, base_path, level=1):
        super().__init__(scene_switcher)
        self.screen = screen
        self.base_path = base_path
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
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Lisame kollisioonide kihid ja muud spraitide grupid
        self.collision_layer = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.glasses = pygame.sprite.Group()
        self.tables = pygame.sprite.Group()

        # Laadige taustapilt
        self.background_image_path = os.path.join(self.base_path, "assets", "designs", "background", "floor.png")
        self.background_image = pygame.image.load(self.background_image_path)
        self.background_image = pygame.transform.scale(self.background_image,(WIDTH // 4, HEIGHT // 4))  # Muudame suuruse ekraanile sobivaks

        # Baar
        bar_image_path = os.path.join(base_path, "..", "assets", "designs", "background", "baar2.png")
        self.bar_image = pygame.image.load(bar_image_path)
        self.rect = self.bar_image.get_rect()

        # Baar objekti loomine
        self.bar = Bar(self.bar_image, 288, 96)
        self.sprites.add(self.bar)  # Lisa baar sprite gruppi

        # Mängija pildi määramine
        character_image_path = os.path.join(self.base_path, "assets", "designs", "character", "mees", "idle.png")
        player_image = pygame.image.load(character_image_path)

        # Paigutame baari ekraani ülaosas keskele
        self.rect.x = (WIDTH - self.rect.width) // 2  # Baar on keskendatud horisontaalselt
        self.rect.y = 50  # Baar asub ekraani ülaservas

        # Mängija loomine
        self.player = Player(WIDTH // 2, HEIGHT - 80, player_image, self.bar)
        self.sprites.add(self.player)


        # Pausi seaded
        self.is_paused = False
        self.game_timer = GameTimer()

        self.time_up = False  # Lisame oleku, et jälgida, kas aeg on otsas
        self.restart_button = ui.Button("Try Again", on_pressed=self.restart_level)
        self.quit_button_time_up = ui.Button("Quit", on_pressed=self.quit_game)
        self.quit_button = ui.Button("Quit", on_pressed=self.quit_game)
        self.continue_button = ui.Button("Continue", on_pressed=self.resume_game)
        self.pause_button = ui.Button("Pause", on_pressed=self.pause_game)

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
            (466, 536), (272, 226), (272, 381), (466, 381), (272, 536),
            (466, 226), (80, 472), (80, 322), (80, 170), (664, 320)
        ]

        predefined_enemy_positions = [
            (144, 162), (144, 304), (596, 440), (726, 246)
        ]

        # Paigutame lauad kindlatesse kohtadesse, kontrollides, et nad ei oleks liiga lähedal baari
        positions = []
        for i in range(table_count):
            while True:
                x, y = predefined_table_positions[i]
                new_rect = pygame.Rect(x, y, 64, 64)  # 80x80 on laua suurus

                # Kontrollime, et laud ei ole liiga lähedal baari
                if new_rect.colliderect(self.bar.rect) or new_rect.centerx > self.bar.rect.right + 50:
                    continue  # Kui laud on liiga lähedal baari, proovime uut kohta

                # Kui laud ei kattu teistega ja ei ole liiga lähedal baari, paigutame laua
                if not any(new_rect.colliderect(existing) for existing in positions):
                    table = Table(x, y, table_image)
                    self.tables.add(table)
                    self.sprites.add(table)
                    self.collision_layer.add(table)
                    positions.append(new_rect)
                    break  # Kui laud ei kattu teistega ja ei ole liiga lähedal baari, paigutame laua

        # Klaaside paigutus
        glass_types = [
            {"image": pygame.image.load(os.path.join(self.base_path, "assets", "designs", "glass", "shot.png")),"points": 1},
            {"image": pygame.image.load(os.path.join(self.base_path, "assets", "designs", "glass", "klaas3.png")),"points": 2},
            {"image": pygame.image.load(os.path.join(self.base_path, "assets", "designs", "glass", "martini.png")),"points": 3}
        ]


        # Paigutame klaasid laua keskpunkti ümber
        for table in self.tables:

            # Määrame laua keskpunkti
            table_centerx = table.rect.centerx
            table_centery = table.rect.centery

            # Paigutame klaasid täpselt laua keskpunkti ümber, et need ei ulatuks laua piiridest välja
            for i in range(3):
                # Iga klaasi paigutamine erinevatesse kohtadesse laua ümber
                if i == 0:
                    # Esimene klaas paigutatakse laua vasakule küljele
                    x_offset = table_centerx - 25
                    y_offset = table_centery - 15
                else:
                    # Teine klaas paigutatakse laua paremale küljele
                    x_offset = table_centerx + 5
                    y_offset = table_centery - 15

                # Kontrollime, et klaasi positsioon ei kattu teiste klaasidega
                glass_rect = pygame.Rect(x_offset, y_offset, 18, 24)
                if not any(glass_rect.colliderect(existing.rect) for existing in self.glasses):
                    glass_data = random.choice(glass_types)  # Valime klaasi tüübi
                    glass = Glass(x_offset, y_offset, glass_data["image"], glass_data["points"])
                    self.glasses.add(glass)
                    self.sprites.add(glass)
                    positions.append(glass.rect)

        # Lisame vaenlased, tagame, et nad ei saa tekkida lauadele
        for a in range(enemy_count):
            while True:
                enemy_x, enemy_y = predefined_enemy_positions[a]
                enemy_rect = pygame.Rect(enemy_x, enemy_y, 60, 60)  # Vaenlase suurus

                # Kontrollime, kas vaenlase koht ei kattu lauaga
                if not any(enemy_rect.colliderect(table.rect) for table in self.tables):
                    break  # Kui vaenlane ei kattu lauaga, siis paigutame ta

            # Kui koht on leitud, loome vaenlase ja lisame selle
            enemy = Enemy(enemy_x, enemy_y, enemy_image, self.tables)
            self.enemies.add(enemy)
            self.sprites.add(enemy)

        for glass in self.glasses:
            print(f"Klaas loodud asukohas: {glass.rect}")


    def handle_events(self, event):
        """Mängu sündmuste käsitlemine."""
        if self.time_up:
            if self.score >= self.win_points:
                self.check_win_condition()
            else:
                self.restart_button.handle_events(event)
                self.quit_button_time_up.handle_events(event)
            return

        if self.is_paused:  # Only handle pause-related events
            self.continue_button.handle_events(event)
            self.quit_button.handle_events(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Kui vajutatakse Q nuppu, siis viige tagasi MainMenu
                self.scene_switcher("MainMenu", self.screen)
            elif event.key == pygame.K_x:  # Klaasi korjamine
                print(f"Mängija asukoht ja suurus: {self.player.rect}")
                self.pick_up_glass()
            elif event.key == pygame.K_p:
                self.pause_game()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pause_button.rect.collidepoint(event.pos):  # Pause button clicked
                self.pause_game()
            if self.waiting_to_place_glasses and event.button == 1:
                self.place_glasses_in_bar()

    def pause_game(self):
        """Pausib mängu ja kuvab 'Continue' nupu."""
        if self.is_paused == False:
            self.is_paused = True
            self.continue_button.visible = True  # Kuvab 'Continue' nupu
            self.game_timer.pause()

        # Loome läbipaistva musta kihi ekraanile, et teha ekraan udune
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)  # Set transparency of the overlay (150 makes it semi-transparent)
        overlay.fill((0, 0, 0))  # Fill with black color for the blur effect
        self.screen.blit(overlay, (0, 0))  # Render the overlay to the screen

    def resume_game(self):
        """Taaskäivitab mängu pärast pausi."""
        if self.is_paused == True:
            self.is_paused = False
            self.continue_button.visible = False  # Peidab 'Continue' nupu
            self.game_timer.resume()  # Taaskäivitab mängu ajamõõdiku


    def render(self, screen):
        # Kuvame taustapildi mitmekordistamise, et katta kogu ekraan
        for x in range(0, WIDTH, self.background_image.get_width()):
            for y in range(0, HEIGHT, self.background_image.get_height()):
                screen.blit(self.background_image, (x, y))  # Taust kuvatakse mitmekordselt üle ekraani

        # Tumeda ala lisamine punktide ja progress bar'i taustaks
        dark_area_height = 50
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, dark_area_height))

        self.sprites.draw(screen)
        ui.draw_score(screen, pygame.font.Font(None, 36), self.score)
        self.game_timer.draw_progress_bar(screen)

        # Kui mäng on pausil, kuvatakse must ekraan ja 'Continue' nupp
        if self.is_paused:
            # Must taust ja overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)  # Läbipaistev must kiht
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Kuvame "Continue" nupu ekraani keskele
            continue_button_position = (
            WIDTH // 2 - self.continue_button.rect.width // 2 + 130, HEIGHT // 2 - self.continue_button.rect.height // 2)
            self.continue_button.render(screen, continue_button_position)
            quit_button_position = (WIDTH // 2 - self.quit_button.rect.width // 2 + 170, HEIGHT // 2 + 90)
            self.quit_button.render(screen, quit_button_position)

        elif self.time_up:
            if self.score >= self.win_points:
                self.check_win_condition()
            else:
                # "Aeg läbi" ekraan
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(150)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))

                font = pygame.font.Font(None, 72)
                text = font.render("Time is up! You lost", True, (255, 0, 0))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

                # Nuppude kuvamine
                self.restart_button.render(screen, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
                self.quit_button_time_up.render(screen, (WIDTH // 2 - 100, HEIGHT // 2 + 70))
        else:
            # Kuvame Quit nuppu ainult siis, kui aeg pole otsas
            pause_button_position = (WIDTH - 250, HEIGHT - 70)
            self.pause_button.render(screen, pause_button_position)

    def restart_level(self):
        """Käivitab leveli uuesti algusest."""
        self.scene_switcher("GameLevel", self.screen)  # Vahetab stseeni tagasi GameLevel'iks

    def quit_game(self):
        """Mängu lõpetamine või MainMenu-le naasmine"""
        from main_menu import MainMenu  # Liiguta impordi siin, et vältida tsüklilist importimist
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
                    break
            else:
                print("Ühtegi klaasi ei leitud mängija lähedalt.")
        else:
            print("Mängija kannab juba maksimaalselt 3 klaasi.")

    def place_glasses_in_bar(self):
        """Paigutab mängija korjatud klaasid baari musta ala peale ja lisab punktid."""
        # Määrame klaaside asukoha baari musta ala peale
        bar_x = self.bar.rect.left
        bar_top = self.bar.rect.top

        # Suurem hulk nihkeid, et klaasid ei kattuks
        x_offsets = [15, 15, 15, 15, 25, 35, 45, 55, 65]

        for i, glass in enumerate(self.collected_glasses):
            if i < len(x_offsets):
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
            else:
                print("Liiga palju klaase korraga, paigutus ebaõnnestus.")

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
        if self.time_up:
            self.scene_switcher("WinMenu", self.screen)
