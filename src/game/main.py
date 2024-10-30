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

from pygame.examples.moveit import WIDTH, HEIGHT
from pygame.examples.sprite_texture import clock, running, event

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(WIDTH, HEIGHT)
pygame.display.set_caption("BAAR ")

FPS = 60
clock = pygame.time.Clock()

TUME_PRUUN = (101, 67, 33)

#põhitsükkel
running = True
while running:
    for sündmus in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(TUME_PRUUN)

    #Siia saab lisada mängu loogika :)





    pygame.display.flip()
    clock.tick(FPS)

