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

# from pygame.examples.moveit import WIDTH, HEIGHT
# from pygame.examples.sprite_texture import clock, running, event

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BAAR")

FPS = 60
clock = pygame.time.Clock()

TUME_PRUUN = (101, 67, 33)

#põhitsükkel
running = False
paused = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not running: #Alusta mängu
                    running = True
                    paused = False
            elif event.key == pygame.K_p:
                if running:
                    paused = not paused  # Pausile või pausilt tagasi
            elif event.key == pygame.K_ESCAPE or pygame.K_q:  # ESC ja q klahviga sulgemine
                pygame.quit()
                sys.exit()
    #kui mäng ei ole käimas
    if not running:
        continue
    # kui mäng on pausil, ei uuenda ekraani
    if not paused:
        screen.fill(TUME_PRUUN)

    #Siia saab lisada mängu loogika :)

        pygame.display.flip()
    clock.tick(FPS)

