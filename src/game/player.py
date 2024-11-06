import pygame
from settings import WIDTH, HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

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