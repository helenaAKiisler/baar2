import pygame
import os
import random
from src.game import ui
from player import Player
from object import Glass, Table, Enemy, Bar
from progress_bar import GameTimer
from scene import Scene
from src.game.main import enemy_image
from main import table_image, bar_image
from settings import WIDTH, HEIGHT


class GameLevel(Scene):

    def __init__(self, scene_switcher, screen, base_path, level=1):
        super().__init__(scene_switcher)
        self.screen = screen
        self.base_path = base_path
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

        # Laadige taustapilt
        self.background_image_path = os.path.join(self.base_path, "assets", "designs", "background", "floor.png")
        self.background_image = pygame.image.load(self.background_image_path)
        self.background_image = pygame.transform.scale(self.background_image,(WIDTH // 4, HEIGHT // 4))  # Muudame suuruse ekraanile sobivaks

        # Laadige laua pilt (laud2.png)
        #table_image_path = os.path.join(self.base_path, "assets", "designs", "table", "laud2.png")
        #table_image = pygame.image.load(table_image_path)
        #self.table_image = pygame.transform.scale(self.table_image, (130, 130))  # Scaling the table image

        # Baar
        bar_image_path = os.path.join(base_path, "..", "assets", "designs", "table", "table.png")
        self.bar_image = pygame.image.load(bar_image_path)
        self.rect = self.bar_image.get_rect()

        # Baar objekti loomine
        self.bar = Bar(200)
        self.sprites.add(self.bar)  # Lisa baar sprite gruppi

        # Mängija pildi määramine
        character_image_path = os.path.join(self.base_path, "assets", "designs", "character", "mees", "teenindus.mees2.png")
        player_image = pygame.image.load(character_image_path)
        self.rect = self.bar_image.get_rect()

        # Paigutame baari ekraani ülaosas keskele
        self.rect.x = (WIDTH - self.rect.width) // 2  # Baar on keskendatud horisontaalselt
        self.rect.y = 50  # Baar asub ekraani ülaservas

        # Mängija loomine
        self.player = Player(WIDTH // 2, HEIGHT - 80, player_image, self.bar)
        self.sprites.add(self.player)

        # Laadige vaenlase pilt enne objekti loomist
        enemy_image_path = os.path.join(self.base_path, "assets", "designs", "customer", "klient1.png")
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
            (100, 100), (250, 200), (400, 300), (500, 100), (500, 200),
            (100, 450), (200, 550), (350, 450), (500, 600), (600, 500)
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
            {"image": pygame.image.load(os.path.join(self.base_path, "assets", "designs", "glass", "klaas4.png")),"points": 2},
            {"image": pygame.image.load(os.path.join(self.base_path, "assets", "designs", "glass", "martini.png")),"points": 3}
        ]

        # Klaasi suuruse määramine (nt 50x50 px)
        glass_width = 20
        glass_height = 20

        # Paigutame klaasid laua keskpunkti ümber
        for table in self.tables:
            table_rect = table.rect
            table_width = table_rect.width
            table_height = table_rect.height

            # Määrame laua keskpunkti
            table_centerx = table_rect.centerx
            table_centery = table_rect.centery

            # Paigutame klaasid täpselt laua keskpunkti ümber, et need ei ulatuks laua piiridest välja
            for i in range(3):
                # Iga klaasi paigutamine erinevatesse kohtadesse laua ümber
                if i == 0:
                    # Esimene klaas paigutatakse laua vasakule küljele
                    x_offset = table_centerx - glass_width - 5  # Väike kaugus vasakule
                    y_offset = table_centery - (glass_height // 2)  # Keskendub vertikaalselt
                elif i == 1:
                    # Teine klaas paigutatakse laua keskmesse
                    x_offset = table_centerx - (glass_width // 2)  # Keskendab klaasi laua keskosas
                    y_offset = table_centery - (glass_height // 2)  # Keskendab klaasi laua keskosas
                else:
                    # Kolmas klaas paigutatakse laua paremale küljele
                    x_offset = table_centerx + 5  # Väike kaugus paremale
                    y_offset = table_centery - (glass_height // 2)  # Keskendub vertikaalselt

                # Kontrollime, et klaasi positsioon ei kattu teiste klaasidega
                glass_rect = pygame.Rect(x_offset, y_offset, glass_width, glass_height)
                if not any(glass_rect.colliderect(existing.rect) for existing in self.glasses):
                    glass_data = random.choice(glass_types)  # Valime klaasi tüübi
                    glass = Glass(x_offset, y_offset, glass_data["image"], glass_data["points"])
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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Lülitame pausi sisse või välja
                self.toggle_pause()
            elif event.key == pygame.K_x:  # Klaasi korjamine
                self.pick_up_glass()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Vasak hiireklahv
                self.pick_up_glass()

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

        # Kui mängija viib klaasi baari, siis annab see punkte
        if self.carried_glasses > 0 and self.player.rect.colliderect(self.bar.rect):
            for glass in self.glasses:
                if self.player.rect.colliderect(glass.rect):  # Kui klaas on baari peal
                    self.score += glass.points  # Lisame klaasi väärtuse
                    print(f"Viidud klaas baari! Punktid: {self.score}")
                    self.carried_glasses -= 1  # Vähendame klaasi arvu pärast baari viimist
                    break  # Kui klaas viidi baari, siis lõpetame kontrollimise

    def continue_game(self):
        """Jätkab mängu pärast pausi."""
        self.paused = False
        self.continue_button.is_visible = False  # Peidab 'Continue' nupu
        self.game_timer.resume()  # Taaskäivitab mängu ajamõõdiku

    def render(self, screen):
        # Kuvame taustapildi mitmekordistamise, et katta kogu ekraan
        for x in range(0, WIDTH, self.background_image.get_width()):
            for y in range(0, HEIGHT, self.background_image.get_height()):
                screen.blit(self.background_image, (x, y))  # Taust kuvatakse mitmekordselt üle ekraani

        self.sprites.draw(screen)
        ui.draw_score(screen, pygame.font.Font(None, 36), self.score)

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

    def pick_up_glass(self):
        """Kontrollib, kas mängija on laua lähedal ja korjab klaasi."""
        if self.carried_glasses < 3:  # Kontrollime, kas mängijal on vähem kui 3 klaasi
            for table in self.tables:
                if self.player.rect.colliderect(table.rect.inflate(50, 50)):  # Kui mängija on laua lähedal
                    for glass in self.glasses:
                        if table.rect.colliderect(glass.rect):  # Kui klaas on laua peal
                            self.glasses.remove(glass)
                            self.sprites.remove(glass)
                            self.carried_glasses += 1  # Lisame klaasi, mida mängija kannab
                            print(f'Klaas korjatud! Kannab {self.carried_glasses} klaasi.')
                            break  # Kui klaas on korjatud, lõppeb kontrollimine

    def check_collisions(self):
        """Kontrollib mängija ja klaaside või vaenlaste vahelisi kokkupõrkeid."""

        # Klaaside kogumine (punktid ei suurene kohe)
        if self.carried_glasses < self.max_glasses:
            glasses_collected = pygame.sprite.spritecollide(self.player, self.glasses, True)
            for glass in glasses_collected:
                self.carried_glasses += 1  # Lisame klaasi mängijale
                print(f'Klaas korjatud! Kannab {self.carried_glasses} klaasi.')

        # Kui mängija viib klaasid baari juurde ja vajutab hiireklahvi, saab ta punkte klaasi väärtuse järgi
        if self.carried_glasses > 0 and self.player.rect.colliderect(self.bar.rect):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:  # Kui hiireklahvi vajutatakse
                    if self.bar.rect.collidepoint(event.pos):  # Kui klikk on baari peal
                        print("Baari klikkimist tuvastatud!")

                        points_earned = 0  # Algväärtustame teenitud punktide kogusumma

                        # Läbime kõik klaasid, mida mängija on korjanud
                        glasses_to_remove = []  # Loend klaasid, mis eemaldatakse
                        for glass in self.glasses:
                            if glass.rect.colliderect(self.player.rect):  # Kui klaas on mängijal kaasas
                                print(f"Klaas {glass} on kaasas, teenitakse punkte!")
                                points_earned += glass.points  # Lisame klaasi määratud punktid
                                glasses_to_remove.append(glass)  # Lisame klaasi eemaldamiseks

                                # Paigutame klaasi baari peale
                                glass.rect.center = self.bar.rect.center  # Paigutame klaasi baari keskele
                                self.sprites.add(glass)  # Lisame klaasi baari peale

                        # Kui teenitud punkte on
                        if points_earned > 0:
                            print(f"Teenitud punktid: {points_earned}")
                            self.score += points_earned  # Lisame teenitud punktid mängija skoorile
                            self.carried_glasses = 0  # Tühjendame kaasaskantavad klaasid

                            # Eemaldame klaasid mängija käest, sest need on baari viidud
                            for glass in glasses_to_remove:
                                self.glasses.remove(glass)
                                self.sprites.remove(glass)
                                self.collision_layer.remove(glass)
                                print(f"Viidud klaas baari! Punktid: {self.score}")

        # Vaenlase kokkupõrke kontroll
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            # Kui mängija põrkab kokku vaenlasega, kaotab ta kõik klaasid, aga mitte punktid
            self.carried_glasses = 0  # Kaotab kõik klaasid, kuid punktid jäävad alles

    def check_win_condition(self):
        """Kontrollib, kas mängija on võitnud taseme."""
        pass