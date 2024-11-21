################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Baar2 mäng
#
#
# Autorid: Helena Angela Kiisler, Lauri Tõnisson
#
# mõningane eeskuju: Internetist leitavad juba koostatud pygame mängud.
#
# Lisakommentaar (nt käivitusjuhend)
# Mängu käivitamiseks tuleb käivitada main.py. Mängija liikumiseks kasuta klaviatuuril nooleklahve või WASD klahvikombinatsioone.
# Nuppudele vajutamine toimub vasaku hiireklahviga. Vajutades klahvi P läheb mäng pausile.
##################################################
import pygame
import sys
import os.path
from settings import WIDTH, HEIGHT
from player import Player
from progress_bar import GameTimer
from object import Glass, Table, Enemy, Bar
from ui import initialize_font # Importime initialize_font
from pohiloogika import Game
from scene import Scene

# Algseaded
pygame.init()
pygame.display.set_caption("Baar2")
clock = pygame.time.Clock()
GAME_TITLE = "Baar2"
font = pygame.font.SysFont("Arial", 30)
score = 0
game = Game()
game.start_game()
current_scene: Scene
bar = Bar

# Mängija ja vastase failitee ja pildi laadimine
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
character_image_path = os.path.join(base_path, "assets", "designs", "character", "mees", "teenindus.mees2.png")
player_image = pygame.image.load(character_image_path)

enemy_image_path = os.path.join(base_path, "assets", "designs", "character", "naine", "idle.png")
enemy_image = pygame.image.load(enemy_image_path)

# Objektide loomine
player = Player(WIDTH // 2, HEIGHT - 80, player_image, bar)

# Kood, mis loob lauaobjektid ja edastab need vaenlasele
tables = pygame.sprite.Group()
table1 = Table(100, 100)
table2 = Table(200, 200)
tables.add(table1, table2)

enemy = Enemy(200, 80, enemy_image, tables)

game_timer = GameTimer()

# Ekraani stseenivahetus funktsioon
def scene_switcher(new_scene_name, screen=None):
    from game_level import GameLevel
    global current_scene
    if new_scene_name == "MainMenu":
        from main_menu import MainMenu
        current_scene = MainMenu(scene_switcher, game_title="Baar 2", screen=screen)
    elif new_scene_name == "GameLevel":
        current_scene = GameLevel(scene_switcher, screen=screen)  # Edastame screen objekti

# Põhifunktsioon
def main():
    from main_menu import MainMenu
    global current_scene, score, game_timer
    screen = pygame.display.set_mode((800, 600))  # Loome screen objekti

    # Initsialiseerime FONT enne MainMenu loomist
    initialize_font()

    # Algne stseen
    current_scene = MainMenu(scene_switcher, game_title="Baar 2", screen=screen)

    # Mängutsükkel
    while current_scene.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pausile minek või pausilt naasmine
                    game.toggle_pause()
                    game_timer.toggle_pause()
                elif event.key == pygame.K_q: #Mängu sulgemine
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c and game.is_paused: #Mängu pausile panek
                    game.toggle_pause()
                    game_timer.toggle_pause()

            current_scene.handle_events(event)  # Kontrollime sündmusi (ka nupu vajutamist)

        current_scene.update()  # Uuendab mänguloogikat, sealhulgas mängija liikumist
        current_scene.render(screen)  # Edastame screen objekti
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
