# Mängija klass koos mängija spetsiifilitse funktsioonidega
import pygame
from settings import WIDTH, HEIGHT
from object import Bar

bar = Bar

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, bar):
        super().__init__()
        self.image = image
        new_image = pygame.transform.scale(image, (64, 64))
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bar = bar
        self.BASE_SPEED = 80

    def handle_movement(self, keys, tables, delta):
        """Käsitleb mängija liikumist ja kontrollib kokkupõrkeid laudadesse ja baari tagumise ala vältimist."""
        move_x = 0
        move_y = 0

        # Arvutame liikumise vastavalt klahvivajutustele ja ajaintervallile
        if keys[pygame.K_UP] or keys[pygame.K_w] > 0:  # Ülespoole liikumine
            move_y = -self.BASE_SPEED * delta
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # Allapoole liikumine
            move_y = self.BASE_SPEED * delta
        if keys[pygame.K_LEFT] or keys[pygame.K_a] > 0:  # Vasakule liikumine
            move_x = -self.BASE_SPEED * delta
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Paremale liikumine
            move_x = self.BASE_SPEED * delta

        # Liigutame vastavalt arvutatud väärtusele
        self.rect.x += move_x
        self.rect.y += move_y

        # Kontrollime, et mängija ei liigu tumedale alale
        if self.rect.top < 50:
            self.rect.top = 50

        # Kontrollige, kas mängija ei lähe ekraanist välja
        if self.rect.left < 0:  # Mängija ei saa minna vasakule väljapoole
            self.rect.left = 0
        if self.rect.right > WIDTH:  # Mängija ei saa minna paremale väljapoole
            self.rect.right = WIDTH
        if self.rect.top < 0:  # Mängija ei saa minna ülespoole väljapoole
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:  # Mängija ei saa minna allapoole väljapoole
            self.rect.bottom = HEIGHT

        # Kontrollime, kas mängija puutub kokku baariga
        if self.rect.colliderect(self.bar.rect):
            # Kui mängija liigub baari taha (üles- või allapoole), piirame liikumist
            if self.rect.top < self.bar.rect.bottom and move_y < 0:  # Ei saa minna baari taha ülevalt
                self.rect.top = self.bar.rect.bottom
            if self.rect.bottom > self.bar.rect.top and move_y > 0:  # Ei saa minna baari taha altpoolt
                self.rect.bottom = self.bar.rect.top

        # Kontrollib kokkupõrkeid iga lauaga ja tühistab liikumise, kui on kokkupõrge
        for table in tables:
            if self.rect.colliderect(table.rect):
                if move_x > 0:  # Mängija liigub paremale, siis peata liikumine paremale
                    self.rect.right = table.rect.left
                if move_x < 0:  # Mängija liigub vasakule, siis peata liikumine vasakule
                    self.rect.left = table.rect.right
                if move_y > 0:  # Mängija liigub alla, siis peata liikumine alla
                    self.rect.bottom = table.rect.top
                if move_y < 0:  # Mängija liigub ülespoole, siis peata liikumine üles
                    self.rect.top = table.rect.bottom

    # Joonistab mängija ekraanile
    def draw(self, surface):
        surface.blit(self.image, self.rect)

#    pygame.draw.circle(screen, (0, 0, 255), (player_x, player_y), 50)

#    pygame.display.flip()
