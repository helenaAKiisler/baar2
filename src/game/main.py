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
from object import Glass, Table
from ui import draw_score, draw_time
from pohiloogika import Game
from main_menu import MainMenu
from scene import Scene

# Algseaded
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Baar2")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 30)
score = 0

game = Game()
game.screen = screen
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

def screen_switcher(new_scene: Scene):
    global current_scene
    current_scene = new_scene

# Põhitsükkel
running = True
score = 0
game_timer = GameTimer()
while running:
    if game_timer.is_time_up():
        print("Mängu aeg on läbi! Skoor:", score)
        running = False
        continue

    # Sündmused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Pausile minek või pausilt naasmine
                game_timer.toggle_pause()
                game.toggle_pause()
            elif event.key == pygame.K_q:
                game.quit_game()
            elif event.key == pygame.K_c and game.is_paused:
                game_timer.toggle_pause()
                game.toggle_pause()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for glass in glasses[:]:
                picked_up, score = glass.check_pickup(player, score)
                if picked_up:
                    glasses.remove(glass)

    # Mängu loogika ja liikumine, kui ei ole pausil
    keys = pygame.key.get_pressed()
    if not game_timer.paused:
        player.handle_movement(keys, tables)

    # Ekraani uuendamine ja progressiriba joonistamine
    screen.fill(DARK_BROWN)
    player.draw(screen)
    for table in tables:
        table.draw(screen)
    for glass in glasses:
        glass.draw(screen)
    draw_score(screen, font, score)
    game_timer.draw_progress_bar(screen)

    # Kuvame kas järelejäänud aja või pausiteate
    if game_timer.paused:
        pause_text = font.render("Pausil", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - 40, HEIGHT // 2))
    else:
        draw_time(screen, font, game_timer.get_time_left())

    pygame.display.flip()
    clock.tick(FPS)