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
import os
from settings import WIDTH, HEIGHT
from player import Player
from progress_bar import GameTimer
from object import Glass, Table, Enemy, Bar
from ui import initialize_font  # Importime initialize_font
from pohiloogika import Game
from scene import Scene
from main_menu import MainMenu

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

# Game initialization
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Loome screen objekti
initialize_font()  # Initsialiseerime FONT

# Mängija ja vastase, tausta failitee ja pildi laadimine
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Töötab igasuguste süsteemide puhul

# Taustapildi laadimine
background_image_path = os.path.join(base_path, "..", "assets", "designs", "background", "floor.png")
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (WIDTH // 4, HEIGHT // 4))  # Muudame suuruse ekraanile sobivaks

# Laadige laua pilt (laud2.png)
table_image_path = os.path.join(base_path, "..", "assets", "designs", "table", "laud2.png")
table_image = pygame.image.load(table_image_path)
table_image = pygame.transform.scale(table_image, (130, 130))  # Scaling the table image

# Baar
bar = Bar(200)  # Baar väiksem kui ekraani laius

# Mängija pildi määramine
character_image_path = os.path.join(base_path, "..", "assets", "designs", "character", "mees", "teenindus.mees2.png")
player_image = pygame.image.load(character_image_path)

# Laadige vaenlase pilt enne objekti loomist
enemy_image_path = os.path.join(base_path, "..", "assets", "designs", "character", "naine", "idle.png")
enemy_image = pygame.image.load(enemy_image_path)

# Objektide loomine
player = Player(WIDTH // 2, HEIGHT - 80, player_image, bar)

# Kood, mis loob lauaobjektid ja edastab need vaenlasele
tables = pygame.sprite.Group()
table1 = Table(100, 100, table_image)  # Edastame table_image
tables.add(table1)

# Loome vaenlase
enemy = Enemy(200, 80, enemy_image, tables)

# Mängu aja loogika
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
    global current_scene, score, game_timer

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