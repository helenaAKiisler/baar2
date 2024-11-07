import pygame
from settings import WIDTH, HEIGHT
from src.game.sprites import load_sprite_sheets


class Player(pygame.sprite.Sprite):
    BASE_SPEED = 100  # Põhikiirus pikslites sekundis
    SPRITES = load_sprite_sheets("../../assets/designs/character", "mees", 32, 32, True)
    ANIMATION_DELAY = 5

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
        self.sprite = self.SPRITES["idle_" + self.direction][0]
        surface.blit(self.sprite, (self.rect.x, self.rect.y))

#    pygame.draw.circle(screen, (0, 0, 255), (player_x, player_y), 50)

#    pygame.display.flip()