import pygame
import random
import os
from os import listdir
from os.path import isfile, join
from settings import WIDTH, HEIGHT, BLACK, GRAY
#from src.game.main import player

PLAYER_VEL = 5

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("../../assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=100, y=100):  # Vaikimisi määrame x ja y väärtused
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        """Liigutab vaenlast allapoole. Kui jõuab ekraani alla, asetatakse tagasi üles."""
        self.rect.y += 10
        if self.rect.top > HEIGHT:
            self.reset_position()

    def reset_position(self):
        """Paigutab vaenlase uuesti üles ekraani algusesse juhusliku horisontaalse positsiooniga."""
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def draw(self, surface):
        """Joonistab vaenlase ekraanile."""
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    BASE_SPEED = 100  # Põhikiirus pikslites sekundis
    SPRITES = load_sprite_sheets("../../assets/designs/character", "mees", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.collect = False

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
 # lisan siia playeri alla klaasi korjamise funktsiooni. Selle peab veel lahti kirjutama
    def collect_glass(self):
        self.collect = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def move_down(self, vel):
        self.y_vel = -vel

    def move_up(self, vel):
        self.y_vel = vel

    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)

        self.update_sprite()

#nagu allolev handle movement tuleb siiagi lisada see kokkupõrke tuvastus
    def handle_move(self, objects):
        keys = pygame.key.get_pressed()

        self.x_vel = 0
        if keys[pygame.K_LEFT]:
            self.move_left(PLAYER_VEL)
        if keys[pygame.K_RIGHT]:
            self.move_right(PLAYER_VEL)
        if keys[pygame.K_UP]:
            self.move_up(PLAYER_VEL)
        if keys[pygame.K_DOWN]:
            self.move_down(PLAYER_VEL)

      #Praegu saab siit kasutada ainult walk sheeti, aga tulevikus võiks ülejäänud ka olla
    def update_sprite(self):
        sprite_sheet = "idle"
        #if self.collect:
        #    sprite_sheet = "collect"
        if self.x_vel != 0:
            sprite_sheet = "walk"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
    #Siin jäin pooleli. vaja veel lisada collision ja collection jne jne. ja ss animation

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def handle_movement(self, keys, tables, delta):
        """Käsitleb mängija liikumist ja kontrollib kokkupõrkeid laudadesse."""
        move_x = 0
        move_y = 0

        # Arvutame liikumise vastavalt klahvivajutustele ja ajaintervallile
        if keys[pygame.K_UP] and self.rect.top > 0:
            move_y = -self.BASE_SPEED * delta
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            move_y = self.BASE_SPEED * delta
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            move_x = -self.BASE_SPEED * delta
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            move_x = self.BASE_SPEED * delta

        # Liigume vastavalt arvutatud väärtustele
        self.rect.x += move_x
        self.rect.y += move_y

        # Kontrollib kokkupõrkeid iga lauaga ja tühistab liikumise, kui on kokkupõrge
        for table in tables:
            if self.rect.colliderect(table.rect):
                self.rect.x -= move_x
                self.rect.y -= move_y

    def draw(self, surface):
        """Joonistab mängija ekraanile."""
        surface.blit(self.sprite, (self.rect.x, self.rect.y))

#    pygame.draw.circle(screen, (0, 0, 255), (player_x, player_y), 50)

#    pygame.display.flip()
class Glass(pygame.sprite.Sprite):
    def __init__(self, x, y, color, points):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((20, 20))  # Määrame klaasi suuruse
        self.image.fill(color)  # Määrame klaasi värvi vastavalt etteantud värvile
        self.rect = self.image.get_rect(topleft=(x, y))  # Seadistame asukoha
        self.points = points  # Määrame klaasi punktiväärtuse

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_pickup(self, player, score):
        # laiendan klaasi üleskorjamis/kokkupõrke ala
        pickup_area = self.rect.inflate(40, 40)

        if pickup_area.colliderect(player.rect):
            score += self.points
            return True, score  # Tagastame True, et klaas saaks eemaldada
        return False, score

class Table(pygame.sprite.Sprite):  # Lisame pärimise pygame.sprite.Sprite klassist
    def __init__(self, x, y):
        super().__init__()  # Kutsume Sprite konstruktori
        self.image = pygame.Surface((50, 50))  # Määrame laua suuruse
        self.image.fill((150, 75, 0))  # Valime lauale pruuni värvi
        self.rect = self.image.get_rect(topleft=(x, y))  # Seadistame asukoha

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)