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
from enemy import Enemy
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
character_image_path = os.path.join(base_path, "assets", "designs", "character", "teenindus.mees2.png")
player_image = pygame.image.load(character_image_path)

# Objektide loomine
player = Player(WIDTH // 2, HEIGHT - 80, player_image)
enemy = Enemy()

# Spraitide gruppide loomine
enemies = pygame.sprite.Group(enemy)
all_sprites = pygame.sprite.Group(player, enemy)

tables = [Table(x, y) for x, y in PRESET_TABLE_POSITIONS]  # Lauad kindlates positsioonides
glass_types = [{"color": "black", "points": 1}, {"color": "red", "points": 2}, {"color": "green", "points": 3}]
glasses = [Glass(table.rect.x + 15, table.rect.y + 15, random.choice(glass_types)["color"], random.choice(glass_types)["points"]) for table in tables]


# Stseeni vahetaja funktsioon
def scene_switcher(new_scene_name):
    global current_scene
    if new_scene_name == "MainMenu":
        current_scene = MainMenu(scene_switcher, game_title="Baar2")
    elif new_scene_name == "GameLevel":
        current_scene = GameLevel(scene_switcher)

def main():
    global current_scene
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Baar2")

    # Initsialiseerime FONT enne MainMenu loomist
    initialize_font()

    # Algne stseen
    current_scene = MainMenu(scene_switcher, game_title="Baar2")

    # Mängutsükkel
    while current_scene.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            current_scene.handle_events(event)

        current_scene.update()  # Uuendab mänguloogikat, sealhulgas mängija liikumist
        current_scene.render(screen)  # Renderdab stseeni
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()