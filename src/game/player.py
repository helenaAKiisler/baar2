import pygame
from settings import WIDTH, HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

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

    def handle_movement(self, keys, tables):
        """Käsitleb mängija liikumist ja kontrollib kokkupõrkeid laudadesse."""
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += 5
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

        # Kontrollib kokkupõrkeid iga lauaga
        for table in tables:
            if self.rect.colliderect(table.rect):
                # Kui on kokkupõrge, liigutab mängija tagasi
                if keys[pygame.K_UP]:
                    self.rect.y += 5
                if keys[pygame.K_DOWN]:
                    self.rect.y -= 5
                if keys[pygame.K_LEFT]:
                    self.rect.x += 5
                if keys[pygame.K_RIGHT]:
                    self.rect.x -= 5

    def draw(self, surface):
        """Joonistab mängija ekraanile."""
        surface.blit(self.image, self.rect)

#    pygame.draw.circle(screen, (0, 0, 255), (player_x, player_y), 50)

#    pygame.display.flip()