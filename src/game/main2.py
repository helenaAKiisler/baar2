import pygame
import sys
import random

pygame.init()

# Mängu seaded
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BAAR")

FPS = 60
clock = pygame.time.Clock()

# Värvid
TUME_PRUUN = (101, 67, 33)
SININE = (0, 0, 255)
PUNANE = (255, 0, 0)

# Mängu seisundid
running = True
paused = False

# Mängija ja objekt
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 5

object_size = 50
object_pos = [random.randint(0, WIDTH - object_size), 0]
object_speed = 3

# Põhitsükkel
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not paused:
                    paused = True  # Pausile minek
                else:
                    paused = False  # Pausilt tagasitulek

    # Kui mäng on pausil, ei uuenda ekraani
    if not paused:
        screen.fill(TUME_PRUUN)

        # Mängija liikumine nooleklahvidega
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
            player_pos[1] += player_speed

        # Liikuva objekti liikumine alla
        object_pos[1] += object_speed
        if object_pos[1] >= HEIGHT:
            object_pos = [random.randint(0, WIDTH - object_size), 0]

        # Kontrollime kokkupõrget
        if (player_pos[0] < object_pos[0] + object_size and
            player_pos[0] + player_size > object_pos[0] and
            player_pos[1] < object_pos[1] + object_size and
            player_pos[1] + player_size > object_pos[1]):
            print("Kokkupõrge! Mäng läbi.")
            running = False  # Lõpetame mängu kokkupõrkel

        # Joonistame mängija ja objekti
        pygame.draw.rect(screen, SININE, (*player_pos, player_size, player_size))
        pygame.draw.rect(screen, PUNANE, (*object_pos, object_size, object_size))

        pygame.display.flip()
    clock.tick(FPS)