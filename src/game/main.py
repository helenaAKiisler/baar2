################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Baar2
#
#
# Autorid: Helena Angela Kiisler, Lauri Tõnisson
#
# mõningane eeskuju:
#
# Lisakommentaar (nt käivitusjuhend)
#
##################################################
import pygame
import sys
import os.path
import random
from settings import WIDTH, HEIGHT, FPS, DARK_BROWN, GRAY, WHITE,  PRESET_TABLE_POSITIONS
from player import Player
from progress_bar import GameTimer
from object import Glass, Table, Enemy
from ui import initialize_font, TEXT_COLOR  # Importime initialize_font ja TEXT_COLOR
from pohiloogika import Game
from main_menu import MainMenu
from game_level import GameLevel
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

# Mängija pildi tee ja pildi laadimine
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
character_image_path = os.path.join(base_path, "assets", "designs", "character", "mees", "teenindus.mees2.png")
player_image = pygame.image.load(character_image_path)

enemy_image_path = os.path.join(base_path, "assets", "designs", "character", "naine", "idle.png")
enemy_image = pygame.image.load(enemy_image_path)

# Objektide loomine
player = Player(WIDTH // 2, HEIGHT - 80, player_image)
enemy = Enemy(200, 80, enemy_image)
# Spraitide gruppide loomine


game_timer = GameTimer()

def scene_switcher(new_scene_name, screen=None):
    global current_scene
    if new_scene_name == "MainMenu":
        current_scene = MainMenu(scene_switcher, game_title="Baar 2", screen=screen)
    elif new_scene_name == "GameLevel":
        current_scene = GameLevel(scene_switcher, screen=screen)  # Edastame screen objekti

def main():
    global current_scene, score, game_timer
    screen = pygame.display.set_mode((800, 600))  # Loome screen objekti siin

    # Initsialiseerime FONT enne MainMenu loomist
    initialize_font()

    # Algne stseen
    current_scene = MainMenu(scene_switcher, game_title="Baar 2", screen=screen)  # Edastame game_title ja screen

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
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c and game.is_paused:
                    game.toggle_pause()
                    game_timer.toggle_pause()

            current_scene.handle_events(event)  # Kontrollime sündmusi (ka nupu vajutamist)

        current_scene.update()  # Uuendab mänguloogikat, sealhulgas mängija liikumist
        current_scene.render(screen)  # Edastame screen objekti
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()