import pygame
from settings import WIDTH, HEIGHT
from bar import Bar

bar = Bar

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, bar):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y
        self.bar = bar
        self.BASE_SPEED = 100

    def handle_movement(self, keys, tables, delta):
        """Käsitleb mängija liikumist ja kontrollib kokkupõrkeid laudadesse ja baari tagumise ala vältimist."""
        move_x = 0
        move_y = 0

        # Arvutame liikumise vastavalt klahvivajutustele ja ajaintervallile
        if keys[pygame.K_UP] or keys[pygame.K_w]:  # Ülespoole liikumine
            move_y = -self.BASE_SPEED * delta
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # Allapoole liikumine
            move_y = self.BASE_SPEED * delta
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Vasakule liikumine
            move_x = -self.BASE_SPEED * delta
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Paremale liikumine
            move_x = self.BASE_SPEED * delta

        # Liigutame vastavalt arvutatud väärtusele
        self.rect.x += move_x
        self.rect.y += move_y

        # Kontrollige, kas mängija ei lähe ekraanist välja
        if self.rect.left < 0:  # Mängija ei saa minna vasakule väljapoole
            self.rect.left = 0
        if self.rect.right > WIDTH:  # Mängija ei saa minna paremale väljapoole
            self.rect.right = WIDTH
        if self.rect.top < 0:  # Mängija ei saa minna ülespoole väljapoole
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:  # Mängija ei saa minna allapoole väljapoole
            self.rect.bottom = HEIGHT

        # Kontrollime, kas mängija puutub kokku baari
        if self.rect.colliderect(self.bar.rect):
            # Kui mängija liigub baari taha (üles- või allapoole), piirame liikumist
            if self.rect.top < self.bar.rect.bottom and move_y < 0:  # Ei saa minna baari taha ülespoole
                self.rect.top = self.bar.rect.bottom
            if self.rect.bottom > self.bar.rect.top and move_y > 0:  # Ei saa minna baari taha allapoole
                self.rect.bottom = self.bar.rect.top

        # Kontrollime kokkupõrkeid laudadega
        for table in tables:
            if self.rect.colliderect(table.rect):
                # Tühistame liikumise, kui on kokkupõrge lauaga
                self.rect.x -= move_x
                self.rect.y -= move_y

    def draw(self, surface):
        """Joonistab mängija ekraanile."""
        surface.blit(self.image, self.rect)

#    pygame.draw.circle(screen, (0, 0, 255), (player_x, player_y), 50)

#    pygame.display.flip()