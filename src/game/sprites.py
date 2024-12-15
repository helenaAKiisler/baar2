import pygame
import random
import os
from os import listdir
from os.path import isfile, join
from settings import WIDTH, HEIGHT, BLACK, GRAY

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
    COLOR = (255, 255, 255)
    SPRITES = load_sprite_sheets("../../assets/designs", "customer", 32, 32, True)
    ANIMATION_DELAY = 3
    BASE_SPEED = 2
    def __init__(self, x=100, y=100):  # Vaikimisi määrame x ja y väärtused
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = "left"
        self.rect.x = x
        self.rect.y = y

        self.direction_x = 1
        self.tables = tables

    def update(self):
        new_rect = self.rect.move(self.BASE_SPEED * self.direction_x, 0)

        if not any(new_rect.colliderect(table.rect) for table in self.tables):
            self.rect = new_rect
        else:
            self.direction_x *= -1

        if self.rect.right >= pygame.display.get_surface().get_width():
            self.direction_x = -1
        elif self.rect.left <= 0:
            self.direction_x = 1

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0


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
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left(PLAYER_VEL)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right(PLAYER_VEL)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.move_up(PLAYER_VEL)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
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
        if keys[pygame.K_UP] or keys[pygame.K_w] and self.rect.top > 0:
            move_y = -self.BASE_SPEED * delta
        if keys[pygame.K_DOWN] or keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            move_y = self.BASE_SPEED * delta
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.rect.left > 0:
            move_x = -self.BASE_SPEED * delta
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.rect.right < WIDTH:
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
        self.image = pygame.Surface((30, 30))  # Klaasi suurus
        self.image.fill(color)  # Klaasi värv
        self.rect = self.image.get_rect(topleft=(x, y))  # Klaasi asukoht
        self.points = points  # Klaasi punktiväärtus

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_pickup(self, player, score):
        # laiendan klaasi üleskorjamis/kokkupõrke ala
        pickup_area = self.rect.inflate(40, 40)

        if pickup_area.colliderect(player.rect):
            score += self.points
            return True, score  # Tagastame True, et klaas saaks eemaldada
        return False, score

class Table(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image  # Määrame laua suuruse
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)  # Seadistame asukoha