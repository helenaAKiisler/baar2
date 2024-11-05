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
from pohiloogika import Game
from settings import *
from player import Player
from object import Table
from object import Glass
from ui import draw_score, draw_time
from game_timer import GameTimer

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Baar2")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Mängu alustamine
score = 0
running = True

# Loome mängija, lauad ja klaasid
player = Player(WIDTH // 2, HEIGHT - PLAYER_SIZE - 40)
tables = [Table(x, y) for x, y in PRESET_TABLE_POSITIONS]
glasses = []
glass_types = [
    {"color": (255, 255, 0), "points": 1},
    {"color": (255, 20, 147), "points": 2},
    {"color": (255, 69, 0), "points": 3}
]

for table in tables:
    glass_type = random.choice(glass_types)
    glasses.append(Glass(table.rect.x + 15, table.rect.y + 15, glass_type["color"], glass_type["points"]))

# Initsialiseerime taimeri
game_timer = GameTimer()

# Põhitsükkel
while running:
    if game_timer.is_time_up():
        print("Mängu aeg on läbi! Skoor:", score)
        running = False
        continue

    # Sündmused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Pausile minek või pausilt naasmine
                game_timer.toggle_pause()
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
    screen.fill(TUME_PRUUN)
    player.draw(screen)
    for table in tables:
        table.draw(screen)
    for glass in glasses:
        glass.draw(screen)
    draw_score(screen, font, score)
    game_timer.draw_progress_bar(screen)

    # Kuvame kas järelejäänud aja või pausiteate
    if game_timer.paused:
        pause_text = font.render("Pausil", True, VALGE)
        screen.blit(pause_text, (WIDTH // 2 - 40, HEIGHT // 2))
    else:
        draw_time(screen, font, game_timer.get_time_left())

    pygame.display.flip()
    clock.tick(FPS)
