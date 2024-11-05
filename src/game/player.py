import os.path

import pygame
from pygame.locals import *
import random, time
import sys

#from src.game.main import WIDTH, HEIGHT

pygame.init()
vec = pygame.math.Vector2
WIDTH = 1600
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
FramePerSec = pygame.time.Clock()

running = True

BLACK = (0, 0, 0)

character_image_path = os.path.join("..", "..", "assets", "designs", "character", "teenindaja.mees3.png")
player_image = pygame.image.load(character_image_path)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,WIDTH-40),0)

    def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 900):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 1370), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#Spraitide loomine
P1 = Player()
E1 = Enemy()

#Spraitide gruppide loomine
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    P1.update()
    E1.move()

    screen.fill((101, 67, 33))
    P1.draw(screen)
    E1.draw(screen)

    pygame.display.update()
    FramePerSec.tick(FPS)
#        if event.type == pygame.KEYDOWN:
#            #vajutab üles noolt või "W"
#            if event.key == pygame.K_UP or event.key == pygame.K_w:
#                speed_y = -1
#            #vajutab alla noolt või "S"
#            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
#                speed_y = 1
#            #vajutab vasakule noolt või "A"
#            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
#                speed_x = -1
#            #vajutab paremale noolt või "D"
#            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
#                speed_x = 1
#        if event.type == pygame.KEYUP:
#            speed_x = 0
#            speed_y = 0
#    if speed_x != 0:
#        player_x += speed_x
#    if speed_y != 0:
#        player_y += speed_y


#    pygame.draw.circle(screen, (0, 0, 255), (player_x, player_y), 50)

#    pygame.display.flip()