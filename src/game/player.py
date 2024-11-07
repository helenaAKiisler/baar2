import pygame
from settings import WIDTH, HEIGHT

class Player(pygame.sprite.Sprite):
    BASE_SPEED = 100  # Põhikiirus pikslites sekundis

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

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
        surface.blit(self.image, self.rect)

#    pygame.draw.circle(screen, (0, 0, 255), (player_x, player_y), 50)

#    pygame.display.flip()